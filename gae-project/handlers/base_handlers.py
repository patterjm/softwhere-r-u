
import json
import logging

from google.appengine.api import users
import webapp2
from webapp2_extras import sessions

import main
import utils
import json


class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

class BasePage(BaseHandler):
  """Page handlers should inherit from this one."""
  def get(self):
    user = users.get_current_user()
    if not user and "user_info" not in self.session:
      self.redirect("/login-page")
      return
    if user:
        email = user.email().lower()
        logout_url = users.create_logout_url("/")
    elif self.session["user_info"]:
        email = json.loads(self.session["user_info"])["email"]
        logout_url = "/logout"
    account_info = utils.get_account_info_for_email(email, create_if_none=True)
    values = {"user_email": email,
              "account_info": account_info,
              "logout_url": logout_url}
    self.update_values(email, account_info, values)
    template = main.jinja_env.get_template(self.get_template())
    notification_query = utils.get_query_for_all_notifications_for_email(email)
    logging.info(notification_query)
    for notification in notification_query:
        logging.info(notification)
    values["notification_query"] = notification_query
    values["num_noti"] = notification_query.count()
    if notification_query.count() == 0:
        values["noti_empty"] = False;
    else:
        values["noti_empty"] = True;
    self.response.out.write(template.render(values))


  def update_values(self, email, account_info, values):
    # Subclasses should override this method to add additional data for the Jinja template.
    pass

  def get_template(self):
    # Subclasses must override this method to set the Jinja template.
    raise Exception("Subclass must implement handle_post!")



### Actions ###

class BaseAction(BaseHandler):
  """ALL action handlers should inherit from this one."""
  def post(self):
    user = users.get_current_user()
    if not user and "user_info" not in self.session:
      raise Exception("Missing user!")
    if user:
        email = user.email().lower()
    elif self.session["user_info"]:
        email = json.loads(self.session["user_info"])["email"]
    account_info = utils.get_account_info_for_email(email)
    self.handle_post(email, account_info)


  def get(self):
    self.post()  # Action handlers should not use get requests.


  def handle_post(self, email, account_info):
    # Subclasses must override this method to handle the requeest.
    raise Exception("Subclass must implement handle_post!")
