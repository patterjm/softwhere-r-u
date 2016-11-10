'''
Created on Oct 17, 2016

@author: patterjm
'''
import json
import logging

from google.appengine.api import users
from google.appengine.api.blobstore.blobstore import BlobKey
from google.appengine.datastore.datastore_query import FilterPredicate
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
import webapp2
from webapp2_extras import sessions

from handlers import base_handlers
from models import Project, Profile, Notification
import utils


class InsertNewProjectAction(base_handlers.BaseAction):
    def handle_post(self, email, account_info):
        if self.request.get("project_entity_key"):
            project_key = ndb.Key(urlsafe=self.request.get("project_entity_key"))
            project = project_key.get()
        else:
            project = Project(parent=utils.get_parent_key_for_email(email))
            project_key = project.key
        
        #add all users we find to the project.users, likewise add the project to the User entity
        users = [ndb.Key(urlsafe=self.request.get("user_entity_key"))]    
        potential_users_list = self.request.get_all("project_collaborator")
        for potential_user in potential_users_list:
            if potential_user and potential_user != utils.get_profile_for_email(email).name:
                profile_query = Profile.query(Profile.name == potential_user)
                for profile in profile_query:
                    user_key = profile.key.parent()
                    users.append(user_key)
        
        administrators = [ndb.Key(urlsafe=self.request.get("user_entity_key"))]
        
        project.title = self.request.get("project_title")
        project.description = self.request.get("project_description")
        project.administrators = administrators
        project.users = users
        project.put()
        
        for user_key in users:
            user = user_key.get()
            if not user.projects:
                user.projects = [project.key]
            else:
                user.projects.append(project.key)
            user.put()
            
        self.redirect(self.request.referer)
        
class UpdateProjectAdministrators(base_handlers.BaseAction):
    def handle_post(self, email, account_info):
        if self.request.get("project_entity_key"):
            project_key = ndb.Key(urlsafe=self.request.get("project_entity_key"))
            project = project_key.get()
        else:
            project = Project(parent=utils.get_parent_key_for_email(email))
            project_key = project.key
        
        #add all users we find to the project.users, likewise add the project to the User entity
        admin_key_list = []
        admin_list = self.request.get_all("admin_selected")   
        for admin_str in admin_list:
            admin_key = ndb.Key(urlsafe=admin_str)
            admin_key_list.append(admin_key.parent())
        project.administrators = admin_key_list
        project.put()
        
        self.redirect(self.request.referer)
        
class UpdateProjectUsers(base_handlers.BaseAction):
    def handle_post(self, email, account_info):
        if self.request.get("project_entity_key"):
            project_key = ndb.Key(urlsafe=self.request.get("project_entity_key"))
            project = project_key.get()
        else:
            project = Project(parent=utils.get_parent_key_for_email(email))
            project_key = project.key
        
        #add all users we find to the project.users, likewise add the project to the User entity
        updated_users_list = project.users
        user_list = self.request.get_all("user_selected")  
        for user_key_str in user_list:
            user_key = ndb.Key(urlsafe=user_key_str).parent()
            updated_users_list.remove(user_key)
        project.users = updated_users_list
        project.put()
        
        self.redirect(self.request.referer)
        
class UpdateProjectStatus(base_handlers.BaseAction):
    def handle_post(self, email, account_info):
        if self.request.get("project_entity_key"):
            project_key = ndb.Key(urlsafe=self.request.get("project_entity_key"))
            project = project_key.get()
        else:
            project = Project(parent=utils.get_parent_key_for_email(email))
            project_key = project.key
        
        archive = self.request.get("archive-project")
        complete = self.request.get("complete-project")
        
        if archive:
            project.status = project.ProjectStatus.ARCHIVED
        elif complete:
            project.status = project.ProjectStatus.COMPLETED
        
        project.put()
        
        self.redirect(self.request.referer)
        
class UpdateProjectAction(blobstore_handlers.BlobstoreUploadHandler):
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
        if self.request.get("project_entity_key"):
            project_key = ndb.Key(urlsafe=self.request.get("project_entity_key"))
            project = project_key.get()
        else:
            project = Project(parent=utils.get_parent_key_for_email(email))
            project_key = project.key
        
        title = self.request.get("title")
        description = self.request.get("description")
        project.title = title
        project.description = description
        
        admin_key_list = []
        admin_list = self.request.get_all("admin_selected")   
        for admin_str in admin_list:
            admin_key = ndb.Key(urlsafe=admin_str)
            admin_key_list.append(admin_key.parent())
        project.administrators = admin_key_list
        
        if self.get_uploads() and len(self.get_uploads()) == 1:
            logging.info("Received an image blob with this profile update.")
            media_blob = self.get_uploads()[0]
            project.picture = media_blob.key()
        else:
            # There is a chance this is an edit in which case we should check for an existing blob key.
            original_blob_key = self.request.get("original_blob_key")
            if original_blob_key:
                logging.info("Attaching original blob key (this must have been an edit or duplicate)")
                project.picture = BlobKey(original_blob_key)
        
        potential_invitees = self.request.get_all("project_collaborator")
        for potential_user in potential_invitees:
            if potential_user and potential_user != utils.get_profile_for_email(email).name:
                profile_query = Profile.query(Profile.name == potential_user)
                for profile in profile_query:
                    user_key = profile.key.parent()
                user = user_key.get()
                if user_key not in project.users:
                    notification_count = Notification.query(Notification.project_key == project_key, 
                                                            ndb.OR(Notification.sender == user_key, 
                                                                   Notification.receiver == user_key)).count()
                    if notification_count == 0:
                        notification = Notification(parent=user_key)
                        notification.sender = account_info.key
                        notification.receiver = user_key
                        notification.project_key = project_key
                        notification.message = utils.get_profile_for_email(email).name + " would like you to join " + project.title
                        notification.type = Notification.NotificationTypes.COLLABORATE
                        notification.put()
        
        project_status_str = self.request.get("status")
        if project_status_str == 'ACTIVE':   
            project.status = Project.ProjectStatus.ACTIVE
        elif project_status_str == 'ARCHIVED':
            project.status = Project.ProjectStatus.ARCHIVED
        elif project.status == 'COMPLETED':
            project.status = Project.ProjectStatus.COMPLETED
        
        project.put()
        
        self.redirect(self.request.referer)