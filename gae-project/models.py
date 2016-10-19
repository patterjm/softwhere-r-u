from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc.messages import Enum


class User(ndb.Model):
    """ Information about this user.  There is only 1 of these per user. """

    email = ndb.StringProperty(default="")
    friends = ndb.KeyProperty(kind='User', repeated=True)
    projects = ndb.KeyProperty(kind='Project', repeated=True)
    notifications = ndb.KeyProperty(kind='Notification', repeated=True)


class Profile(ndb.Model):
    """ Information about this user.  There is only 1 of these per user. """

    ID = ndb.StringProperty()
    name = ndb.StringProperty()
    description = ndb.TextProperty()
    picture = ndb.BlobProperty()
    dob = ndb.DateTimeProperty()


class Account(ndb.Model):
    """ Information about this user.  There is only 1 of these per user. """

    username = ndb.StringProperty()
    password = ndb.TextProperty()


class Notification(ndb.Model):
    """ Another example model object. """
    
    # Examples of some different property types.
    ID = ndb.StringProperty()
    sender = ndb.KeyProperty(kind='User')
    receiver = ndb.KeyProperty(kind='User')
    message = ndb.TextProperty()
    time_stamp = ndb.DateTimeProperty()
    has_been_viewed = ndb.BooleanProperty(default=False)


class Project(ndb.Model):
    """ Project object. Users can have and manage these """

    ID = ndb.StringProperty()
    title = ndb.StringProperty()
    description = ndb.TextProperty()
    administrators = ndb.KeyProperty(kind='User', repeated=True)
    date_created = ndb.DateTimeProperty()
    users = ndb.KeyProperty(kind='User', repeated=True)

    class ProjectStatus(Enum):

        ARCHIVED = 0
        ACTIVE = 1
        COMPLETED = 2

    status = msgprop.EnumProperty(ProjectStatus)
