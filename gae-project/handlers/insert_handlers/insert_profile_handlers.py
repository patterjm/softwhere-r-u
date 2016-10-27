'''
Created on Oct 17, 2016

@author: patterjm
'''
from google.appengine.ext import ndb

from handlers import base_handlers
from models import Profile
import utils


class InsertNewProfileAction(base_handlers.BaseAction):
    def handle_post(self, email, account_info):
        if self.request.get("profile_entity_key"):
            profile_key = ndb.Key(urlsafe=self.request.get("profile_entity_key"))
            profile = profile_key.get()
        else:
            profile = Profile(parent=account_info.key, id=email)
    
        profile.name = self.request.get("profile_name")
        profile.location = self.request.get("profile_location")
        profile.put()
        self.redirect(self.request.referer)