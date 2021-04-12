from django.http import HttpResponse
from django.db import connection
from django.http import JsonResponse
import hashlib
import sys
from django.views.decorators.csrf import csrf_exempt
import json
import time

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@csrf_exempt
def index(request):
    if request.method == 'POST':  
        ip = get_client_ip(request)
        with connection.cursor() as cursor:
            try:
                today = time.strftime("%Y-%m-%d")	
                email = request.POST['email']
                cursor.execute("SELECT ID FROM users WHERE email = %s ", email) 
                id = cursor.fetchone()
                cursor.execute("""SELECT COUNT(*) FROM failed_login_attempts WHERE IP = %s AND failed_time = %s""", (ip, today))
                failed_attempts = cursor.fetchone()
                if failed_attempts[0] > 5:
                    return JsonResponse({'match':'false - to many attempts, wait a day'})
                
                cursor.execute("SELECT salt FROM users_password WHERE ID = %s", id)
                salt = cursor.fetchone()
                password = request.POST['password']
                #salt need conversion, it is a unicode tuple 
                typedhashpassword = hashlib.sha512(password + map(str, salt)[0]).hexdigest()
                cursor.execute("SELECT password FROM users_password WHERE ID = %s", id)
                dbhashpassword = cursor.fetchone()
                #db hash password is also a unicode tuple
                
                if typedhashpassword == map(str,dbhashpassword)[0]:
                    cursor.execute("UPDATE users SET last_login=%s WHERE ID=%s",(today, id[0]))
                    return JsonResponse({'match':'true'})
                else:
                    cursor.execute("""INSERT INTO failed_login_attempts(user_id, IP, failed_time) VALUES (%s,%s,%s)""",(id[0], ip, today))
                    return JsonResponse({'match':'false'})

            except Exception as e:
                return JsonResponse({'match - exc':str(e)})
    return JsonResponse({'match - no cursor':'false'})
