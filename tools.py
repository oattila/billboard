import os
import re
from . import constants

def GetDir():
	result = os.path.dirname(os.path.realpath(__file__))
	return result

print(GetDir())

def GetHtmlPath(week):
	return constants.HTML_DIR + "/" + str(week) + ".html"

def GetTxtPath(week):
	return constants.TXT_DIR + "/" + str(week) + ".txt"

def EnsureDir(dir):
	if (not os.path.isdir(dir)):
		os.makedirs(dir)

def GetAll(dir, regex):
	result = set()
	pattern = re.compile(regex)

	for f in os.listdir(dir):
		match = pattern.match(f)
		
		if (match):
			groups = match.groups()

			if (len(groups) > 0):
				result.add(groups[0])
			else:
				result.add(f)

	return result