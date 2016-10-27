'''
Created on Oct 17, 2016

@author: patterjm
'''
import logging

from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2

from handlers import base_handlers
import main
import utils
from models import Profile

class MainHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/main_page.html"
    
    def update_values(self, email, account_info, values):
        # Subclasses should override this method to add additional data for the Jinja template.
        project_query = utils.get_query_for_all_projects_for_email(email)
        logging.info(project_query)
        for project in project_query:
            logging.info(project)
        values["project_query"] = project_query
        
class ManageProjectsHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/manage_projects_page.html"

class AddProjectHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/add_project_page.html"
    
class AddProfileHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/temp_add_profile_page.html"

class AddCollaboratorHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/add_collaborator_page.html"
    
class ExploreProjectsHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/explore_new_projects_page.html"
    
class ManageCollaboratorsHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/manage_collaborators_page.html"

class ProjectDetailHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/project_detail_page.html"
    
class UserProfileHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/user_profile_page.html"
    
    def update_values(self, email, account_info, values):
        if self.request.get('profile_key'):
            profile = ndb.Key(urlsafe=self.request.get('profile_key')).get()
        else:
            profile = utils.get_profile_for_email(email)
        if not profile:
            parent_key = utils.get_parent_key_for_email(email)
            profile = Profile(parent=parent_key, id=email)
            profile.put()
        values["profile"] = profile
    
class LoginHandler(webapp2.RequestHandler):
    """Custom page to handle multiple methods of user authentication"""
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect("/")
        values = {"login_url": users.create_login_url("/")}
        template = main.jinja_env.get_template(self.get_template())
        self.response.out.write(template.render(values))
    
    def get_template(self):
        return "templates/login_page.html"