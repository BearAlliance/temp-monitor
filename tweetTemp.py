import twitter
import datetime
import time
from RPi import GPIO


# Saves the temperature to a database for fun graphs later
def saveToDb(temp):
	# no DB yet
	return

# Returns formated dat time string
# Ex: '01/12 4:40PM'
def getDateTimeString():
	now = datetime.datetime.now()
	return now.strftime('%m/%d %-I:%M%p')

# Tweets the given temperature
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


# Temperature reading
#################################################

def bin2dec(string_num):
    return str(int(string_num, 2))

def cTof(cTemp):
	return str((float(cTemp) * 1.8) + 32)


def readTemp():
	data = []

	GPIO.setmode(GPIO.BCM)

	GPIO.setup(4,GPIO.OUT)
	GPIO.output(4,GPIO.HIGH)
	time.sleep(0.025)
	GPIO.output(4,GPIO.LOW)
	time.sleep(0.02)

	GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	for i in range(0,500):
	    data.append(GPIO.input(4))

	bit_count = 0
	tmp = 0
	count = 0
	HumidityBit = ""
	TemperatureBit = ""
	crc = ""

	try:
		while data[count] == 1:
			tmp = 1
			count = count + 1

		for i in range(0, 32):
			bit_count = 0

			while data[count] == 0:
				tmp = 1
				count = count + 1

			while data[count] == 1:
				bit_count = bit_count + 1
				count = count + 1

			if bit_count > 3:
				if i>=0 and i<8:
					HumidityBit = HumidityBit + "1"
				if i>=16 and i<24:
					TemperatureBit = TemperatureBit + "1"
			else:
				if i>=0 and i<8:
					HumidityBit = HumidityBit + "0"
				if i>=16 and i<24:
					TemperatureBit = TemperatureBit + "0"

	except:
		print "ERR_RANGE"
		return "Error"

	try:
		for i in range(0, 8):
			bit_count = 0

			while data[count] == 0:
				tmp = 1
				count = count + 1

			while data[count] == 1:
				bit_count = bit_count + 1
				count = count + 1

			if bit_count > 3:
				crc = crc + "1"
			else:
				crc = crc + "0"
	except:
		print "ERR_RANGE"
		return "Error"

	Humidity = bin2dec(HumidityBit)
	Temperature = bin2dec(TemperatureBit)

	if int(Humidity) + int(Temperature) - int(bin2dec(crc)) == 0:
		# print "Humidity:"+ Humidity +"%"
		# print "Temperature:"+ Temperature +"C"
		fTemp = cTof(Temperature)
		# print "Temperature:"+ fTemp +"F"
		return fTemp
	else:
		print "ERR_CRC"
		return "Error"

# Returns temperature reading as a string
# Hit sensor again if error is returned
def getTempReading():
	result = readTemp()
	while(result == "Error"):
		result = readTemp()
	
	return result


#################################################


# Get the temperature
currentTemp = getTempReading()
# print "Temperature: " + currentTemp + "F"

# Save it to a dabase
saveToDb(currentTemp)

# Tweet the temperature
tweetTemperature(currentTemp)