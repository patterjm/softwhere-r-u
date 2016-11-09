'''
Created on Oct 17, 2016

@author: patterjm
'''
import json
import logging

from google.appengine.ext import ndb

from handlers import base_handlers
from models import Notification, Profile
import utils


class InsertNewNotificationAction(base_handlers.BaseAction):
    def handle_post(self, email, account_info):
        if self.request.get("notification_entity_key"):
            notification_key = ndb.Key(urlsafe=self.request.get("notification_entity_key"))
            notification = notification_key.get()
        else:
            receiver = ndb.Key(urlsafe=self.request.get("receiver_entity_key"))
            receiver_user = receiver.parent()
            logging.info(receiver_user)
            notification = Notification(parent=receiver_user)
        
        notification.receiver = ndb.Key(urlsafe=self.request.get("receiver_entity_key"))
        notification.sender = ndb.Key(urlsafe=self.request.get("sender_entity_key"))
        notification_type = self.request.get("type")
        profile = Profile.query(ancestor=notification.sender).fetch(1)[0]
        if notification_type == "collaborator":
            notification.message = profile.name + " would like to be your friend."
        notification.put()
        self.redirect(self.request.referer)
        
class InsertNotificationActionAjax(base_handlers.BaseAction):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        logging.info(self.request.get("receiver"))
        receiver = ndb.Key(urlsafe=self.request.get("receiver"))
        logging.info(receiver)
        receiver_user = receiver.parent()
        logging.info(receiver_user)
        notification = Notification(parent=receiver_user)
        
        notification.receiver = receiver_user
        notification.sender = ndb.Key(urlsafe=self.request.get("sender"))
        notification.message = self.request.get("message")
        notification.put()
        response = notification.key.urlsafe()
        self.response.out.write(json.dumps(response))
        
class InsertManyNotifications(base_handlers.BaseAction):
    def handle_post(self, email, account_info):
        if self.request.get("project_entity_key"):
            project_key_str = self.request.get("project_entity_key")
            project_key = ndb.Key(urlsafe=project_key_str)
            project = project_key.get()
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
                            notification.put()
        self.redirect(self.request.referer)
