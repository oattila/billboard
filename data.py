import datetime
import sys
import random

from . import tools
from . import constants

def MakeId(artist, song):
	return artist + song

class Song:
	def __init__(self, artist, song):
		self.name = song
		self.artist = artist
		self.id = MakeId(artist, song)
		self.top = 0
		self.topWeek = None

	def __str__(self):
		return f'{self.artist}: {self.name} ({self.top}. {self.topWeek})'

class Database:
	def __init__(self):
		self.songs = {}

		for filename in tools.GetAll(constants.TXT_DIR, "(\d\d\d\d-\d\d-\d\d.txt)"):
			week = datetime.date.fromisoformat(filename.removesuffix(".txt"))
			filename = constants.TXT_DIR + "/" + filename

			with open(filename, "r") as f:
				while True:
					if not (rankStr := f.readline()):
						break;

					rank = int(rankStr)
					artist = f.readline().strip("\n")
					song = f.readline().strip("\n")
					self.Register(artist, song, rank, week)

	def Register(self, artist, song, rank, week):
		id = MakeId(artist, song)
		p = self.songs.get(id)

		if not p:
			p = Song(artist, song)
			self.songs[id] = p

		if not p.top or rank <= p.top:
			if not p.topWeek or rank < p.top:
				p.topWeek = week

			if p.topWeek and rank == p.top and week < p.topWeek:
				p.topWeek = week

			p.top = rank

	def GetRandomSong(self):
		return random.choice(list(self.songs.values()))

def MakePeakFile(db, rank, pretty):
	suffix = "" if pretty else "_raw"
	filename = constants.PEAK_DIR + "/" + str(rank) + suffix + ".txt"

	with open(filename, "w") as f: 
		list = []

		for song in db.songs.values():
			if song.top == rank:
				list.append(song)

		list.sort(key = lambda song: song.topWeek)

		if pretty:
			f.write("Hot 100 Songs with peak position = " + str(rank) + ", total " + str(len(list)) + " songs\n")

		i = 0
		year = 0

		for song in list:
			if song.topWeek.year != year:
				year = song.topWeek.year

				if pretty:
					f.write("\n" + str(year) + "\n\n")

			i = i + 1

			if pretty:
				f.write(str(i) + ". " + song.artist + ": " + song.name + "\n")
			else:
				f.write(song.artist + "\n" + song.name +"\n")

		return len(list)

def main():
	db = Database()

	with open(constants.PEAK_DIR + "/counts.txt", "w") as f:
		for i in range(1, 101):
			count = MakePeakFile(db, i, False)
			count = MakePeakFile(db, i, True)
			f.write(str(count) + "\n")

if __name__ == "__main__":
	main()


