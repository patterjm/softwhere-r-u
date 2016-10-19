


import jinja2
import os
import webapp2
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


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # A basic template could just send text out the response stream, but we use Jinja
        # self.response.write("Hello world!")
        
        template = jinja_env.get_template("templates/main_page.html")
        values = {"title": "Hello, world! - deploy testing merge check"}
        self.response.out.write(template.render(values))
    

class ManageProjectHandler(webapp2.RequestHandler):
    def get(self):
        
        template = jinja_env.get_template("templates/manage_projects_page.html")
        values = {"title": "Hello, world! - deploy testing merge check"}
        self.response.out.write(template.render(values))

class AddProjectHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("templates/add_project_page.html")
        values = {"title": "Hello, world! - deploy testing merge check"}
        self.response.out.write(template.render(values))
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/manageProject', ManageProjectHandler),
    ('/addProject', AddProjectHandler)
], debug=True)
