from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc.messages import Enum


class AccountInfo(ndb.Model):
    """ Information about this user.  There is only 1 of these per user. """

    # Example property for this example model object.
    name = ndb.StringProperty(default="")


class MyObjectClassName(ndb.Model):
    """ Another example model object. """
    
    # Examples of some different property types.
    someProperty = ndb.StringProperty(default="")
    non_indexed_string = ndb.TextProperty()
    datetime = ndb.DateTimeProperty(auto_now_add=True, auto_now=False)
    boolean = ndb.BooleanProperty(default=False)
    someNumericfieldName = ndb.IntegerProperty()
    float = ndb.FloatProperty()
    repeatedField = ndb.StringProperty(repeated=True)
    
    class ExampleEnum(Enum):
        """ Properties that can only have a few values."""
        OPTION_1 = 1
        OPTION_2 = 2
        OPTION_3 = 3
    recipient_type = msgprop.EnumProperty(ExampleEnum, default=ExampleEnum.OPTION_1)
    
class MyOtherClassName(ndb.Model):
    """ Yet another example model object. """
  
    single_key = ndb.KeyProperty(kind=MyObjectClassName)
    list_of_keys = ndb.KeyProperty(kind=MyObjectClassName, repeated=True)
    

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
