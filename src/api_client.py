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
        self.client_http = aiohttp.ClientSession()  # close this
        self.db = DatabaseHandler(db_path)

    async def search_properties(self, query_property, query, params, radius: float):
        # Find all surrounding properties as dict
        surrounding_property = self.db.read(query, params)
        self.update_property_coords(query_property['id'])
        self.update_property_score(query_property['id'])

        # go through each entry in dict,
        for property in surrounding_property:
            self.update_property_coords(property['id'])
            self.update_property_score(query_property['id'])

            params = {'id': property['id']}

            if haversine.haversine((query_property['lat'], query_property['lon']), (property['lat'], [property['lon']]), unit=Unit.MILES) > radius:
                surrounding_property.remove(property)

        # return the dict
        return surrounding_property

    # requests the walk score of the current address and gets rid of the excess space
    async def get_score(self, address, lat, lon):
        """Returns a dictionary of the walk, bike, and transit scores + descriptions, if available.

        Or a `None` if an error occured
        """
        params = {'format': 'json', 'transit': '1', 'bike': '1',
                  'wsapikey': self.k_walk_score, 'lat': lat, 'lon': lon, 'address': address}
        query = ApiClient.base_url_walk_score

        result = await self.client_http.get(query, params=params)
        try:
            result = json.loads(result.content._buffer[0])

            return {
                'walk_score': result['walkscore'],
                'walk_desc': result['description'],
                'bike_score': result['bike']['score'],
                'bike_desc': result['bike']['description'],
                'transit_score': result['transit']['score'],
                'transit_desc': result['transit']['description'],
                'transit_summary': result['transit']['summary']}

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

    # if the current property has no geo coordinates, call the google api to find them and update

    async def update_property_score(self, id, force=False):
        query = """
        SELECT * FROM property
        WHERE id = ?
        LIMIT 1"""

        params = id

        response = self.db.read(query, params)

        try:
            if not force and response['lat'] != None and response['lon'] != None:
                return

        score = self.get_score(property['address'])

        query = """
        UPDATE property
                walk_score = ?,
                bike_score = ?,
                transit_score = ?,
                transit_summary = ?
        WHERE id = ?"""

        params = {
            score['walk_score'],
            score['bike_score'],
            score['transit_score'],
            score['transit_summary'],
            id
        }

        self.db.write(query, params)

    # if the current property has no geo coordinates, call the google api to find them and update
    async def update_property_coords(self, id, force=False):
        query = """
        SELECT * FROM property
        WHERE id = ?
        LIMIT 1"""

        params = id

        response = self.db.read(query, params)

        try:
            if not force and response['walk_score'] != None:
                return

        response['lat'], response['lon'] = self.get_geo_coord(
            property['address'])

        query = """
        UPDATE property
                lat = ?,
                lon = ?)
        WHERE id = ?"""

        params = {response['lat'], response['lon'], id}

        self.db.write(query, params)

    def get_most_similar(self, p: Property):

        sim_query = """
        SELECT * from property
        WHERE (num_bedrooms = ?
        AND num_bathrooms = ?
        AND ABS(? - close_price) < (? * 0.1))
        LIMIT 10
        """

        # Yields list of top most similar properties
        sim_params = [p.bedrooms, p.bathrooms, p.list_price, p.list_price]
        sim_results = db_handler.execute_read_query(
            self.db_con, sim_query, sim_params)
        json_output = json.dumps(sim_results)

        return json_output

    # Simplified, mechanical averaging of dict values
    def get_average_close_price(self, dataList):
        number_of_entries = 0
        sum = 0

        for dict in dataList:
            for key in dict:
                if key == 'close_price':
                    sum += dict['close_price']
                    number_of_entries += 1

        avg = sum / float(1 + number_of_entries)

        return avg
