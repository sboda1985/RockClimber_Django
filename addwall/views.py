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
                wallname = request.POST['wallname']
                walldescription = request.POST['walldescription']
                wallapproach = request.POST['wallapproach']
                wallaccess = request.POST['wallaccess']
                route_quality = request.POST['wall_route_quality']
                popularity = request.POST['popularity']
                note = request.POST['note']
                rows = cursor.execute("SELECT ID FROM Region WHERE Name = %s ", [region]) 
                if rows > 0:
                    region_id = cursor.fetchone()
                    wall_rows = cursor.execute("""SELECT * FROM Wall Where Name = %s """, [wallname])
                    if wall_rows == 0:
                        cursor.execute("""INSERT INTO `Wall` (`ID`, `Region_id`, `Name`, `Description`, `Approach`, `Access`, `Route_quality`, `Popularity`, `Note`) VALUES 
                              (NULL, %s, %s, %s, %s, %s, %s, %s, %s)""", (region_id, wallname, walldescription, wallapproach, wallaccess, route_quality, popularity, note))
                        return JsonResponse({"wall":"added"})
                    else:
                        return JsonResponse({"wall":"exists"})
                else:
                    return JsonResponse({"Region":"does not exists"})


