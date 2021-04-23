import datetime
from django.db import connection, connections
from functools import reduce
import hashlib


def get_value_from_sql(value):
    return value[0]

def checktoken(user, token):
    with connections['default'].cursor() as cursor:
        try:
            cursor.execute("SELECT pin FROM users_password WHERE ID in (SELECT ID Fro users WHERE username = %s) ", [user])
            value = cursor.fetchone()
            databasetoken = get_value_from_sql(value)

            if (token == databasetoken) and len(databasetoken) > 1:
                return True
            return False
        except Exception as e:
            return False

def getsalt(user):
    with connections['default'].cursor() as cursor:
        cursor.execute("SELECT salt FROM users WHERE username = %s",[user])
        value = cursor.fetchone()
        hashsalt = get_value_from_sql(value)
        return hashsalt

def checksalt(user, salt):
    db_salt = getsalt(user)
    return db_salt == salt
         
def hashsaltedpassword(password, hashsalt):
    h_password = password + hashsalt
    return hashlib.sha512(h_password.encode()).hexdigest()

def checkpassword(user, password):
    with connections['default'].cursor() as cursor:
        try:
            hashsalt = getsalt(user)
            cursor.execute("SELECT password FROM users WHERE username = %s",[user])
            value = cursor.fetchone()
            db_password = get_value_from_sql(value) 
            hashed_password = hashsaltedpassword(password, hashsalt)
            if (hashed_password == db_password):
                return True
            return False
        except:
            return False

def log_activity(name, text,action):
    #get the current timestamp
    #millis = int(round(time.time() ))
    return 0


def changepassword(user, password):
    with connections['default'].cursor() as cursor:
        salt = getsalt(user)
        hashed_password = hashsaltedpassword(password, salt)
        cursor.execute("UPDATE users SET password = %s WHERE username = %s;", [hashed_password, user])
        


def gettoken(user): 
    with connections['default'].cursor() as cursor: 
        try: 
            cursor.execute("SELECT token FROM users WHERE username = %s ", [user]) 
            value = cursor.fetchone() 
            databasetoken = get_value_from_sql(value) 
            return databasetoken 
        except Exception as e:
            return str(e)
