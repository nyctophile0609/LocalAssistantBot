import sqlite3
from datetime import datetime
db_path='bot_data.db'

def add_admin(telegram_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        joined_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO admin_user(telegram_id, joined_date) VALUES (?,?)",
                       (telegram_id,joined_date))

        conn.commit()
        return True
    except sqlite3.Error as e:
        return f"SQLite error: {e}"
    finally:
        cursor.close()
        conn.close()

id=input("Input telegram_id:\n")
print(add_admin(id))
# def hhh(district_id, skills):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     try:
#         cursor.execute("SELECT service_user_id FROM service_districts WHERE district_id = ?", (district_id,))
#         d_users = cursor.fetchall()
#         s_users = []
#         for skill in skills:
#             cursor.execute("SELECT service_user_id FROM service_skills WHERE skill_id = ?", (skill,))
#             user_ids = cursor.fetchall()
#             if user_ids:
#                 s_users.append(set(user_ids))
#         y=s_users[0]
#         for i in range(len(s_users)):
#             y=y&s_users[i]
#         service_id= y&set(d_users)
#         services=[]
#         for i in list(service_id):
#             cursor.execute(f"SELECT * FROM service_user WHERE id = {i[0]}")
#             x=cursor.fetchone()
#             if x:
#                 services.append(x)
#                 print(x)
#         return services
        
#     except sqlite3.Error as e:
#         return f"SQLite error: {e}"
#     finally:
#         cursor.close()
#         conn.close()

# print(hhh(2, [1, 2, 3]))
