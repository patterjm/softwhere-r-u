'''
Created on Oct 17, 2016

@author: patterjm
'''
from google.appengine.api import users
import webapp2

from handlers import base_handlers
import main


class MainHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/main_page.html"
        
class ManageProjectsHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/manage_projects_page.html"

class AddProjectHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/add_project_page.html"

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
    
class LoginHandler(webapp2.RequestHandler):
    """Custom page to handle multiple methods of user authentication"""
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect("/")
        values = {};
        template = main.jinja_env.get_template(self.get_template())
        self.response.out.write(template.render(values))
    
    def get_template(self):
        return "templates/login_page.html"