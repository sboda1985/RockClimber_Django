from django.http import HttpResponse
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import functions

@csrf_exempt
def index(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            pin = request.POST['pin']
            user_id = request.POST['id']
            if functions.checkpin(user_id, pin, request):
                region = request.POST['region']
                description = request.POST['description']
                note = request.POST['note']
                rows = cursor.execute("SELECT ID FROM Region WHERE Name = %s ", [region]) 
                if rows == 0:
                    cursor.execute("""INSERT INTO `Region` (`ID`, `Name`, `Description`, `Note`) VALUES
                                  (NULL, %s, %s, %s)""", (region, description, note)) 
                    return JsonResponse({"Region":"added"})
                else:
                    return JsonResponse({"Region":" exists"})


