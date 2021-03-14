from haversine import haversine, Unit
import urllib
import aiohttp
import asyncio
import json
import sqlite3
import googlemaps

class Property:
    def __init__(self, address, square_footage, lot_size, bedrooms, bathrooms, year_created, price, estimated_monthly_cost):
        self.address = address
        self.square_footage = square_footage
        self.lot_size = lot_size
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.year_created = year_created
        self.estimated_monthly_cost = estimated_monthly_cost
        self.price = price
        self.score = None

    def distance_from(self, other):
        """Returns the distance from the current Property and the other Property, or `None` if

        """
        if not self.address.has_valid_coordinates() and not other.address.has_valid_coordinates():
            return None
        
        return haversine((self.address.latitude, self.address.longitude), (other.address.latitude, other.address.longitude), unit=Unit.MILES)


class Address:
    def __init__(self, address_line, city, state, zip_code, lat, lon):
        self.address_line = address_line
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.lat = lat
        self.lon = lon

    def has_valid_coordinates(self):
        return self.lon != None and self.lat != None

"""



API_KEY = 'AIzaSyAxHyjC0qy7dseYGnT8RpjGqV6UvwvUMhw'



address = '1600 Amphitheatre Parkway, Mountain View, CA'

params = {
    'key': API_KEY,
    'address': address
}

base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
response = requests.get(base_url, params=params).json()
response.keys()

if response['status'] == 'OK':
    geometry = response['results'][0]['geometry']
    lat = geometry['location']['lat']
    lon = geometry['location']['lng']

print(lat, lon)
    
"""
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
    base_url_google_geocode = 'https://maps.googleapis.com/maps/api/geocode/json?'
    
    def __init__(self, client_db, k_walk_score="UNSET", k_google="UNSET"):
        self.k_walk_score = k_walk_score
        self.k_google = k_google
        self.client_http = aiohttp.ClientSession()
        self.client_db = client_db

    async def update_property_coords(self, property):
        if property.address.lat == None or property.address.lon == None
            property.address.lat, property.address.lon = self.get_geo_coord(property.address)

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
            return location['lat'], location['lng']
        else:
            return

    async def update_property_score(self, p: Property):
        if p.score != None
            address = p.address.address_line.split()
            score: Score = await get_score(p.address)
            a_num = (address.pop(0),)
            a_zip = (p.address.zip_code,)
            a_city = (p.address.city,)
            cur.execute("UPDATE Property SET [Walk Score]=?, [Bike Score]=?, [Transit Score]=?, [Transit Summary]=?, WHERE [Street #]=? AND [Zip Code]=? AND [City]=?", (score.walk_score,), (score.bike_score,), (score.transit_score,),(score.transit_summary,), a_num, a_zip, a_city)
            p.score = score
        
    async def get_score(self, a: Address):
        """Returns a dictionary of the walk, bike, and transit scores + descriptions, if available.

        Returns a `Score` object

        Or a `None` if an error occured
        """
        params = {'format': 'json', 'transit': '1', 'bike': '1', 'wsapikey': self.k_walk_score, 'lat': a.lat, 'lon': a.lon,'address': "{} {} {} {}".format(a.address_line, a.city, a.state, a.zip_code)}
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

    def get_id(self, p: Property):
        if p.id != None:
            return p.id
        self.cur.execute("SELECT TOP 1 [Listing Number] FROM Property WHERE [Street #]=? AND [Zip Code]=? AND [City]=?", a_num, a_zip, a_city)
        return self.cur.fetchone()


import env

env.KEY_GOOGLE_GEO

