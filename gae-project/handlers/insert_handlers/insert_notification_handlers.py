'''
Created on Oct 17, 2016

@author: patterjm
'''
import json
import logging

from google.appengine.ext import ndb

from handlers import base_handlers
from models import Notification
import utils


class InsertNewNotificationAction(base_handlers.BaseAction):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        logging.info(self.request.get("receiver"))
        receiver = ndb.Key(urlsafe=self.request.get("receiver"))
        receiver_user = receiver.get().key.parent()
        notification = Notification(parent=receiver_user)
        
        notification.receiver = receiver_user
        notification.sender = ndb.Key(urlsafe=self.request.get("sender"))
        notification.message = self.request.get("message")
        notification.put()
        response = notification.key.urlsafe()
        self.response.out.write(json.dumps(response))