'''
Created on Oct 17, 2016

@author: patterjm
'''
from google.appengine.ext import ndb

from handlers import base_handlers
from models import Project
import utils


class InsertNewProjectAction(base_handlers.BaseAction):
    def handle_post(self, email, account_info):
        if self.request.get("project_entity_key"):
            project_key = ndb.Key(urlsafe=self.request.get("project_entity_key"))
            project = project_key.get()
        else:
            project = Project(parent=utils.get_parent_key_for_email(email))
    
        project.title = self.request.get("project_title")
        project.description = self.request.get("project_description")
        project.administrators = [ndb.Key(urlsafe=self.request.get("user_entity_key"))]
        project.users = [ndb.Key(urlsafe=self.request.get("user_entity_key"))]
        project.put()
        
        user = utils.get_user_for_email(email)
        user.projects.push(project_key)
        self.redirect(self.request.referer)