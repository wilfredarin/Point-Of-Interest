import csv
import requests


#enter api key

api_key="" 

#file strucutre
poi_file = 'poi.csv'
poi_name = 2
lat_col = 3
lon_col = 4



#area 500x500 sq metters
search_box_len = 500;
	
# at equator dist btwn longitude 111.045 km | at 45 degree it's 79 km
# 110km is 1 degree | 110000 meter is 1 degree-> 1 meter : 0.110000 long
meter_to_coordinate = 0.0000090909;

lat_delta = ((search_box_len)/2)*meter_to_coordinate;
lon_delta = ((search_box_len)/2)*meter_to_coordinate;

print("Point of Interest Test ")
print("################################")
print("")

outlet_coordinates = input("Enter outlet Coordinates : ")

outlet_coordinates = outlet_coordinates.split(",")
outlet_lat = float(outlet_coordinates[0])
outlet_lon = float(outlet_coordinates[1][1:])

origin = str(outlet_lat)+","+str(outlet_lon)
url_begin ="https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins="

lon_west_bound = outlet_lon -lon_delta;
lon_east_bound = outlet_lon+lon_delta;
lat_north_bound = outlet_lat+lat_delta;
lat_south_bound = outlet_lat-lat_delta;

	

lower_distance = float(input("Set lower limit distance in meters : "))
upper_distance = float(input("Set upper limit distance in meters : "))

#input validation
while lower_distance>upper_distance:
	print("Lower Limit has to be lesser than upper limit | Please Re-enter")
	lower_distance = float(input("Set lower limit distance in meters : "))
	upper_distance = float(input("Set upper limit distance in meters : "))


destination = ""
with open(poi_file,'r') as csvfile:
	csvreader = csv.reader(csvfile)
	for row in csvreader:
		row = row[0].split(",")
		lat = float(row[0])
		lon = float(row[1][1:])
		if (lat<lat_north_bound and lat>lat_south_bound):
			if lon<lon_east_bound and lon>lon_west_bound:
				if destination =="":
					destination+=str(lat)+"%2C"+str(lon)
				else:
					destination+="%7C"+str(lat)+"%2C"+str(lon)
#api
url = url_begin + origin+"&destinations="+destination+"&key="+api_key

print("####### Result #######")
print("")
print("")
if destination!="":
	req = requests.get(url=url)
	response = req.json()
	if response['status']=="OK":
		places = response['rows'][0]['elements']
		min_dist = float("inf")
		for i in range(len(places)):
			min_dist = min(min_dist,places[i]['distance']['value'])
		print("Min Distance from POI is : ",min_dist,"meters")
		print("")
		if min_dist<=lower_distance:
			print("$$$$$  Passed POI  $$$$$")
			print("")
		elif min_dist>lower_distance and min_dist<upper_distance:
			print("!!!!  Manual Intervention Required   !!!!!")
			print("")
		else:
			print("XXXXX Failed POI  XXXXX")
			print("")
	else:
		print("XXXXX Failed POI XXXXX")
		print("")



else:
	print("Failed POI")
	print("")