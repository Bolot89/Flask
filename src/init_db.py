import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            ('Artem', 'email@mail.ru', '12345')
            )

connection.commit()
connection.close()