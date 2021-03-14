from haversine import haversine, Unit
import urllib
import aiohttp
import asyncio
import json
import sqlite3

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
        if self.address.has_valid_coordinates() and other.address.has_valid_coordinates():
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
        return self.lon != None and self.latitude != None


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

    def __init__(self, client, k_walk_score="UNSET"):
        self.k_walk_score = k_walk_score
        self.client = client

    async def get_score(self, a: Address):
        """Returns a dictionary of the walk, bike, and transit scores + descriptions, if available.

        Returns a `Score` object

        Or a `None` if an error occured
        """
        query = ApiClient.base_url_walk_score + urllib.parse.urlencode({'format': 'json', 'transit': 1, 'bike': 1, 'wsapikey': self.k_walk_score, 'lat': a.lat, 'lon': a.lon,
                                                                        'address': "{} {} {} {}".format(a.address_line, a.city, a.state, a.zip_code)})

        result = await self.client.get(query)
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

