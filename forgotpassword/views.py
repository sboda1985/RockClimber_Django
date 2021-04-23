from django.http import HttpResponse
from django.db import connection
from django.http import JsonResponse
import hashlib
import sys, traceback
from django.views.decorators.csrf import csrf_exempt
import json
import time
from django.core.mail import send_mail
import functions

@csrf_exempt
def index(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            try:
                email = request.POST['email']
                cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s ", [email])
                nr = cursor.fetchone()
                #check if the email is registered
                if  nr[0]!=1:
                    return JsonResponse({'email':'not registered'})
                functions.generatepin(email)
                cursor.execute("SELECT pin FROM users_password JOIN users WHERE users.ID = users_password.ID AND users.email = %s", [email])
                pin = cursor.fetchone()
                cursor.execute("SELECT ID FROM users WHERE email = %s",[email])
                id = cursor.fetchone()[0]
                body = """Please enter the following PIN to reset your Password \n  \n """
                body = body + pin[0]
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
                return JsonResponse({'match - exc':str(traceback.format_exc())}, status=500)

