from django.db import connection
import time


def checkpin(ip, pin, id):
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
