from django.http import HttpResponse
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            region = request.POST['region']
            wallname = request.POST['wallname']
            walldescription = request.POST['walldescription']
            wallapproach = request.POST['wallapproach']
            wallaccess = request.POST['wallaccess']
            route_quality = request.POST['wall_route_quality']
            popularity = request.POST['popularity']
            note = request.POST['note']
            rows = cursor.execute("SELECT ID FROM Region WHERE Name = %s ", region) 
            if rows > 0:
                region_id = cursor.fetchone()
                cursor.execute("""INSERT INTO `Wall` (`ID`, `Region_id`, `Name`, `Description`, `Approach`, `Access`, `Route_quality`, `Popularity`, `Note`) VALUES 
                              (NULL, %s, %s, %s, %s, %s, %s, %s, %s)""", (region_id, wallname, walldescription, wallaccess, route_quality, popularity, note))
