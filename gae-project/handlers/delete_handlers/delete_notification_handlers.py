'''
Created on Oct 17, 2016

@author: patterjm
'''
import logging

from google.appengine.ext import ndb

from handlers import base_handlers
import utils
from models import Notification


class DeleteNotificationAction(base_handlers.BaseAction):
    def handle_post(self, email, account_info):
        if self.request.get("notification_entity_key"):
            notification_key = ndb.Key(urlsafe=self.request.get("notification_entity_key"))
            notification = notification_key.get()
        else:
            sender_key = ndb.Key(urlsafe=self.request.get("sender_entity_key"))
            receiver_key = ndb.Key(urlsafe=self.request.get("receiver_entity_key"))
            
            notifications_query = Notification.query(Notification.sender == sender_key, 
                                                     Notification.receiver == receiver_key, 
                                                     Notification.type == Notification.NotificationTypes.FRIEND)
            for notification_result in notifications_query:
                notification = notification_result
            
        accept = self.request.get("type-accept")
        if accept and notification.type == Notification.NotificationTypes.FRIEND:
            notification_sender = ndb.Key(urlsafe=self.request.get("sender_entity_key"))
            sender_user = notification_sender.get()
            current_user = utils.get_user_for_email(email)
            if sender_user.friends:
                sender_user.friends.append(current_user.key)
            else:
                sender_user.friends = [current_user.key]
            if current_user.friends:
                current_user.friends.append(sender_user.key)
            else:
                current_user.friends = [sender_user.key]
                
            sender_user.put()
            current_user.put()
        elif accept and notification.type == Notification.NotificationTypes.COLLABORATE:
            project = notification.project_key.get()
            project.users.append(account_info.key)
            project.put()
            
            account_info.projects.append(project.key)
            account_info.put()
        notification.key.delete()
            
        self.redirect(self.request.referer)