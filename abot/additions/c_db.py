import sqlite3

connection = sqlite3.connect('bot_data.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE region(
                   id INTEGER PRIMARY KEY,
                   name TEXT,
                   added_date TEXT
               )""")
connection.commit()

cursor.execute("""CREATE TABLE district(
                   id INTEGER PRIMARY KEY,
                   name TEXT,
                   region_id INTEGER,
                   added_date TEXT,
                   FOREIGN KEY (region_id) REFERENCES region(id)
               )""")
connection.commit()

cursor.execute("""CREATE TABLE skill(
                   id INTEGER PRIMARY KEY,
                   name TEXT,
                   added_date TEXT
               )""")
connection.commit()

cursor.execute("""CREATE TABLE admin_user(
                   id INTEGER PRIMARY KEY,
                   telegram_id TEXT,
                   joined_date TEXT
               )""")
connection.commit()

cursor.execute("""CREATE TABLE customer_user(
                   id INTEGER PRIMARY KEY,
                   telegram_id TEXT,
                   name TEXT,
                   phone_number TEXT,
                   telegram_username TEXT,  
                   joined_date TEXT
               )""")
connection.commit()

cursor.execute("""CREATE TABLE service_user(
                   id INTEGER PRIMARY KEY,
                   telegram_id TEXT,
                   name TEXT,
                   phone_number TEXT,
                   telegram_username TEXT,
                   description TEXT,
                   joined_date TEXT
               )""")
connection.commit()

cursor.execute("""CREATE TABLE service_skills(
                   id INTEGER PRIMARY KEY,
                   service_user_id INTEGER,
                   skill_id INTEGER,
                   FOREIGN KEY (service_user_id) REFERENCES service_user(id),
                   FOREIGN KEY (skill_id) REFERENCES skill(id)
               )""")

connection.commit()

cursor.execute("""CREATE TABLE service_districts(
                   id INTEGER PRIMARY KEY,
                   service_user_id INTEGER,
                   district_id INTEGER,
                   FOREIGN KEY (service_user_id) REFERENCES service_user(id),
                   FOREIGN KEY (district_id) REFERENCES district(id)
               )""")


connection.commit()
cursor.close()
connection.close()
