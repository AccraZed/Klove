import db_handler
import env
import aiohttp
import asyncio
from api_interface import *
import json

client = ApiClient("src/db.sqlite", env.KEY_WALK_SCORE, env.KEY_GOOGLE_GEO)

# We need to link the FrontEnd input to this constructor
user_property = Property('1234 Main St.', 1500, 2, 2, 1965, 130000, 140000)

print("Test")

# returns dict of 5 properties and float of 5-value closing price avg
similar_properties, average_sell_price = client.get_most_similar(user_property)

# This is the packet going to the front end for arrangement
to_frontend = json.dumps(similar_properties)

# The moneyshot
if int(user_property.list_price) < average_sell_price:
    print("Undervalued")
else:
    print("Overvalued")

