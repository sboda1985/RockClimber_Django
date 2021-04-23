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
                wallname = request.POST['wallname']
                routename = request.POST['name']
                latitude = request.POST['latitude']
                longitude = request.POST['longitude']
                grading_system = request.POST['grading_system']
                difficulty = request.POST['difficulty']
                length = request.POST['length']
                length_unit = request.POST['length_unit']
                note = request.POST['note']
                rows = cursor.execute("SELECT ID FROM Wall WHERE Name = %s ", [wallname]) 
                if rows > 0:
                    wall_id = cursor.fetchone()
                    cursor.execute("""SELECT ID FROM Grading_systems Where Name = %s """, [grading_system])
                    grade_id = cursor.fetchone()[0]
                    cursor.execute("""SELECT ID FROM Length_units Where Name = %s """, [length_unit])
                    length_id = cursor.fetchone()[0]
                    route_rows = cursor.execute("""SELECT * FROM Route Where Name = %s """, [wallname])
                    
                    if route_rows == 0:
                        cursor.execute("""INSERT INTO `Route` (`ID`, `Wall_id`, `Name`, `Latitude`, `Longitude`, `Grading_ID`, `Difficulty`, `Length`, `Length_unit_id`, `Note`) VALUES 
                               (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (wall_id, routename, latitude,longitude,grade_id,difficulty,length,length_id,  note))
                        return JsonResponse({"route":"added"})
                    else:
                        return JsonResponse({"route":"exists"})
                else:
                    return JsonResponse({"Wall":"does not exists"})


