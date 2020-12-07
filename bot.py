# -*- encoding: utf-8 -*-

from telebot import TeleBot, types
import sqlite3
  
bot = TeleBot(*)


 
@bot.message_handler(commands=['start']) #Запрос локации
def request_location(message):
    
	bot.send_message(message.chat.id, "Добавить категорию /add \n Добавить канал откуда парсить /from_add \n Добавить канал куда вставлять /to_add")




#Category operations

@bot.message_handler(regexp="DEL_C")
def handle_message(message):
	
	conn = sqlite3.connect("db.sqlite3") 
	cursor = conn.cursor()
	cursor.execute('DELETE FROM category WHERE name=?', (message.text[6:],))
	conn.commit()
	cursor.execute('DELETE FROM channels WHERE category=?', (message.text[6:],))
	conn.commit()
	cursor.execute('DELETE FROM toPars WHERE category=?', (message.text[6:],))
	conn.commit()
	bot.send_message(message.chat.id, 'Удалено')

@bot.message_handler(regexp="ADD_C")
def handle_message(message):
	
	conn = sqlite3.connect("db.sqlite3") 
	cursor = conn.cursor()
	cursor.execute('INSERT INTO category(id,name) VALUES(?,?)', (None,message.text[6:]))
	conn.commit()
	bot.send_message(message.chat.id, 'Добавлено')


@bot.message_handler(regexp="LIS_C")
def handle_message(message):
	conn = sqlite3.connect("db.sqlite3") 
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM category")
	rows = cursor.fetchall()
	final = ''
	for row in rows:
		final += str(row[1])+'\n'
	bot.send_message(message.chat.id, 'Cписок всех  категорий: \n'+final)
#Category operations




#from operations

@bot.message_handler(regexp="ADD_F")
def handle_message(message):
	
	conn = sqlite3.connect("db.sqlite3") 
	cursor = conn.cursor()
	

	cursor.execute("SELECT * FROM category WHERE name like '%"+message.text[6:].split('\\')[1]+"%'")
	rows = cursor.fetchall()
	if len(rows) != 0:
		
		cursor.execute('INSERT INTO channels(id,name,category) VALUES(?,?,?)', (None,message.text[6:].split('\\')[0],message.text[6:].split('\\')[1]))
		conn.commit()
		bot.send_message(message.chat.id, 'Добавлено')
	else:
		bot.send_message(message.chat.id, 'Такой категории нет')

@bot.message_handler(regexp="DEL_F")
def handle_message(message):
	
	conn = sqlite3.connect("db.sqlite3") 
	cursor = conn.cursor()
	cursor.execute('DELETE FROM channels WHERE name=?', (message.text[6:],))
	conn.commit()
	bot.send_message(message.chat.id, 'Удалено')

@bot.message_handler(regexp="LIS_F")
def handle_message(message):
	conn = sqlite3.connect("db.sqlite3") 
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM channels")
	rows = cursor.fetchall()
	final = ''
	for row in rows:
		final += 'Имя:'+str(row[1])+'  \\  Категория:'+str(row[2])+'\n'
	bot.send_message(message.chat.id, 'Cписок откуда парсить вместе с категориями: \n'+final)

#from operations


#To operations
@bot.message_handler(regexp="ADD_T")
def handle_message(message):
	
	conn = sqlite3.connect("db.sqlite3") 
	cursor = conn.cursor()
	

	cursor.execute("SELECT * FROM category WHERE name like '%"+message.text[6:].split('\\')[1]+"%'")
	rows = cursor.fetchall()
	if len(rows) != 0:
		
		cursor.execute('INSERT INTO toPars(id,name,category) VALUES(?,?,?)', (None,message.text[6:].split('\\')[0],message.text[6:].split('\\')[1]))
		conn.commit()
		bot.send_message(message.chat.id, 'Добавлено')
	else:
		bot.send_message(message.chat.id, 'Такой категории нет')

@bot.message_handler(regexp="DEL_T")
def handle_message(message):
	
	conn = sqlite3.connect("db.sqlite3") 
	cursor = conn.cursor()
	cursor.execute('DELETE FROM toPars WHERE name=?', (message.text[6:],))
	conn.commit()
	bot.send_message(message.chat.id, 'Удалено')

@bot.message_handler(regexp="LIS_T")
def handle_message(message):
	conn = sqlite3.connect("db.sqlite3") 
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM toPars")
	rows = cursor.fetchall()
	final = ''
	for row in rows:
		final += 'Имя:'+str(row[1])+'  \\  Категория:'+str(row[2])+'\n'
	bot.send_message(message.chat.id, 'Cписок куда постить вместе с категориями: \n'+final)

#To operations




@bot.message_handler(commands=['add']) 
def request_location(message):
	bot.send_message(message.chat.id, "ADD_C <имя категории> - добавление категории \n DEL_C <имя категории> - удаление категории \n LIS_C  - список всех категорий")
	
	

@bot.message_handler(commands=['from_add']) #Запрос локации
def request_location(message):
		bot.send_message(message.chat.id, "ADD_F <имя канала>\\<имя категории> - добавление откуда парсить \n DEL_F <имя канала> - удаление источника \n LIS_F  - список всех источников")




@bot.message_handler(commands=['to_add']) #Запрос локации
def request_location(message):
	bot.send_message(message.chat.id, "ADD_T <имя канала>\\<имя категории> - добавление куда постить  \n DEL_T <имя канала> - удаление куда постить  \n LIS_T  - список куда постить ")

if __name__ == "__main__":
    bot.polling()


