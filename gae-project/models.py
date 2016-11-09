from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc.messages import Enum    

class User(ndb.Model):
    """ Information about this user.  There is only 1 of these per user. """
    email = ndb.StringProperty(default="")
    friends = ndb.KeyProperty(kind='User', repeated=True)
    projects = ndb.KeyProperty(kind='Project', repeated=True)


class Profile(ndb.Model):
    """ Information about this user.  There is only 1 of these per user. """
    name = ndb.StringProperty()
    location = ndb.StringProperty()
    description = ndb.TextProperty()
    picture = ndb.BlobKeyProperty()
    dob = ndb.DateProperty()


class Account(ndb.Model):
    """ Information about this user.  There is only 1 of these per user. """
    username = ndb.StringProperty()
    password = ndb.TextProperty()


class Notification(ndb.Model):
    """ Another example model object. """
    sender = ndb.KeyProperty(kind='User')
    receiver = ndb.KeyProperty(kind='User')
    project_key = ndb.KeyProperty(kind='Project')
    message = ndb.TextProperty()
    time_stamp = ndb.DateTimeProperty(auto_now=True)
    has_been_viewed = ndb.BooleanProperty(default=False)

    class NotificationTypes(Enum):
        FRIEND = 0
        COLLABORATE = 1
        REQUESTJOIN = 2
    
    type = msgprop.EnumProperty(NotificationTypes, default=NotificationTypes.FRIEND)

class Project(ndb.Model):
    """ Project object. Users can have and manage these """
    title = ndb.StringProperty()
    description = ndb.TextProperty()
    administrators = ndb.KeyProperty(kind='User', repeated=True)
    date_created = ndb.DateTimeProperty(auto_now=True)
    users = ndb.KeyProperty(kind='User', repeated=True)

    class ProjectStatus(Enum):
        ARCHIVED = 0
        ACTIVE = 1
        COMPLETED = 2

    status = msgprop.EnumProperty(ProjectStatus, default=ProjectStatus.ACTIVE)
