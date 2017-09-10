from django.http import HttpResponse
from django.db import connection
from django.http import JsonResponse
import hashlib
import sys
from django.views.decorators.csrf import csrf_exempt
import random
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
  with connection.cursor() as cursor:
   try:
        id = request.POST['id']
	pin = request.POST['pin']
	typpass = request.POST['password']
	cursor.execute("""SELECT COUNT(*) FROM failed_pin_attempts WHERE IP = %s AND failed_time = %s""", (ip, today))
	failed_attempts = cursor.fetchone()
	if failed_attempts[0] > 5:
		return JsonResponse({'password_reset':'false - to many attempts, wait a day'})
	#get the pin from the database
        cursor.execute("SELECT pin FROM users_password WHERE id = %s ", id)
        value = cursor.fetchone()
	dbpin = map(str, value)[0] 
	today = time.strftime("%y-%m-%d")
	#check if the email is still available	
	if (dbpin =='0'):
		return JsonResponse({'reset passwrod':'password recovery not requested'})
	if (dbpin != pin):
		return JsonResponse({'reset password':'password recovery not requested'})	
	cursor.execute("SELECT salt FROM users_password WHERE id = %s", id)
	value = cursor.fetchone()
	salt = map(str, value)[0]
	#print typpass
	password = hashlib.sha512(typpass + salt).hexdigest()
	#add the new password and reset pin
	cursor.execute(""" UPDATE `users_password` SET `password`=%s,`password_date`=%s,`pin`=0 WHERE `ID`=%s""",( password, today,id))
        cursor.close()
        return JsonResponse({'password reset':'success'})
        
   except Exception as e:
        return JsonResponse({'not reset':str(e)})
 return JsonResponse({'match - no cursor':'unsuccessful'})

