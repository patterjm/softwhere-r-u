import logging

from google.appengine.ext import ndb

from models import User, Notification, Project, Profile


def get_parent_key_for_email(email):
    """ Gets the parent key (the key that is the parent to all Datastore data for this user) from the user's email. """
    return ndb.Key("Entity", email.lower())

def get_query_for_all_user_profiles(email):
    email_profile = get_profile_for_email(email)
    email_key = email_profile.key
    logging.info(email_key.urlsafe())
    user_key = email_key.parent()
    user = user_key.get()
    friends = user.friends
    logging.info(friends)
    qry =  Profile.query(Profile.key != email_key)
    for friend in friends:
        logging.info(friend.urlsafe())
        qry = qry.filter(ndb.AND(friend!=Profile.key))
    return qry

def get_self_profile(email):
    email_key = get_profile_for_email(email).key
    return Profile.query(Profile.key == email_key)

def get_account_info_for_email(email, create_if_none=False):
    """ Gets the one and only AccountInfo object for this email. Returns None if User object doesn't exist. """
    email = email.lower()  # Just in case.
    parent_key = get_parent_key_for_email(email)
    account_info = User.get_by_id(email, parent=parent_key)
    
    if create_if_none and not account_info:
        parent_key = get_parent_key_for_email(email)
        logging.info("Creating a new User for user " + email)
        account_info = User(parent=parent_key, id=email)
        account_info.email = email
        account_info.friends = []
        account_info.put()
  
    return account_info
 
 
def get_query_for_all_notifications_for_email(email):
    """ Returns a query for all notifications for this user. """
    parent_key = get_parent_key_for_email(email)
    return Notification.query(ancestor=parent_key).order(Notification.time_stamp)

def get_query_for_all_projects_for_email(email):
    """ Returns a query for all projects for this user. """
    parent_key = get_parent_key_for_email(email)
    return Project.query(ancestor=parent_key).order(Project.date_created)

def get_profile_for_email(email):
    parent_key = get_user_for_email(email).key
    return Profile.get_by_id(email, parent=parent_key)

def get_user_for_email(email):
    parent_key = get_parent_key_for_email(email)
    return User.get_by_id(email, parent=parent_key)
