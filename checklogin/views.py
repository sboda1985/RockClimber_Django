from django.http import HttpResponse
from django.db import connection
from django.http import JsonResponse
import hashlib
import traceback
import sys
from django.views.decorators.csrf import csrf_exempt
import json
import time
import functions


@csrf_exempt
def index(request):
    if request.method == 'POST':  
        ip = functions.get_client_ip(request)
        with connection.cursor() as cursor:
            try:
                today = time.strftime("%Y-%m-%d")	
                email = str(request.POST['email'])
                cursor.execute("SELECT ID FROM users WHERE email = %s ", [email]) 
                id = cursor.fetchone()[0]
                cursor.execute("""SELECT COUNT(*) FROM failed_login_attempts WHERE IP = %s AND failed_time = %s""", (ip, today))
                failed_attempts = cursor.fetchone()
                if failed_attempts[0] > 5:
                    return JsonResponse({'match':'false - to many attempts, wait a day'})
                
                cursor.execute("SELECT salt FROM users_password WHERE ID = %s", [id])
                salt = cursor.fetchone()
                password = request.POST['password']
                #salt need conversion, it is a unicode tuple
                h_password = str(password) + salt[0]  
                typedhashpassword = hashlib.sha512(h_password.encode()).hexdigest()
                cursor.execute("SELECT password FROM users_password WHERE ID = %s", [id])
                dbhashpassword = cursor.fetchone()
                #db hash password is also a unicode tuple
                
                if typedhashpassword == dbhashpassword[0]:
                    functions.generatepin(email)
                    cursor.execute("UPDATE users SET last_login=%s WHERE ID=%s",(today, id))
                    pin = functions.getpin(id)   
                    return JsonResponse({'match':'true','pin':pin})
                else:
                    cursor.execute("""INSERT INTO failed_login_attempts(user_id, IP, failed_time) VALUES (%s,%s,%s)""",(id[0], ip, today))
                    return JsonResponse({'match':'false'})

            except Exception as e:
                return JsonResponse({'match - exc':str(traceback.format_exc())}, status=500)
    return JsonResponse({'match - no cursor':'false'})
