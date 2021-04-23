from django.db import connection
import time
import random

def get_client_ip(request):
    ip = '0.0.0.0'
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



def generatepin(email):
    cursor = connection.cursor()
    pin = random.randint(1000000, 10000000)  
    cursor.execute("""UPDATE `users_password` JOIN users SET pin=%s WHERE users.ID = users_password.ID AND users.email = %s""",(pin, email)) 



def checkpin(id, pin, request):
    ip = get_client_ip(request)
    today = time.strftime("%y-%m-%d")
    with connection.cursor() as cursor:
        cursor.execute("""SELECT COUNT(*) FROM failed_pin_attempts WHERE IP = %s AND failed_time = %s""", (ip, today))
        failed_attempts = cursor.fetchone()
        if failed_attempts[0] > 5:
            return 5
        cursor.execute("SELECT pin FROM users_password WHERE id = %s ", [id])
        value = cursor.fetchone()
        dbpin = value[0] 
                
        #check if the email is still available	
        if (dbpin =='0' or dbpin == 0 ):
            return 4
        if (dbpin != str(pin)):
            return 3
        return 1	

def getpin(id):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT pin FROM `users_password` WHERE id = %s""", [id])
        return cursor.fetchone()[0]
