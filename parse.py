import os
import re
import enum

from . import chartdates
from . import constants
from . import tools
from . import chartdates

class Next(enum.Enum):
	RANK = 1
	SONG = 2
	ARTIST = 3

shitFinder = re.compile(r'^[\w ()/.,?!&+\'"\-òà¿#;:*=$%\[\]@]+$')

def Fix(str):
	str = str.replace("&#039;", "'")
	str = str.replace("`", "'")
	str = str.replace("&amp;", "&")
	str = str.replace("&quot;", '"')

	if not shitFinder.match(str):
		raise Exception("Shit found: " + str)

	return str

def Parse(week, test = False):
	filename = tools.GetHtmlPath(week)

	with open(filename, "r") as f: 
		lines = f.readlines()

	weekPattern = re.compile(r'.*data-chart-date="(\d\d\d\d-\d\d-\d\d)"');
	songPattern = re.compile(r'.*<span class="chart-element__information__song text--truncate color--primary">(.*)</span>')
	rankPattern = re.compile(r'.*<span class="chart-element__rank__number">(.*)</span>')
	artistPattern = re.compile(r'.*<span class="chart-element__information__artist text--truncate color--secondary">(.*)</span>')
	result = False;

	songs = []
	artists = []

	if not test:
		print("Parsing file " + filename)

	rank = 0
	next = Next.RANK

	for line in lines:
		r = weekPattern.match(line)

		if r:
			foundWeek = r.group(1);

			if (foundWeek == "1976-07-04"):
				foundWeek = "1976-07-03" # bug in billboard

			if foundWeek != week:
				raise Exception("Found wrong week: " + foundWeek)

		r = rankPattern.match(line)

		if r:
			s = r.group(1);
			i = int(s)

			if i <= 0 or i > 100:
				raise Exception("Invalid rank: " + s)

			if next != Next.RANK:
				raise Exception("Didn't expect a rank! Encountered rank: " + str(i))

			if i != rank + 1:
				raise Exception("Got rank " + str(i) + " while expecting rank " + str(rank + 1))

			rank = i
			next = Next.SONG

		r = songPattern.match(line)

		if r:
			if next != Next.SONG:
				raise Exception("Didn't expect song, got: " + r.group(1))

			songs.append(r.group(1))
			next = Next.ARTIST

		r = artistPattern.match(line)

		if r:
			if next != Next.ARTIST:
				raise Exception("Didn't expect artist, got: " + r.group(1))

			artists.append(r.group(1))
			next = Next.RANK

	if not foundWeek:
		raise Exception("Found no week at all")

	if len(songs) != 100:
		raise Exception("Wrong number of songs: " + str(len(songs)))

	if len(artists) != 100:
		raise Exception("Wrong number of artists: " + str(len(artists)))		

	if test:
		return

	for i in range(0, 100):
		artists[i] = Fix(artists[i])
		songs[i] = Fix(songs[i])

	with open(tools.GetTxtPath(week), "w") as f : 
		for i in range(0, 100):
			f.write(str(i + 1) + "\n")
			f.write(artists[i] + "\n")
			f.write(songs[i] + "\n")
	
def main():
	htmls = tools.GetAll(constants.HTML_DIR, "(\d\d\d\d-\d\d-\d\d).html")

	if not htmls:
		print("No htmls")
		return;

	tools.EnsureDir(constants.TXT_DIR)
	txts = tools.GetAll(constants.TXT_DIR, "(\d\d\d\d-\d\d-\d\d).txt")
	toParse = htmls.difference(txts)

	print(str(len(toParse)) + " new htmls to parse")

	for date in toParse:
		if not os.path.isfile(tools.GetTxtPath(date)):
			Parse(date)

if __name__ == "__main__":
	main()