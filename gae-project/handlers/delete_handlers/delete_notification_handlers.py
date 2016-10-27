'''
Created on Oct 17, 2016

@author: patterjm
'''
import logging

from google.appengine.ext import ndb

from handlers import base_handlers
import utils


class DeleteNotificationAction(base_handlers.BaseAction):
    def handle_post(self, email, account_info):
        if self.request.get("notification_entity_key"):
            notification_key = ndb.Key(urlsafe=self.request.get("notification_entity_key"))
            notification = notification_key.get()
            accept = self.request.get("type-accept")
            if accept:
                test_val = self.request.get("sender_entity_key")
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
            notification.key.delete()
            self.redirect(self.request.referer)