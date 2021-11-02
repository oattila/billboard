import sys
import re
from . import data

rx = re.compile("([^\w ]|_)")

def Fix(name):
	name = re.sub("\(.*?\)", "", name)
	name = re.sub(" feat.*", "", name, flags = re.IGNORECASE)

	name = re.sub(" starring.*", "", name, flags = re.IGNORECASE)
	name = re.sub(" duet with .*", "", name, flags = re.IGNORECASE)		
	name = re.sub(" with .*", "", name, flags = re.IGNORECASE)		
	name = re.sub(" and the .*", "", name, flags = re.IGNORECASE)		
	name = re.sub(" and his .*", "", name, flags = re.IGNORECASE)

	name = re.sub(" and .*", "", name, flags = re.IGNORECASE)

	name = re.sub("\/.*", "", name, flags = re.IGNORECASE)

	name = re.sub("&.*", "", name, flags = re.IGNORECASE)
	name = re.sub(" x .*", "", name, flags = re.IGNORECASE)

	name = re.sub("the ", "", name, flags = re.IGNORECASE)

	name = rx.sub(' ', name)
	name = name.rstrip().lstrip()

	return name

def main():
	db = data.Database()

	seen = set()
	once = {}

	for song in db.songs.values():
		artist = Fix(song.artist)

		if artist in seen:
			if artist in once:
				once.pop(artist)
			continue

		seen.add(artist)

		if song.top < 11:
			once[artist] = f'{song.artist}: {song.name}'

	for s in once.values():
		print(s)

if __name__ == "__main__":
	main()

