import webapp2

class Results(webapp2.RequestHandler):

	actualSearch = "";
	guess = " ";

	def post(self):
		guess=self.request.get('guess')

		myFile = open('actualSearch', 'r')

		actualSearch = myFile.readLine()

	def get(self):
		output = """
		<html>
			<head>
			</head>

			<body>

		"""
		output += "Your guess was " + guess + "\n"

		tempGuess = threshold(guess)
		tempActual = threshold(actualSearch)

		result = tempGuess == tempActual

		if result:
			output ++ "You are correct! Congratulations!\n"
		else:
			output += "That is not correct! You have failed....\n"

		output += pullScore(self, result)

		output += "The actual search was " + actualSearch

		output += 
		bottom = """
		</body>
		</html>
		"""

		output = output + bottom

		self.response.write(output)

	def threshold(theString):
		myFile = open('thresholds.txt')

		lines = []
		lines = myFile.readLines()

		for i in lines:
			theString.replace(i, "")

		return theString

	def pullScore(self, result):
		cookie_value = ""
		if 'google_game' in self.request.headers['Cookie']:
			cookie_value = self.request.cookies.get('google_game')
		else:
			cookie_value = 0
			self.response.set_cookie('google_game', '0',
				path='/results', domain='www.geopardygame.appspot.com', secure=false)

		score = int(cookie_value)
		if result:
			score += 1

		return "Your score is now " + str(score)