import webapp2
import re

myFile = open('searchDescriptions.txt','r')
re.split(';',myFile)
class Game(webapp2.RequestHandler):
	def get(self):
		top = '''
		<html>
			<head>
				<style>
				.div1 { border: 1px black ;}
				</style>
			</head>
		<body>'''
		for i in myFile:
			top += '''
			<div class="div1"> {} 
			</div>'''.format(i) 
		top += '''
			</body>
		</html>'''
		self.response.write(top)


