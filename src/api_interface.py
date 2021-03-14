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
    
    def __init__(self, db_path="db.sqlite", k_walk_score="UNSET", k_google="UNSET"):
        self.k_walk_score = k_walk_score
        self.k_google = k_google
        self.client_http = aiohttp.ClientSession()
        self.db_con = sqlite3.connect(db_path)
        self.db_cur = self.db_con.cursor()

    # if the current property has no geo coordinates, call the google api to find them and update
    async def update_property_coords(self, property):
        if property.address.lat == None or property.address.lon == None:
            property.address.lat, property.address.lon = self.get_geo_coord(property.address)

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

    # request the walk score of the current property and update the database
    async def update_property_score(self, p: Property):
        if p.score != None:
            address = p.address.address_line.split()
            score: Score = await get_score(p.address)
            a_num = (address.pop(0),)
            a_zip = (p.address.zip_code,)
            a_city = (p.address.city,)

            # TODO: UPDATE THIS EXECUTE WITH THE SUPPORTED COMMAND FROM db_handler.py
            db_cur.execute("UPDATE Property SET [Walk Score]=?, [Bike Score]=?, [Transit Score]=?, [Transit Summary]=?, WHERE [Street #]=? AND [Zip Code]=? AND [City]=?", (score.walk_score,), (score.bike_score,), (score.transit_score,),(score.transit_summary,), a_num, a_zip, a_city)
            p.score = score
    
    # requests the walk score of the current address and gets rid of the excess space
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

    # get the ID of the current property
    def get_id(self, p: Property):
        if p.id != None:
            return p.id

        # TODO: UPDATE THIS EXECUTE WITH THE SUPPORTED COMMAND FROM db_handler.py
        self.db_cur.execute("SELECT TOP 1 [Listing Number] FROM Property WHERE [Street #]=? AND [Zip Code]=? AND [City]=?", a_num, a_zip, a_city)
        return self.db_cur.fetchone()


