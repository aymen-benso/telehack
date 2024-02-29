from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
# rest of your code

conn = sqlite3.connect('instance/my_database.db')

def add_complaint(conn, user_id, created_at, description, status, title):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO complaint (user_id, created_at, description, status, title) VALUES (?, ?, ?, ?, ?)', (user_id, created_at, description, status, title))
    conn.commit()
    return cursor.lastrowid


def response_complaint(complaint_id, response, responder_id , responded_at , status, response_description, response_username):
    cursor = conn.cursor()
    cursor.execute('UPDATE complaint SET response = ?, responder_id = ?, responded_at = ?, status = ?, response_description = ?, response_username = ? WHERE id = ?', (response, responder_id, responded_at, status, response_description, response_username, complaint_id))
    conn.commit()
    return cursor.lastrowid

def create_table():
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE complaint (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            created_at TEXT,
            description TEXT,
            status TEXT,
            response TEXT,
            responder_id INTEGER,
            responded_at TEXT,
            response_description TEXT,
            response_username TEXT
        )
    ''')
    conn.commit()
    return cursor.lastrowid

def edit_complaint(complaint_id, user_id, created_at, description, status):
    cursor = conn.cursor()
    cursor.execute('UPDATE complaint SET user_id = ?, created_at = ?, description = ?, status = ? WHERE id = ?', (user_id, created_at, description, status, complaint_id))
    conn.commit()
    return cursor.lastrowid

def get_all_complaints():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM complaint')
    return cursor.fetchall()

def get_complaint_by_id(complaint_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM complaint WHERE id = ?', (complaint_id,))
    return cursor.fetchone()


def delete_complaint(complaint_id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM complaint WHERE id = ?', (complaint_id,))
    conn.commit()
    return cursor.lastrowid


print(get_all_complaints())