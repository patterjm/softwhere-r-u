from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc.messages import Enum


# TODO: Implement




# Potentially helpful (or not) NDB Snippets - For reference only (delete or comment out)
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
    