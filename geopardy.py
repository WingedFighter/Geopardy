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

  
numSearchTerms = 10
currentKeys = 0
keys = []
lines = []
start = time.clock()
refreshTimer = 100

rawr = open('searchTerms.txt','r')   

with open('searchTerms.txt','r') as f:
    lines = f.readlines()
for x in range(0, len(lines)):
    lines[x] = lines[x].strip()
rawr.close()



class Search(ndb.Model):
    searchBlocks = ndb.JsonProperty()
    answer = ndb.StringProperty()

def getSearch():
    try:
        i = random.choice(keys)
        return i.get()
    except IndexError:
        createSearch()
        return getSearch()
    

def createSearch():
    global currentKeys
    searchword = lines[currentKeys]
    try :
        # logging.info("----------------------------------------------------------------")
        # logging.info(searchword);
        url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%r&start=1&rsz=8" % searchword
        # logging.info(url)
        # logging.info("----------------------------------------------------------------")
        response = urlfetch.fetch(url)
        # logging.info(type(response))
        # logging.info("----------------------------------------------------------------")
        # logging.info("----------------------------------------------------------------")
        # logging.info(response.content)
        # logging.info("----------------------------------------------------------------")
        # logging.info("----------------------------------------------------------------")
        data = json.loads(response.content)
        responseData = data["responseData"]
        results = responseData["results"]
        content = []
        
        for i in range(len(results)):
            content.append(results[i]["content"])
        
        s = Search(searchBlocks = removeSearchTerm(content, searchword), answer = searchword)
        s_key = s.put()
        keys.append(s_key)
        currentKeys += 1

    except TypeError:
        logging.info("JSON issue")
        pass


def removeSearchTerm(listOfInfo, searchword):
    for info in range(len(listOfInfo)):
        if searchword.lower() in listOfInfo[info].lower():
            listOfInfo[info] = listOfInfo[info].lower().replace(searchword.lower(), "_____")
            # logging.info("************************************************")
            # logging.info("Claims replacement")
            # logging.info("************************************************")
    return listOfInfo


class HomeHandler(webapp2.RequestHandler):   
    def get(self):
        #Get Values
        #Modify Values
        global start
        logging.info("==========================================================")
        logging.info(time.clock()-start)
        logging.info("==========================================================")
        if(time.clock() - start > refreshTimer):
            createSearch()
            start = time.clock()

        search = getSearch()
        correct = search.answer
        content = search.searchBlocks
        template_values = {"content" : content, 
                            "correct" : correct
                            }
        #Write Values
        template = jinja_environment.get_template('templates/home.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        answer = self.request.get("answer")
        correct = self.request.get("correct")
        logging.info("Answer : ")
        logging.info(answer)
        logging.info("Correct : ")
        logging.info(correct)
        logging.info("NumKeys : ")
        logging.info(len(keys))
        if(answer.lower() == correct.lower()):
            logging.info("We won")




routes = [
    
    ('/.*', HomeHandler),
    
]
app = webapp2.WSGIApplication(routes, debug=True)