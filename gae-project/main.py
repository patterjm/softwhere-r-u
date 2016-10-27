import os

import jinja2
import webapp2

from handlers import main_handler
from handlers.insert_handlers import insert_project_handlers, insert_profile_handlers



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

app = webapp2.WSGIApplication([
    ('/', main_handler.MainHandler),
    ('/manage-projects', main_handler.ManageProjectsHandler),
    ('/add-project', main_handler.AddProjectHandler),    
    ('/login-page', main_handler.LoginHandler),
    ('/add-collaborator', main_handler.AddCollaboratorHandler),
    ('/explore-new-projects', main_handler.ExploreProjectsHandler),
    ('/manage-collaborators', main_handler.ManageCollaboratorsHandler),
    ('/project-detail', main_handler.ProjectDetailHandler),
    ('/user-profile', main_handler.UserProfileHandler),
    ('/temp-add-profile', main_handler.AddProfileHandler),
    
    ('/insert-project', insert_project_handlers.InsertNewProjectAction),
    ('/insert-profile', insert_profile_handlers.InsertNewProfileAction),
    
    
], debug=True)
