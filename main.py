import os
import cgi
import datetime
import wsgiref.handlers
import appengine_admin
import settings

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import run_wsgi_app

class Objective(db.Model):
  Description = db.StringProperty(multiline=True)
  Date = db.DateProperty()
  def __str__(self):
      return str(self.Description)
  
class AdminObjective(appengine_admin.ModelAdmin):
    model = Objective
    listFields = ('Description', 'Date')
    editFields = ('Description', 'Date')


appengine_admin.register(AdminObjective)
  

class Educations(db.Model):
  Start_Date = db.DateProperty()
  End_Date = db.DateProperty()
  Where = db.StringProperty(multiline=True)
  Description = db.StringProperty(multiline=True)
  def __str__(self):
      return str(self.Where)
  
class AdminEducations(appengine_admin.ModelAdmin):
    model = Educations
    listFields = ('Start_Date', 'End_Date', 'Where','Description')
    editFields = ('Start_Date', 'End_Date', 'Where','Description')

appengine_admin.register(AdminEducations) 

class Experience(db.Model):
    Start_Date = db.DateProperty()
    End_Date = db.DateProperty()
    Where = db.StringProperty(multiline=True)
    Role = db.StringProperty(multiline=True)
    Description = db.StringProperty(multiline=True)
    def __str__(self):
        return str(self.Where)
  
class AdminExperience(appengine_admin.ModelAdmin):
    model = Experience
    listFields = ('Start_Date','Role', 'End_Date', 'Where','Description')
    editFields = ('Start_Date','Role', 'End_Date', 'Where','Description')

appengine_admin.register(AdminExperience)   

class Skill(db.Model):
    Type =  db.StringProperty(multiline=True)
    Skills =  db.StringListProperty()
    def __str__(self):
      return str(self.Type)
  
class AdminSkill(appengine_admin.ModelAdmin):
    model = Skill
    listFields = ('Type','Skills')
    editFields = ('Type','Skills')

appengine_admin.register(AdminSkill)  
  

objectives = db.GqlQuery("SELECT * "
                       "FROM Objective "
                       "ORDER BY Description")

educations = db.GqlQuery("SELECT * "
                       "FROM Educations "
                       "ORDER BY End_Date")
  
experiences = db.GqlQuery("SELECT * "
                       "FROM Experience "
                       "ORDER BY End_Date")  

skills = db.GqlQuery("SELECT * "
                       "FROM Skill "
                       "ORDER BY Type")  

class MainHandler(webapp.RequestHandler):
    def get(self):

        template_values = {
                           'objectives': objectives,
                           'educations': educations,
                           'experiences':experiences,
                           'skills':skills,
                           'name': settings.Name,
                           'sourname': settings.Sourname,
                           'role': settings.Role,
                           'address': settings.Address,
                           'email': settings.Email,
                           'phone':settings.Phone,
                           'web':settings.WebSite,
                           'photo':settings.Photo,                       
        }
        
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/', MainHandler)], debug=True)

def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                         (r'^(/admin)(.*)$', appengine_admin.Admin)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()