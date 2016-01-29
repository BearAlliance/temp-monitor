import twitter
import datetime

# Returns temperature reading as a string
def getTempReading():
	# don't have the sensor yet, just return a value

	temp = 68.5

	return str(temp)

# Saves the temperature to a database for fun graphs later
def saveToDb(temp):
	# no DB yet
	return

# Returns formated dat time string
# Ex: '01/12 4:40PM'
def getDateTimeString():
	now = datetime.datetime.now()
	return now.strftime('%m/%d %-I:%M%p')

def tweetTemperature(temp):
	dateTime = getDateTimeString()

	tweet = dateTime + " Temperature is " + temp + 'F'

	# Tweet temperature
	print 'initializing Twitter API'
	api = twitter.Api(consumer_key = '4zaWW67mmvqFUgtXeBDSzTmzK',
					  consumer_secret = 'QxBCXzgidWb5JvPfx3gmFhKSJpz2HPkjxgUSqvEatIxWALzZXa',
					  access_token_key = '4861195187-49Fca2M8tq3zqQqrflRXgkOBXvr4mtLMysgXYXD',
					  access_token_secret = 'WUVdcSK9ibXyudtXPaYznfKI0HTEb6IkvXrdASHel0bB3')

	# If the connection is successful, tweet the temperature
	if (api.VerifyCredentials().id):
		print 'API connection success'
		print 'tweeting: \'' + tweet + '\''

		if (api.PostUpdate(tweet)):
			print 'Temperature tweeted successfully'
		else:
			print 'Tweet Failed'
	else:
		print 'APIconnection failure'


#################################################


# Get the temperature
currentTemp = getTempReading()

# Save it to a dabase
saveToDb(currentTemp)

# Tweet the temperature
tweetTemperature(currentTemp)