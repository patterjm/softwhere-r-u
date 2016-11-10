'''
Created on Oct 17, 2016

@author: patterjm
'''
import json

from google.appengine.ext import ndb
import webapp2


class DeleteUserFromProjectAction(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        user_key_str = self.request.get("user_key")
        project_key_str = self.request.get("project_key")
        
        user_key = ndb.Key(urlsafe=user_key_str)
        project_key = ndb.Key(urlsafe=project_key_str)
        
        user = user_key.get()
        project = project_key.get()
        
        if user_key in project.administrators:
            project.administrators.remove(user_key)
        
        if user_key in project.users:
            project.users.remove(user_key)
            
        if project_key in user.projects:
            user.projects.remove(project_key)
            
        project.put()
        user.put()
        response = {}
        self.response.out.write(json.dumps(response))