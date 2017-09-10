from django.http import HttpResponse
from django.db import connection
from django.http import JsonResponse
import hashlib
import sys, traceback
from django.views.decorators.csrf import csrf_exempt
import json
import time
from django.core.mail import send_mail
import random

def generatepin(email):
 cursor = connection.cursor()
 pin = random.randint(1000000, 10000000)  
 cursor.execute("""UPDATE `users_password` JOIN users SET pin=%s WHERE users.ID = users_password.ID AND users.email = %s""",(pin, email)) 

@csrf_exempt
def index(request):
 if request.method == 'POST':
  with connection.cursor() as cursor:
   try:
	email = request.POST['email']
	cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s ", email)
        nr = cursor.fetchone()
	#check if the email is registered
	if (map(str, nr)[0]!='1'):
		return JsonResponse({'email':'not registered'})
	generatepin(email)
	cursor.execute("SELECT pin FROM users_password JOIN users WHERE users.ID = users_password.ID AND users.email = %s", email)
	pin = cursor.fetchone()
	cursor.execute("SELECT ID FROM users WHERE email = %s",email)
	id = map(str, cursor.fetchone())[0]
	body = """Please enter the following PIN to reset your Password \n  \n """
	body = body + map(str,pin)[0]
	body = body + "\n"
	send_mail(
    		'RC - reset link',
    		body,
    		'admin@rockclimber.com',
    		[email],
    		fail_silently=False,
	)
		
        return JsonResponse({'forgot':'reset email sent', 'id':id})

   except:
        traceback.print_exc(file=sys.stdout)
	return JsonResponse({'exc':'error'})
