# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# IMPORTS AND ENVIRONMENT
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import jinja2
import os
import webapp2
import logging
import datetime
import urllib2
import json
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
LOADER = jinja2.FileSystemLoader(os.path.dirname(__file__))
jinja_environment = jinja2.Environment(loader = LOADER)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# DATA STRUCTURES / CLASSES
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# class ExampleClass(ndb.Model):
    # data
    # methods
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# HANDLERS
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# def main():
  # # Open the file, read it into memory as a single string.
  # with open('web2.txt') as web2_file:
    # words = web2_file.read()
   
  # return makeDict(words)     
numSearchTerms = 10 
start = 1
searchTerm = "kittens"

class HomeHandler(webapp2.RequestHandler):   
    def get(self):
        #Get Values
        #Modify Values
        try :
            url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q="+ searchTerm + "&start=" + str(start) + "&rsz=8"
            response = urllib2.urlopen(url)
            data = json.loads(response.read())
            responseData = data["responseData"]
            results = responseData["results"]
            content = []
            logging.info("----------------------------------------------------------------")
            for i in range(len(results)):
                content.append(results[i]["content"])
            logging.info("----------------------------------------------------------------")
            # logging.info(content)
        except TypeError :
            logging.info("Second call to data, null values found")
            pass






        template_values = {"content" : content}
        #Write Values
        template = jinja_environment.get_template('templates/home.html')
        self.response.out.write(template.render(template_values))
routes = [
    ('/.*', HomeHandler),
]
app = webapp2.WSGIApplication(routes, debug=True)