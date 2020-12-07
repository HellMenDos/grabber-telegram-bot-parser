# -*- encoding: utf-8 -*-

import configparser
import json
import time
import requests
from telethon.sync import TelegramClient
from telethon import connection

# для корректного переноса времени сообщений в json
from datetime import date, datetime

# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest
import sqlite3



# Присваиваем значения внутренним переменным
api_id   = *
api_hash = *
username = *
api_token = *


client = TelegramClient(username, api_id, api_hash)

client.start()



	


async def dump_all_messages(channel):

	offset_msg = 0    # номер записи, с которой начинается считывание
	limit_msg = 1 # максимальное число записей, передаваемых за один раз

	all_messages = []   # список всех сообщений
	total_messages = 0
	total_count_limit = 1  # поменяйте это значение, если вам нужны не все сообщения

	while True:
		history = await client(GetHistoryRequest(
			peer=channel,
			offset_id=offset_msg,
			offset_date=None, add_offset=0,
			limit=limit_msg, max_id=0, min_id=0,
			hash=0))
		if not history.messages:
			break
		messages = history.messages
		for message in messages:
			all_messages.append(message.to_dict())
		offset_msg = messages[len(messages) - 1].id
		total_messages = len(all_messages)
		if total_count_limit != 0 and total_messages >= total_count_limit:
			break

	return all_messages[0]
	

async def main():
		while True:
			conn = sqlite3.connect("db.sqlite3")
			cursor = conn.cursor()
			cursor.execute("SELECT * FROM channels")
			entitys = cursor.fetchall()
			time.sleep(2500)
			
			
			for entity in entitys:
				print(entity)
				channel = await client.get_entity(entity[1])
				# client.send_message('gamee', "hi", file='Untitled-1.jpg')
				f = await dump_all_messages(channel)
				#делаем селект по id ит проверям совбадае ли, если совпадает ничего не делаем, если совпадает 
				print(f)
				conn = sqlite3.connect("db.sqlite3") 

				cursor = conn.cursor()
				cursor.execute("SELECT * FROM last_mess WHERE from_id like '%"+str(f['to_id']['channel_id'])+"%'" )
				rows2 = cursor.fetchall()
				if len(rows2) == 0:
					conn = sqlite3.connect("db.sqlite3")
					cursor = conn.cursor()
					cursor.execute('INSERT INTO last_mess(id,id_of_mess,from_id,mess,url,category) VALUES(?,?,?,?,?,?)', (None,str(f['id']),str(f['to_id']['channel_id']),str(f['message']),str(f['media']),entity[2] ))
					conn.commit()
					conn = sqlite3.connect("db.sqlite3")
					cursor = conn.cursor()
					cursor.execute("SELECT * FROM toPars WHERE category like '%"+str(entity[2])+"%'" )
					toPars = cursor.fetchall()
					for toPar in toPars: requests.get('https://api.telegram.org/bot{}/sendMessage'.format(api_token), params=dict(chat_id=str('@'+str(toPar[1].split('https://t.me/')[1])),text=f['message']))

				else:
					if str(rows2[0][1]) != str(f['id']):
						conn = sqlite3.connect("db.sqlite3")
						cursor = conn.cursor()
						cursor.execute('DELETE FROM last_mess WHERE id_of_mess=?', (str(rows2[0][1]),))
						conn.commit()
						time.sleep(1)
						conn = sqlite3.connect("db.sqlite3")
						cursor = conn.cursor()
						cursor.execute('INSERT INTO last_mess(id,id_of_mess,from_id,mess,url,category) VALUES(?,?,?,?,?,?)', (None,str(f['id']),str(f['to_id']['channel_id']),str(f['message']),str(f['media']),entity[2] ))
						conn.commit()
						conn = sqlite3.connect("db.sqlite3")
						cursor = conn.cursor()
						cursor.execute("SELECT * FROM toPars WHERE category like '%"+str(entity[2])+"%'" )
						toPars = cursor.fetchall()
						for toPar in toPars: requests.get('https://api.telegram.org/bot{}/sendMessage'.format(api_token), params=dict(chat_id=str('@'+str(toPar[1].split('https://t.me/')[1])),text=f['message']))

with client:
	client.loop.run_until_complete(main())
				