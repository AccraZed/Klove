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

class Score:
    def __init__(self, walk_score, walk_desc, bike_score, bike_desc, transit_score, transit_desc, transit_summary):
        self.walk_score = walk_score
        self.walk_desc = walk_desc
        self.bike_score = bike_score
        self.bike_desc = bike_desc
        self.transit_score = transit_score
        self.transit_desc = transit_desc
        self.transit_summary = transit_summary

class ApiClient:
    base_url_walk_score = "https://api.walkscore.com/score?"
    base_url_google_geocode = "https://maps.googleapis.com/maps/api/geocode/json?"
    
    def __init__(self, db_path="db.sqlite", k_walk_score="UNSET", k_google="UNSET"):
        self.k_walk_score = k_walk_score
        self.k_google = k_google
        self.client_http = aiohttp.ClientSession() # close this
        self.db = DatabaseHandler(db_path)

    def search_properties(self, address: str, radius: float):
        raise NotImplementedError
        # Find property of address
        
        # Find all surrounding properties as json
        
        # Find extra info of each property
            # Turn json into dict

            # go through each entry in dict,
                # get klove data on entry
                # if klove data exists
                    # pull data into score, lat, lon
                # if klove data doesn't exist
                    # lat, lon = get_geocords(entry->address)
                    # get_score(entry -> address, lat, lon)

                # add new data to current entry dict 
                    # (entry['score']['walk_score'] = new score stuff, entry['lat' = lat] etc)

        # return the dict

    # request the walk score of the current property and update the database
    async def update_property_db(self, p: Property):
        if p.score != None:
            address = p.address.address_line.split()
            score: Score = await self.get_score(p.address)

            query = """
            UPDATE property
            SET walk_score = ?,
                bike_score = ?,
                transit_score = ?,
                transit_summary = ?
            WHERE (street_number = ?
            AND zip_code = ?
            AND city = ?)
            """
            params = [score.walk_score, score.bike_score, score.transit_score, score.transit_summary, (address.pop(0),), (p.address.zip_code,), (p.address.city,)]

            self.db.write(self.db_con, query, params)

            p.score = score
    
    # requests the walk score of the current address and gets rid of the excess space
    async def get_score(self, address):
        """Returns a dictionary of the walk, bike, and transit scores + descriptions, if available.

        Returns a `Score` object

        Or a `None` if an error occured
        """
        params = {'format': 'json', 'transit': '1', 'bike': '1', 'wsapikey': self.k_walk_score, 'lat': a.lat, 'lon': a.lon,'address': address}
        query = ApiClient.base_url_walk_score

        result = await self.client_http.get(query, params=params)
        try:
            result = json.loads(result.content._buffer[0])

            return Score(result['walkscore'],
                         result['description'],
                         result['bike']['score'],
                         result['bike']['description'],
                         result['transit']['score'],
                         result['transit']['description'],
                         result['transit']['summary'])
        except Exception as e:
            print(e)
            
    # def get_distance(self, ):
    #     return haversine((self.address.latitude, self.address.longitude), (other.address.latitude, other.address.longitude), unit=Unit.MILES)


    # # if the current property has no geo coordinates, call the google api to find them and update
    # async def update_property_coords(self, property):
    #     if property.address.lat == None or property.address.lon == None:
    #         property.address.lat, property.address.lon = self.get_geo_coord(property.address)

    # # return the latitude and longitude of the given address
    # async def get_geo_coord(self, address):
    #     params = {
    #         'key': self.k_google,
    #         'address': "{} {} {} {}".format(address.address_line, address.city, address.state, address.zip_code)
    #     }
        
    #     response = await self.client_http.get(ApiClient.base_url_google_geocode, params=params)
    #     data = response.json() 

    #     if data['status'] == 'OK':
    #         result = data['results'][0]
    #         location = result['geometry']['location']
    #         return (location['lat'], location['lng'])
    #     else:
    #         return (None, None)