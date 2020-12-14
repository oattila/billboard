import datetime
from . import constants

MONDAY = 0
SATURDAY = 5

def GetLatestChartDate():
	now = datetime.date.today()

	while (now.weekday() != SATURDAY):
		now = now + datetime.timedelta(days = 1)

	return now

def GetAllChartDates():
	result = [];
	date = constants.FIRST_CHART_DATE 
	assert date.weekday() == MONDAY

	while (date <= GetLatestChartDate()):
		if (date == datetime.date(1962, 1, 1)):
			date = datetime.date(1962, 1, 6)

		assert date.weekday() == (MONDAY if date.year < 1962 else SATURDAY)

		result.append(date);
		date = date + datetime.timedelta(days = 7);

	return result

def MakeDateIndexes():
	result = {}
	index = 0;
	for date in dates:
		result[date] = index
		index = index + 1
	return result

dates = GetAllChartDates();
dateIndexes = MakeDateIndexes();

def GetDate(index):
	return dates[index]

def GetIndex(date):
	return dateIndexes[date]