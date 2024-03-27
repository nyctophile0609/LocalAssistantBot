import sqlite3
from datetime import datetime
from messed_up import *
db_path='../db.sqlite3'



def get_the_user_info(telegram_id: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    data ={}
    try:
        cursor.execute(f'SELECT * FROM main_admin WHERE telegram_id = "{telegram_id}"')
        result = cursor.fetchone()
        if result==None:
            cursor.execute(f'SELECT * FROM main_service WHERE telegram_id = "{telegram_id}"')
            result = cursor.fetchone()           
            if result == None:
                cursor.execute(f'SELECT * FROM main_customer WHERE telegram_id = "{telegram_id}"')
                result = cursor.fetchone()
                if result ==None:
                    return None
                else:
                    return [2,make_dict([2,result])] 
            else:
                return [1,make_dict([2,result])] 
        else:
            return [0,make_dict([2,result])] 


    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        cursor.close()
        conn.close()

def check_the_user_status(telegram_id: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    data ={}
    try:
        cursor.execute(f'SELECT * FROM main_admin WHERE telegram_id = "{telegram_id}"')
        result = cursor.fetchone()
        if result==None:
            cursor.execute(f'SELECT * FROM main_service WHERE telegram_id = "{telegram_id}"')
            result = cursor.fetchone()           
            if result == None:
                cursor.execute(f'SELECT * FROM main_customer WHERE telegram_id = "{telegram_id}"')
                result = cursor.fetchone()
                if result ==None:
                    return None
                else:
                    return make_dict("customer") 
            else:
                return make_dict("service") 
        else:
            return make_dict("admin") 


    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        cursor.close()
        conn.close()


def get_all_regions():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM main_region ORDER BY added_date ASC;")
        regions = cursor.fetchall()
        return regions
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        cursor.close()
        conn.close()

def get_all_districts(region_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM main_district WHERE region_id = '{region_id}';")
        districts = cursor.fetchall()
        return districts
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        cursor.close()
        conn.close()

def get_all_skills():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM main_skill")
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
        cursor.execute(f"SELECT * FROM main_skill WHERE id = {skill_id};")
        skill = cursor.fetchall()
        return skill[0]
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        cursor.close()
        conn.close()


import sqlite3

def get_the_masters(region_id, district_id, skills):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        skill_ids = [skill[0] for skill in skills]
        skill_placeholders = ','.join(['?' for _ in skill_ids])
        query = f"""
            SELECT DISTINCT s.id, s.name
            FROM main_service AS s
            INNER JOIN main_service_skills AS ss ON s.id = ss.service_id
            INNER JOIN main_service_districts AS sd ON s.id = sd.service_id
            WHERE s.region_id = ?
              AND sd.district_id = ?
              AND ss.skill_id IN ({skill_placeholders})
            GROUP BY s.id, s.name
            HAVING COUNT(DISTINCT ss.skill_id) = ?
        """

        flat_skill_ids = tuple(skill_ids)
        cursor.execute(query, [region_id, district_id] + list(flat_skill_ids) + [len(flat_skill_ids)])
        services = cursor.fetchall()
        return services
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        cursor.close()
        conn.close()


def get_the_service(service_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        query = """
        SELECT 
            main_service.id AS service_id,
            main_service.name AS service_name,
            main_service.telegram_id AS service_telegram_id,
            main_service.number AS service_number,
            main_service.telegram_username AS service_telegram_username,
            main_service.description AS service_description,
            main_service.joined_date AS service_joined_date,
            main_region.id AS region_id,
            main_region.name AS region_name,
            main_region.added_date AS region_added_date,
            (
                SELECT 
                    GROUP_CONCAT(main_district.id || ',' || main_district.name || ',' || main_district.added_date)
                FROM 
                    main_service_districts
                JOIN 
                    main_district ON main_service_districts.district_id = main_district.id
                WHERE 
                    main_service_districts.service_id = main_service.id
            ) AS district_info,
            (
                SELECT 
                    GROUP_CONCAT(main_skill.id || ',' || main_skill.name || ',' || main_skill.added_date)
                FROM 
                    main_service_skills
                JOIN 
                    main_skill ON main_service_skills.skill_id = main_skill.id
                WHERE 
                    main_service_skills.service_id = main_service.id
            ) AS skill_info
        FROM 
            main_service
        JOIN 
            main_region ON main_service.region_id = main_region.id
        WHERE 
            main_service.id = ?;
        """
        cursor.execute(query, (service_id,))
        rows = cursor.fetchall()
        return format_the_data(rows[0])
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        cursor.close()
        conn.close()

