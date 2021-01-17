import random

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class User(Base):

	__tablename__ = "user"
	id = sa.Column(sa.INTEGER, primary_key=True)
	first_name = sa.Column(sa.TEXT)
	last_name = sa.Column(sa.TEXT)
	gender = sa.Column(sa.TEXT)
	email = sa.Column(sa.TEXT)
	birthdate = sa.Column(sa.TEXT)
	height = sa.Column(sa.REAL)

engine = sa.create_engine(DB_PATH)
Sessions = sessionmaker(engine)
session = Sessions()
users = session.query(User).all()

found = False
user_id = int(input('Введите id: '))

for user in users:
	if user.id == user_id:
		user_search = session.query(User).filter(User.id == user_id).first()
		found = True

if found == False:
	print('id не найден')


if found == True:

	search = {}
	search_id = []

	for user in users:
		if user.id != user_id:
			search[user.id] = abs(user.height-user_search.height)

	for couple in search:
		if search[couple] == min(search.values()):
			search_id.append(couple)

	id_height = session.query(User).filter(User.id == random.choice(search_id)).first()
	print(str(id_height.id) + ' ' + id_height.first_name + ' ' + id_height.last_name + ' ' + str(id_height.height))

	search_years = {}
	search_months = {}
	search_days = {}


	for user in users:
		if user.id != user_id:
			date = user.birthdate.split('.')
			search_years[user.id] = abs(int(date[2])-int(user_search.birthdate.split('.')[2]))
			search_months[user.id] = abs(int(date[1])-int(user_search.birthdate.split('.')[1]))
			search_days[user.id] = abs(int(date[0])-int(user_search.birthdate.split('.')[0]))

	for year in search_years:
		if len(search_years) > 1:
			if min(search_years.values()) != search_years[year]:
				search_months.pop(year)
				search_days.pop(year)


	for month in search_months:
		if len(search_months) > 1:
			if min(search_months.values()) != search_months[month]:
				search_days.pop(month)
		else:
			id_birthdate = session.query(User).filter(User.id == month).first()
			print(str(id_birthdate.id) + ' ' + id_birthdate.first_name + ' ' + id_birthdate.last_name + ' ' + str(id_birthdate.birthdate))

	if len(search_days) > 1:
		day = random.choice(list(search_days.keys()))
		id_birthdate = session.query(User).filter(User.id == day).first()
		print(str(id_birthdate.id) + ' ' + id_birthdate.first_name + ' ' + id_birthdate.last_name + ' ' + str(id_birthdate.birthdate))