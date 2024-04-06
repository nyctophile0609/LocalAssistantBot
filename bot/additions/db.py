import sqlite3
from datetime import datetime
from .cyberpunks import *
db_path='additions/bot_data.db'
#############################################################################################
#######################################################################################

#############################################################################################
# REGION

def create_region_object(name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        added_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO region (name, added_date)
            VALUES (?, ?)
        """, (name, added_date))

        conn.commit()

        return True
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_all_regions():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM region ORDER BY added_date ASC;")
        regions = cursor.fetchall()
        return regions
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        cursor.close()
        conn.close()

def get_the_region(region_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM region where id = {region_id}")
        region = cursor.fetchone()
        return region
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        cursor.close()
        conn.close()

#############################################################################################
# DISTRICT

def create_district_object(name, region_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        added_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO district (name, region_id, added_date)
            VALUES (?, ?, ?)""", (name, region_id, added_date))

        conn.commit()

        return True
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def get_all_districts(region_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM district WHERE region_id = '{region_id}';")
        districts = cursor.fetchall()
        return districts
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        cursor.close()
        conn.close()

def get_the_district(district_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM district WHERE id = {district_id};")
        district = cursor.fetchall()
        return district[0]
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        cursor.close()
        conn.close()

#############################################################################################
# SKILL

def create_skill_object(name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        added_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO skill (name, added_date)
            VALUES (?, ?)
        """, (name, added_date))

        conn.commit()

        return True
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_all_skills():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM skill")
        skills = cursor.fetchall()
        return skills
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        cursor.close()
        conn.close()

def get_the_skill(skill_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM skill WHERE id = {skill_id};")
        skill = cursor.fetchall()
        return skill[0]
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        cursor.close()
        conn.close()

#############################################################################################
# SERVICE

def create_service_object(telegram_id, name, phone_number, telegram_username, description, skills_ids, districts_ids):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM service_user WHERE telegram_id = ? or phone_number = ? ",
                       (telegram_id, phone_number))
        service_user = cursor.fetchone()
        service_user_id = 0
        if service_user:
            service_user_id = service_user[0]
            cursor.execute("""UPDATE service_user SET name = ?, telegram_id = ?, phone_number = ?,
                            telegram_username = ?, description = ? WHERE id = ?""",
                           (name, telegram_id, phone_number, telegram_username, description, service_user_id))
            for skill_id in skills_ids:
                cursor.execute("DELETE FROM service_skills WHERE service_user_id = ? AND skill_id = ?",
                               (service_user_id, skill_id))
            
            for district_id in districts_ids:
                cursor.execute("DELETE FROM service_districts WHERE service_user_id = ? AND district_id = ?",
                               (service_user_id, district_id))

        else:
            cursor.execute("""INSERT INTO service_user (telegram_id, name, phone_number, telegram_username, description) VALUES (?, ?, ?, ?, ?)""",
                           (telegram_id, name, phone_number, telegram_username, description))
            service_user_id = cursor.lastrowid
        for skill_id in skills_ids:

            cursor.execute("INSERT INTO service_skills (service_user_id, skill_id) VALUES (?, ?)",
                           (service_user_id, skill_id))

        for district_id in districts_ids:
            cursor.execute("INSERT INTO service_districts (service_user_id, district_id) VALUES (?, ?)",
                           (service_user_id, district_id))
        
        conn.commit()
        return True

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        cursor.close()
        conn.close()



def get_all_services(district_id, skills):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:

        cursor.execute("SELECT service_user_id FROM service_districts WHERE district_id = ?", (district_id,))
        d_users = cursor.fetchall()
        s_users = []
        for skill_id in skills:
            cursor.execute("SELECT service_user_id FROM service_skills WHERE skill_id = ?", (skill_id[0],))
            user_ids = cursor.fetchall()
            if user_ids:
                s_users.append(set(user_ids))
        if s_users:
            intersected_users = s_users[0]
            for user_set in s_users:
                intersected_users=intersected_users & user_set

            service_ids = intersected_users & set(d_users)
            services = []
            for service_id in service_ids:
                cursor.execute("SELECT * FROM service_user WHERE id = ?", (service_id[0],))
                service = cursor.fetchone()
                if service:
                    services.append(service)
            return services
        else:
            return []
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def get_the_service(service_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT * FROM service_user WHERE id = {service_id}")
        user = cursor.fetchone()
        cursor.execute(f"SELECT skill_id FROM service_skills WHERE service_user_id = {service_id}")
        skill_ids = cursor.fetchall()
        cursor.execute(f"SELECT district_id FROM service_districts WHERE service_user_id = {service_id}")
        district_ids = cursor.fetchall()
        skills=[]
        districts=[]
        for i in skill_ids:
            cursor.execute(f"SELECT * FROM skill WHERE id = {i[0]}")
            x=cursor.fetchone()
            if x:
                skills.append(x)
        for i in district_ids:
            cursor.execute(f"SELECT * FROM district WHERE id = {i[0]}")
            x=cursor.fetchone()
            if x:
                districts.append(x)

        return [user, skills, districts]
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        cursor.close()
        conn.close()

#############################################################################################
# CUSTOMER
 
def create_customer_object(telegram_id, name, phone_number, telegram_username):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id FROM customer_user WHERE telegram_id = ? OR phone_number = ?
        """, (telegram_id, phone_number))
        existing_customer_user = cursor.fetchone()
        if existing_customer_user:
            cursor.execute("""
                UPDATE customer_user SET name = ?, phone_number = ?, telegram_username = ?
                WHERE id = ?
            """, (name, phone_number, telegram_username, existing_customer_user[0]))
            return True
        else:
            joined_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
                INSERT INTO customer_user (telegram_id, name, phone_number, telegram_username, joined_date)
                VALUES (?, ?, ?, ?, ?)
            """, (telegram_id, name, phone_number, telegram_username, joined_date))



        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        cursor.close()
        conn.close()

#############################################################################################
# USER

def get_the_user_info(telegram_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT * FROM admin_user WHERE telegram_id = "{telegram_id}"')
        result = cursor.fetchone()
        if result is not None:
            return [0, make_dict([0, result])]
        
        cursor.execute(f'SELECT * FROM service_user WHERE telegram_id = "{telegram_id}"')
        result = cursor.fetchone()
        if result is not None:
            return [1, make_dict([1, result])]

        cursor.execute(f'SELECT * FROM customer_user WHERE telegram_id = "{telegram_id}"')
        result = cursor.fetchone()
        if result is not None:
            return [2, make_dict([2, result])]
        
        return None
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        cursor.close()
        conn.close()



#############################################################################################
# DELETE

def delete_user(telegram_id, phone_number, data):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        if data == "service":
            cursor.execute("""
                    SELECT id FROM service_user WHERE telegram_id = ? OR phone_number = ?
                """, (telegram_id, phone_number))
            existing_service_user = cursor.fetchone()
            if existing_service_user:
                cursor.execute("DELETE FROM service_user WHERE telegram_id = ? OR phone_number = ?",
                               (telegram_id, phone_number))
                cursor.execute("DELETE FROM service_skills WHERE service_user_id = ?",
                               (existing_service_user[0],))
                cursor.execute("DELETE FROM service_districts WHERE service_user_id = ?",
                               (existing_service_user[0],))
        elif data == "customer":
            cursor.execute("""
                DELETE FROM customer_user WHERE telegram_id = ? OR phone_number = ?
            """, (telegram_id, phone_number))
        conn.commit()

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        cursor.close()
        conn.close()


#############################################################################################
# END
