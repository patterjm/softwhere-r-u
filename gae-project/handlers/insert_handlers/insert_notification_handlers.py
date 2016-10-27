'''
Created on Oct 17, 2016

@author: patterjm
'''
import logging

from google.appengine.ext import ndb

from handlers import base_handlers
from models import Notification
import utils


class InsertNewNotificationAction(base_handlers.BaseAction):
    def handle_post(self, email, account_info):
        if self.request.get("notification_entity_key"):
            notification_key = ndb.Key(urlsafe=self.request.get("notification_entity_key"))
            notification = notification_key.get()
        else:
            receiver = ndb.Key(urlsafe=self.request.get("receiver"))
            receiver_user = receiver.get().key.parent()
            logging.info(receiver_user)
            notification = Notification(parent=receiver_user)
        
        notification.receiver = ndb.Key(urlsafe=self.request.get("receiver")).get().key.parent()
        notification.sender = ndb.Key(urlsafe=self.request.get("sender"))
        notification_type = self.request.get("type")
        if notification_type == "collaborator":
            notification.message = "User would like to be your friend."
        notification.put()
        self.redirect(self.request.referer)