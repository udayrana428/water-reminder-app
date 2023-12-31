
# database.py
import mysql.connector
import json
import os
from tkinter import messagebox

# Read configuration from JSON
def read_config_from_json(file_name):
    script_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_directory, file_name)

    with open(file_path, 'r') as file:
        config_data = json.load(file)

    return config_data
config_data = read_config_from_json('hydration_goals.json')


# Constants
DATABASE_HOST = config_data['mysql_data']['HOST']
DATABASE_USER = config_data['mysql_data']['USER']
DATABASE_PASSWORD = config_data['mysql_data']['PASSWORD']
DATABASE_NAME = config_data['mysql_data']['NAME']

# Initialize the database (create tables if not exist)
def initialize_database():
    connection = mysql.connector.connect(
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database=DATABASE_NAME
    )
    cursor = connection.cursor()

    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                goal INT NOT NULL,
                age INT,
                weight FLOAT,
                height FLOAT
            )
        ''')
        print("Database connected")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        connection.commit()
        connection.close()

# Save user profile to the database
def save_user_profile(username, email, password, goal, age, height, weight):
    connection = mysql.connector.connect(
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database=DATABASE_NAME
    )
    cursor = connection.cursor()

    try:
        cursor.execute('''
            INSERT INTO users (username, email, password, goal, age, height, weight)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (username, email, password, goal, age, height, weight))

        print("User added")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        connection.commit()
        connection.close()

# Update user profile in the database
def update_user_profile(username, new_goal=None,new_username=None,new_password=None,new_age=None, new_email=None, new_weight=None, new_height=None):
    connection = mysql.connector.connect(
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database=DATABASE_NAME
    )
    cursor = connection.cursor()

    try:
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user_profile = cursor.fetchone()

        if user_profile:
            if new_username is not None:
                cursor.execute("UPDATE users SET username = %s WHERE username = %s;", (new_username, username))
                connection.commit()
                messagebox.showinfo("Update", "Username updated!")
            elif new_email is not None:
                cursor.execute("UPDATE users SET email = %s WHERE username = %s;", (new_email, username))
                connection.commit()
                messagebox.showinfo("Update", "Email updated!")
            elif new_password is not None:
                cursor.execute("UPDATE users SET password = %s WHERE username = %s;", (new_password, username))
                connection.commit()
                messagebox.showinfo("Update", "Password updated!")
            elif new_goal is not None:
                cursor.execute("UPDATE users SET goal = %s WHERE username = %s;", (new_goal, username))
                connection.commit()
                messagebox.showinfo("Update", "Goal updated!")
            elif new_age is not None:
                cursor.execute("UPDATE users SET age = %s WHERE username = %s;", (new_age, username))
                connection.commit()
                messagebox.showinfo("Update", "Age updated!")
            elif new_height is not None:
                cursor.execute("UPDATE users SET height = %s WHERE username = %s;", (new_height, username))
                connection.commit()
                messagebox.showinfo("Update", "Height updated!")
            elif new_weight is not None:
                cursor.execute("UPDATE users SET weight = %s WHERE username = %s;", (new_weight, username))
                connection.commit()
                messagebox.showinfo("Update", "Weight updated!")
            else:
                print("No changes to the goal provided.")
        else:
            print("Access Denied!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        connection.close()

# Get user profile from the database
def get_user_profile_auth(username):
    connection = mysql.connector.connect(
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database=DATABASE_NAME
    )
    cursor = connection.cursor()

    try:
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user_profile = cursor.fetchone()

        if user_profile:
            return {
                'user_id': user_profile[0],
                'username': user_profile[1],
                'email': user_profile[2],
                'password': user_profile[3],
                'goal': user_profile[4],
                'age': user_profile[5],
                'height': user_profile[6],
                'weight': user_profile[7]
            }
        else:
            return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        connection.close()

# Get user profile from the database
def get_user_profile(username):
    connection = mysql.connector.connect(
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database=DATABASE_NAME
    )
    cursor = connection.cursor()

    try:
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user_profile = cursor.fetchone()

        if user_profile:
            return {
                'user_id': user_profile[0],
                'username': user_profile[1],
                'email': user_profile[2],
                'goal': user_profile[4],
                'age': user_profile[5],
                'height': user_profile[6],
                'weight': user_profile[7]
            }
        else:
            return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        connection.close()
initialize_database()

