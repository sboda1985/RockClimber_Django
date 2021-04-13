from django.http import HttpResponse
from django.db import connection
from django.http import JsonResponse
import hashlib
import sys
from django.views.decorators.csrf import csrf_exempt
import random
import time

@csrf_exempt
def index(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            try:
                email = str(request.POST['email'])
                cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s ", [email])
                nr = cursor.fetchone()
                #check if the email is still available	
                if nr[0]!=0:
                    return JsonResponse({'email':'already taken'})
                #get the max current ID
                cursor.execute("SELECT MAX( ID ) FROM users WHERE 1") 
                id = cursor.fetchone()
                id = id[0]
                id = id + 1 
                #make username from email   
                username = email.split("@")[0]
                login = str(time.strftime("%Y-%m-%d"))
                today = str(time.strftime("%Y-%m-%d"))
                realname = ""
                try:
                    realname = request.POST['realname']
                except:
                    realname = ""
                #insert user
                cursor.execute("""INSERT INTO `users`(`ID`, `username`, `realname`, `email`, `last_login`, `account_creation`, `account_active`) VALUES (%s,%s,%s,%s,%s,%s,%s)""", (id, username, realname, email, login, today, "1"))	
                #generate salt from email and a random number	
                rd = random.getrandbits(128)
                hemail = email + str(rd)
                salt = hashlib.sha512(hemail.encode()).hexdigest()
                #get the current password and salt it
                typpass = request.POST['password']
                #print typpass
                hpass = typpass + salt
                password = hashlib.sha512(hpass.encode()).hexdigest()
                #add the password and salt
                cursor.execute(""" INSERT INTO `users_password`(`ID`, `password`, `salt`, `password_date`, `pin`) VALUES (%s,%s,%s,%s,%s)""",(id, password, salt, today, 0))
                cursor.close()
                return JsonResponse({'create':'success'})
                    
            except Exception as e:
                return JsonResponse({'not created':str(e)})
            return JsonResponse({'match - no cursor':'unsuccessful'})

