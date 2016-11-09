'''
Created on Oct 17, 2016

@author: patterjm
'''
import logging

from google.appengine.datastore.datastore_query import FilterPredicate
from google.appengine.ext import ndb

from handlers import base_handlers
from models import Project, Profile
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