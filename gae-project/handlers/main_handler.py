'''
Created on Oct 17, 2016

@author: patterjm
'''
import json
import json
import logging

from google.appengine.api import users
from google.appengine.api.blobstore import blobstore
from google.appengine.ext import ndb
import webapp2
from webapp2_extras import sessions

from github import Github
from github.GithubException import BadCredentialsException
from handlers import base_handlers
import main
from models import Profile, Notification
import utils


class MainHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/main_page.html"
    
    def update_values(self, email, account_info, values):
        # Subclasses should override this method to add additional data for the Jinja template.
        values["project_query"] = account_info.projects
        
class ManageProjectsHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/manage_projects_page.html"
    
    def update_values(self, email, account_info, values):
        # Subclasses should override this method to add additional data for the Jinja template.
        values["project_query"] = account_info.projects

class AddProjectHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/add_project_page.html"
    
class AddProfileHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/temp_add_profile_page.html"

class ManageFriendsHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/manage_friend_page.html"

class AddFriendsHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/add_friend_page.html"
    
class ExploreProjectsHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/explore_new_projects_page.html"
    
class ManageCollaboratorsHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/manage_collaborators_page.html"

class ProjectDetailHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/project_detail_page.html"
    
    def update_values(self, email, account_info, values):
        #preload null values to prevent Jinja UndefinedError
        values["project"] = None
        values["is_administrator"] = False
        values["is_collaborator"] = False
        values["is_active"] = False
        values["active_collaboration_request"] = False
        values["is_sender"] = False
        values["is_receiver"] = False
        
        if self.request.get('project_entity_key'):
            project_entity_key_str = self.request.get('project_entity_key')
            project_key = ndb.Key(urlsafe=project_entity_key_str)
            project = project_key.get()
            
            values["project"] = project
            
            if project.status == project.ProjectStatus.ACTIVE:
                values["is_active"] = True
            #build user list to be rendered in Collaborators section
            profile_list = []
            
            for user_key in project.users:
                profile = Profile.query(ancestor=user_key).fetch(1)
                profile_list.append(profile[0])
            values["profiles"] = profile_list
            
            #check if accessing user is a project administrator
            if account_info.key in project.administrators:
                values["is_administrator"] = True
                
            #check if user is a collaborator
            if account_info.key in project.users:
                values["is_collaborator"] = True
            else:
                #check if accessing user received a friend request from profile owner
                notification_receiver_query = Notification.query(Notification.receiver == account_info.key, Notification.project_key == project_key)
                for notification in notification_receiver_query:
                    values["active_collaboration_request"] = True
                    values["is_receiver"] = True
                    values["is_sender"] = False
                    
                #check if accessing user sent a friend request to profile owner
                notification_receiver_query = Notification.query(Notification.sender == account_info.key, Notification.project_key == project_key)
                for notification in notification_receiver_query:
                    values["active_collaboration_request"] = True
                    values["is_receiver"] = False
                    values["is_sender"] = True

        
class UserProfileHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/user_profile_page.html"
    
    def update_values(self, email, account_info, values):
        #preload null values to prevent Jinja UndefinedError
        values["profile"] = None
        values["is_owner"] = False
        values["is_friend"] = False
        values["pending_friend_request"] = False
        values["is_receiver"] = False
        values["is_sender"] = False
        
        if self.request.get('profile_entity_key'):
            profile_entity_key_str = self.request.get('profile_entity_key')
            profile_key = ndb.Key(urlsafe=profile_entity_key_str)
            profile = profile_key.get()
        else:
            profile = utils.get_profile_for_email(email)
        if profile:
            profile_key = profile.key
            values["profile"] = profile
            user = utils.get_user_for_email(email)
            #build project list to be rendered in Featured Projects section
            project_list = []
            for project_key in user.projects:
                project = project_key.get()
                project_list.append(project)
            values["projects"] = project_list
            
            #check if accessing user is profile owner    
            if email == profile_key.id():
                values["is_owner"] = True
            else:
                values["is_owner"] = False
                
                #check if users are friends
                if profile_key.parent() in user.friends:
                    values["is_friend"] = True
                else:
                    #check if accessing user received a friend request from profile owner
                    notification_receiver_query = Notification.query(Notification.receiver == user.key,
                                       Notification.sender == profile_key.parent())
                    for notification in notification_receiver_query:
                        values["pending_friend_request"] = True
                        values["is_receiver"] = True
                        values["is_sender"] = False
                    
                    #check if accessing user sent a friend request to profile owner
                    notification_sender_query = Notification.query(Notification.sender == user.key,
                                       Notification.receiver == profile_key.parent())
                    for notification in notification_sender_query:
                        values["pending_friend_request"] = True
                        values["is_receiver"] = False
                        values["is_sender"] = True
        #set-up modal for uploading blob_images
        values["form_action"] = blobstore.create_upload_url('/insert-profile')

    

class LoginHandler(base_handlers.BaseHandler):
    """Custom page to handle multiple methods of user authentication"""
    def get(self):
        user = users.get_current_user()
        if user or "user_info" in self.session:
            self.redirect("/")
        values = {"login_url": users.create_login_url("/")}
        template = main.jinja_env.get_template(self.get_template())
        self.response.out.write(template.render(values))
    
    def get_template(self):
        return "templates/login_page.html"
    
    def post(self):
        username = self.request.get("gitUsername")
        password = self.request.get("gitPassword")
        logging.info(username)
        logging.info(password)
        g = Github(username,password)
        user = g.get_user()
        try:
            name = user.name
            logging.info(name)
            self.serve_page(False)
        except BadCredentialsException:
            self.serve_page(True)
            
    def serve_page(self, failed=False):
        if failed:
            logging.info("--------failed")
            values={"failed": failed}
            template = main.jinja_env.get_template(self.get_template())
            self.response.out.write(template.render(values))
            return "templates/login_page.html"
        username = self.request.get("gitUsername")
        password = self.request.get("gitPassword")

        email = filter(lambda obj: obj["primary"] == True, Github(username, password).get_user().get_emails())[0]["email"]
        user_info = {"username":username,
                     "email":email
            }
        self.session['user_info'] = json.dumps(user_info)
        self.redirect('/')
class LogoutHandler(base_handlers.BaseHandler):
    def get(self):
        del self.session["user_info"]
        self.redirect(uri="/")
