'''
Created on Oct 17, 2016

@author: patterjm
'''
import json
import logging

from google.appengine.api import users
from google.appengine.api.blobstore.blobstore import BlobKey
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
import webapp2
from webapp2_extras import sessions

from handlers import base_handlers
from models import Profile
import utils


class InsertNewProfileAction(blobstore_handlers.BlobstoreUploadHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()
    """ALL action handlers should inherit from this one."""
    
    def post(self):
      user = users.get_current_user()
      if not user and "user_info" not in self.session:
        raise Exception("Missing user!")
      if user:
          email = user.email().lower()
      elif "user_info" in self.session:
          jsonVar = json.loads(self.session["user_info"])
          email = jsonVar["email"].lower()
      account_info = utils.get_account_info_for_email(email)
      self.handle_post(email, account_info)


    def get(self):
        self.post()  # Action handlers should not use get requests.
    
    def handle_post(self, email, account_info):
        if self.request.get("profile_entity_key"):
            profile_key = ndb.Key(urlsafe=self.request.get("profile_entity_key"))
            profile = profile_key.get()
        else:
            profile = Profile(parent=account_info.key, id=email)
            
        if self.get_uploads() and len(self.get_uploads()) == 1:
            logging.info("Received an image blob with this profile update.")
            media_blob = self.get_uploads()[0]
            profile.picture = media_blob.key()
        else:
            # There is a chance this is an edit in which case we should check for an existing blob key.
            original_blob_key = self.request.get("original_blob_key")
            if original_blob_key:
                logging.info("Attaching original blob key (this must have been an edit or duplicate)")
                profile.picture = BlobKey(original_blob_key)

        profile.name = self.request.get("name")
        profile.location = self.request.get("location")
        profile.description = self.request.get("description")
        profile.dob = self.request.get("dob")
        profile.put()
        self.redirect(self.request.referer)