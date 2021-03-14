import db_handler
import env
import aiohttp
import asyncio
from api_interface import ApiClient

client = ApiClient("src/db.sqlite", env.KEY_WALK_SCORE, env.KEY_GOOGLE_GEO)

# We need to link the FrontEnd input to this constructor
user_property = client.Property('1234 Main St.', '1500', '2', '2', '1965', '130000', '140000')

# returns dict of 5 properties
similar_properties = client.get_most_similar(user_property)
for row in similar_properties:
    print(row)
average_sell_price = client.get_avg_close_price(similar_properties)

# The moneyshot
if user_property.list_price < average_sell_price:
    print("Undervalued")
else:
    print("Overvalued")

