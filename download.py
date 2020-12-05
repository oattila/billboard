import datetime
import chartdates
import os
import constants
import requests
import time
import tools
import parse

def GetMissingDates():
	result = []

	for date in chartdates.dates:
		if (not os.path.isfile(tools.GetHtmlPath(date))):
			result.append(date)

	return result

def Download(date):
	url = constants.BILLBOARD_URL + str(date);
	print("Downloading chart " + str(date) + ": " + url)
	stuff = requests.get(url)

	if stuff.status_code != 200:
		print("Status: " + str(stuff.status_code))
		return False;

	path = tools.GetHtmlPath(date)
	
	with open(tools.GetHtmlPath(date), "w") as f:
		f.write(stuff.text)

	try:
		parse.Parse(str(date), True)
	except Exception as e:
		print("Parsing failed for " + path + ": " + str(e))
		#os.remove(path)

	return True;

def main():
	tools.EnsureDir(constants.HTML_DIR)

	missingDates = GetMissingDates()

	print(str(len(missingDates)) + " charts are missing")

	for date in missingDates:
		while not Download(date):
			print("Sleeping")
			time.sleep(60)

if __name__ == "__main__":
	main()