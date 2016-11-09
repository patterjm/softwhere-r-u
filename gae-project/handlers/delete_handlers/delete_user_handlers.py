'''
Created on Oct 17, 2016

@author: patterjm
'''
import logging

from google.appengine.ext import ndb

from handlers import base_handlers
from models import Notification, Profile


class DeleteFriendAction(base_handlers.BaseAction):
    def handle_post(self, email, account_info):
        sender_key_str = self.request.get("sender_entity_key")
        former_friend_key_str = self.request.get("former-friend")
        user = ndb.Key(urlsafe=sender_key_str).get()
        user.friends.remove(ndb.Key(urlsafe=former_friend_key_str))
        user.put()
        self.redirect(self.request.referer)