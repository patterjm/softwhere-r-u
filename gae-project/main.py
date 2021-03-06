import os

import jinja2
import webapp2

from handlers import main_handler, blob_handler
from handlers.delete_handlers import delete_notification_handlers, \
    delete_user_handlers, delete_project_handlers
from handlers.insert_handlers import insert_project_handlers, insert_profile_handlers, \
    insert_notification_handlers


# Jinja environment instance necessary to use Jinja templates.
def __init_jinja_env():
    jenv = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols", "jinja2.ext.with_"],
        autoescape=True)
    # Example of a Jinja filter (useful for formatting data sometimes)
    #   jenv.filters["time_and_date_format"] = date_utils.time_and_date_format
    return jenv

jinja_env = __init_jinja_env()
config = {}
config['webapp2_extras.sessions'] = {
    # This key is used to encrypt your sessions
    'secret_key': 'mysupersecretkey',
}
app = webapp2.WSGIApplication([
    ('/', main_handler.MainHandler),
    ('/add-project', main_handler.AddProjectHandler),    
    ('/login-page', main_handler.LoginHandler),
    ('/add-friends', main_handler.AddFriendsHandler),
    ('/explore-new-projects', main_handler.ExploreProjectsHandler),
    ('/manage-friends', main_handler.ManageFriendsHandler),
    ('/project-detail', main_handler.ProjectDetailHandler),
    ('/user-profile', main_handler.UserProfileHandler),
    ('/temp-add-profile', main_handler.AddProfileHandler),
    ('/logout', main_handler.LogoutHandler),
    
    ('/insert-project', insert_project_handlers.InsertNewProjectAction),
    ('/update-project', insert_project_handlers.UpdateProjectAction),
    ('/insert-profile', insert_profile_handlers.InsertNewProfileAction),
    ('/insert-notification', insert_notification_handlers.InsertNewNotificationAction),
    ('/insert-notification-ajax', insert_notification_handlers.InsertNotificationActionAjax),
    ('/insert-many-notifications', insert_notification_handlers.InsertManyNotifications),
    ('/update-project-status', insert_project_handlers.UpdateProjectStatus),
    ('/update-project-administrators', insert_project_handlers.UpdateProjectAdministrators),
    ('/update-project-users', insert_project_handlers.UpdateProjectUsers),
    ('/delete-friend', delete_user_handlers.DeleteFriendAction),
    ('/delete-project-user', delete_project_handlers.DeleteUserFromProjectAction),
    ('/delete-notification', delete_notification_handlers.DeleteNotificationAction),
    ('/cancel-friendrequest' ,main_handler.CancelRequestHandler), 
    ('/check-notification', main_handler.CheckNotiHandler),
    ('/get-users', main_handler.GetProfilesByNameHandler),
    ('/request-join', main_handler.RequestJoinHandler),
    ('/pics/([^/]+)?', blob_handler.BlobServer),
    
], config=config, debug=True)
