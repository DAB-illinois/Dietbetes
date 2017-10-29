import requests
import json
import state_abbrev
import google_key

from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)
DATABASE_NAME = "databetes_app"
TABLE_NAME = "health_centers"
db = client[DATABASE_NAME]

def find_closest_centers(lat, lon):
    base = "http://maps.googleapis.com/maps/api/geocode/json?"
    params = "latlng={lat},{lon}".format(lat=lat,lon=lon)
    url = "{base}{params}".format(base=base, params=params)
    response = requests.get(url)
    print(response.json())
    state_ab = response.json()['results'][0]['formatted_address'].split(" ")[-3]

    centers = db[TABLE_NAME]
    closer_centers = []
    current_closer_center = []

    for state in centers.find({'state':state_ab}):
        
        for center in state["centers"]:
            
            lat_lon = convert_to_lat_lon(center['address'], center['name'])
            if lat_lon == None:
                continue
            distance = get_distance(lat, lon, lat_lon[0], lat_lon[1])
            print(distance)

            if distance < (8.04672) * 3:
                current_closer_center.append(center["name"])
                current_closer_center.append(lat_lon)
                current_closer_center.append(center["telephone"])

                closer_centers.append(current_closer_center)
                current_closer_center = []

    return closer_centers

def convert_to_lat_lon(address, name):
    response_address = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+("+".join(address.split(" ")))+"&key="+google_key.KEY)
    response_name = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+("+".join(name.split(" ")))+"&key="+google_key.KEY)
    json_address = response_address.json()
    json_name = response_name.json()
    if json_address['results'] == [] and json_name['results'] == []:
        return None
    elif json_address['results'] == []:
        json_address = json_name
    coord = json_address['results'][0]['geometry']['location']
    
    lat_lon = [coord['lat'], coord['lng']]
    print(lat_lon)
    
    return lat_lon

from math import sin, cos, sqrt, atan2, radians
# approximate radius of earth in km
def get_distance(lat_user, lon_user, lat_center, lon_center):
    R = 6373.0

    lat1 = radians(lat_user)
    lon1 = radians(lon_user)
    lat2 = radians(lat_center)
    lon2 = radians(lon_center)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

def main():
    print(find_closest_centers())

	# HTML and Javascript version of the nearest location finder

    # <script type="text/javascript" src="//maps.googleapis.com/maps/api/js?sensor=true&libraries=places"></script>

    # <script type="text/javascript">
    #   var map;
    #   var infowindow;
    #   var service ;
    #   function initialize(lat,lng) 
    #   {
    #     var origin = new google.maps.LatLng(lat,lng);
       
    #     map = new google.maps.Map(document.getElementById('map'), {
    #       mapTypeId: google.maps.MapTypeId.HYBRID,
    #       center: origin,
    #       zoom: 15
    #     });
        
    #     var request = {
    #       location: origin,
    #       radius: 2500,
    #       types: ['train_station','bus_station','subway_station','transit_station']
    #     };
    #     infowindow = new google.maps.InfoWindow();
    #     service = new google.maps.places.PlacesService(map);
    #     service.search(request, callback);
    #   }

    #   function callback(results, status) {
    #     if (status == google.maps.places.PlacesServiceStatus.OK) {
    #       for (var i = 0; i < results.length; i++) {
    #         createMarker(results[i]);
    #       }
    #     }
    #   }

    #   function createMarker(place) {
      
    #     var placeLoc = place.geometry.location;
    #     var marker = new google.maps.Marker({
    #       map: map,
    #       position: place.geometry.location
    #     });
    #     var content='<strong style="font-size:1.2em">'+place.name+'</strong>'+
    #                 '<br/><strong>Latitude:</strong>'+placeLoc.lat()+
    #                 '<br/><strong>Longitude:</strong>'+placeLoc.lng()+
    #                 '<br/><strong>Type:</strong>'+place.types[0]+
    #                 '<br/><strong>Rating:</strong>'+(place.rating||'n/a');
    #     var more_content='<img src="http://googleio2009-map.googlecode.com/svn-history/r2/trunk/app/images/loading.gif"/>';
        
    #     //make a request for further details
    #     service.getDetails({reference:place.reference}, function (place, status) 
    #                                 {
    #                                   if (status == google.maps.places.PlacesServiceStatus.OK) 
    #                                   {
    #                                     more_content='<hr/><strong><a href="'+place.url+'" target="details">Details</a>';
                                        
    #                                     if(place.website)
    #                                     {
    #                                       more_content+='<br/><br/><strong><a href="'+place.website+'" target="details">'+place.website+'</a>';
    #                                     }
    #                                   }
    #                                 });


    #     google.maps.event.addListener(marker, 'click', function() {
          
    #       infowindow.setContent(content+more_content);
    #       infowindow.open(map, this);
    #     });
    #   }

    #   google.maps.event.addDomListener(window, 'load', function(){initialize(1.299845,103.856292);});
    # </script>
    # <div id="map" style="height:400px;"></div>