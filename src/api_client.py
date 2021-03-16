from haversine import haversine, Unit
from statistics import mean
import ast
import urllib
import aiohttp
import asyncio
import json
import sqlite3
import googlemaps
from db_handler import DatabaseHandler
class ApiClient:
    base_url_walk_score = "https://api.walkscore.com/score?"
    base_url_google_geocode = "https://maps.googleapis.com/maps/api/geocode/json?"
    
    def __init__(self, db_path="db.sqlite", k_walk_score="UNSET", k_google="UNSET"):
        self.k_walk_score = k_walk_score
        self.k_google = k_google
        self.client_realtor = None #TODO: UPDATE CLIENT ONCE WE GET ACCESS TO DB
        self.client_http = aiohttp.ClientSession() # close this
        self.db = DatabaseHandler(db_path)

    # TODO: UPDATE DEF ONCE WE KNOW THE SPECIFICS - THIS IS IN ESSENSE A MORE WRITTEN PSEUDOCODE
    async def search_properties(self, address: str, radius: float):
        # Find property info of address
        query = ""
        params = {}

        # Find all surrounding properties as json
        result = await self.client_http.get(query, params=params)
        
        # Turn json into dict
        surrounding_property = json.loads(result)

        # go through each entry in dict,
        for property in surrounding_property:
            query = """SELECT * FROM property
            WHERE id = ?
            LIMIT 1"""

            params = {'id': property['id']}

            # get klove data on entry
            response = self.db.read(query, params)
            
            # if klove data exists
            if len(response) == 1: 
                # pull data into score, lat, lon
                property['score']['walk_score'] = response['walk_score']
                property['score']['walk_desc'] = response['walk_desc']
                property['score']['bike_score'] = response['bike_score']
                property['score']['bike_desc'] = response['bike_desc']
                property['score']['transit_score'] = response['transit_score']
                property['score']['transit_desc'] = response['transit_desc']
                property['score']['transit_summary'] = response['transit_summary']
                property['lon'] = response['lon']
                property['lat'] = response['lat']
            # if klove data doesn't exist
            else:
                # lat, lon = get_geocords(entry->address)
                property['lat'], property['lon'] = self.get_geo_coord(property['address'])
                # score = get_score(entry -> address, lat, lon)
                property['score'] = self.get_score(property['address'], property['lat'], property['lon'])

                # add new data to current entry dict 
                query = """
                UPDATE property
                SET (id = ?,
                walk_score = ?,
                walk_desc = ?,
                bike_score = ?,
                bike_desc = ?,
                transit_score = ?,
                transit_desc = ?,
                transit_summary = ?,
                lat = ?,
                lon = ?)"""

                params = {
                    property['id'],
                    property['score']['walk_score'],
                    property['score']['walk_desc'],
                    property['score']['bike_score'],
                    property['score']['bike_desc'] ,
                    property['score']['transit_score'],
                    property['score']['transit_desc'],
                    property['score']['transit_summary'],
                    property['lat'],
                    property['lon']
                    }
                
                self.db.write(query, params)

        # return the dict
        return surrounding_property
    
    # requests the walk score of the current address and gets rid of the excess space
    async def get_score(self, address, lat, lon):
        """Returns a dictionary of the walk, bike, and transit scores + descriptions, if available.

        Or a `None` if an error occured
        """
        params = {'format': 'json', 'transit': '1', 'bike': '1', 'wsapikey': self.k_walk_score, 'lat': lat, 'lon': lon,'address': address}
        query = ApiClient.base_url_walk_score

        result = await self.client_http.get(query, params=params)
        try:
            result = json.loads(result.content._buffer[0])

            return { 'score' : {
                'walk_score': result['walkscore'], 
                'walk_desc': result['description'],
                'bike_score': result['bike']['score'],
                'bike_desc': result['bike']['description'],
                'transit_score': result['transit']['score'],
                'transit_desc': result['transit']['description'],
                'transit_summary': result['transit']['summary']}}

        except Exception as e:
            print(e)
            return None

    # return the latitude and longitude of the given address
    async def get_geo_coord(self, address):
        params = {
            'key': self.k_google,
            'address': "{} {} {} {}".format(address.address_line, address.city, address.state, address.zip_code)
        }
        
        response = await self.client_http.get(ApiClient.base_url_google_geocode, params=params)
        data = response.json() 

        if data['status'] == 'OK':
            result = data['results'][0]
            location = result['geometry']['location']
            return (location['lat'], location['lng'])
        else:
            return (None, None)


    # # if the current property has no geo coordinates, call the google api to find them and update
    # async def update_property_coords(self, property):
    #     if property.address.lat == None or property.address.lon == None:
    #         property.address.lat, property.address.lon = self.get_geo_coord(property.address)

    