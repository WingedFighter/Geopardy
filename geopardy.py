# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# IMPORTS AND ENVIRONMENT
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import jinja2
import os
import webapp2
import logging
import datetime
import urllib2
import time
import random
import json
from results import Results
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from google.appengine.ext import ndb


LOADER = jinja2.FileSystemLoader(os.path.dirname(__file__))
jinja_environment = jinja2.Environment(loader = LOADER)

lines = []

rawr = open('searchTerms.txt','r')   

with open('searchTerms.txt','r') as f:
    lines = f.readlines()
for x in range(0, len(lines)):
    lines[x] = lines[x].strip()
rawr.close()

class Search(ndb.Model):
    searchBlocks = ndb.JsonProperty()
    answer = ndb.StringProperty()

def getSearch(searchword=None):
  if searchword == None:
    searchword = random.choice(lines)
  s = ndb.Key("Search", searchword).get()
  if s == None:
    try:
      createSearch(searchword)
      return getSearch(searchword)
    except Exception:
      return Search.query().fetch(1)[0]
  else:
    return s
    

def createSearch(searchword):
    try :
        url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%r&start=1&rsz=8" % searchword
        response = urlfetch.fetch(url)
        data = json.loads(response.content)
        responseData = data["responseData"]
        results = responseData["results"]
        content = []
        
        for i in range(len(results)):
            content.append(results[i]["content"])
        
        s = Search(searchBlocks = removeSearchTerm(content, searchword), answer = searchword)
        s.key = ndb.Key("Search", searchword)
        s.put()
    except Exception as e:
        logging.info("Search issue" + str(e))
        raise e


def removeSearchTerm(listOfInfo, searchword):
    for info in xrange(len(listOfInfo)):
      listOfInfo[info] = listOfInfo[info].lower().replace(searchword.lower(), "_____")
    return listOfInfo


class HomeHandler(webapp2.RequestHandler):   
    def get(self):
        search = getSearch()
        correct = search.answer
        content = search.searchBlocks
        template_values = {"content" : content, 
                            "correct" : correct
                            }
        template = jinja_environment.get_template('templates/home.html')
        self.response.out.write(template.render(template_values))


class ResultHandler(webapp2.RequestHandler):
    def post(self):
        answer = self.request.get("answer")
        correct = self.request.get("correct")
        template_values = {"correct" : correct,
                            "answer" : answer,
                            }
        template = jinja_environment.get_template('templates/results.html')
        self.response.out.write(template.render(template_values))

routes = [
    
    ('/', HomeHandler),
    ('/result', ResultHandler),
    
]
app = webapp2.WSGIApplication(routes, debug=True)