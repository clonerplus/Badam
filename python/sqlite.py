import datetime
import sqlite3

from python.Message import Message

conn = sqlite3.connect('../chatroom.db')

cursor = conn.cursor()

create_table_sql = '''
CREATE TABLE IF NOT EXISTS chatroom (
    msg_id INTEGER PRIMARY KEY,
    order_num INTEGER,
    sender_id INTEGER,
    body TEXT,
    send_time DATETIME
);
'''
cursor.execute(create_table_sql)

message = Message(1, 12345, "This is the body text.", datetime.datetime.now())

insert_sql = '''
INSERT INTO chatroom (order_num, sender_id, body, send_time)
VALUES (?, ?, ?, ?);
'''

message_data = (message.order_num, message.sender_id, message.body, message.send_time)
cursor.execute(insert_sql, message_data)

conn.commit()
conn.close()
