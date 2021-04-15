from api_client import *
from haversine import haversine, Unit
import db_handler
import env
import aiohttp
import asyncio
import json
import sys


# TODO: PLAN OUT AND FIX THIS ENTIRE DOCUMENT, BACKEND IS COMPLETELY RESTRUCTURED
client = ApiClient("src/db.sqlite", env.KEY_WALK_SCORE, env.KEY_GOOGLE_GEO)

# We need to link the FrontEnd input to this constructor
# houseNumber, streetName, city, state, zip
query_property = sys.argv[1:6]
query_property[0] = int(query_property[0])  # houseNumber

property_info = client.search_properties(query_property)

if len(property_info) == 0:
    print("PROPERTY NOT FOUND")
    client.client_http.close()
    sys.exit(0)

print(property_info)

client.update_property_score(query_property)

property_info = property_info[0]
query_property.square_footage = property_info['total_sqft']
query_property.bedrooms = property_info['num_bedrooms']
query_property.bathrooms = property_info['num_bathrooms']
query_property.year_built = property_info['year_built']
query_property.list_price = property_info['list_price']

# returns dict-like string of 5 properties and float of 5-value closing price avg
similar_properties = client.get_most_similar(query_property)

print(similar_properties)
# Writes json to file for frontend
with open('similar_properties.json', 'w') as f:
    json.dump(similar_properties, f, ensure_ascii=False, indent=4)

json_to_dict = json.loads(similar_properties)
average_close_price = client.get_average_close_price(json_to_dict)
print(average_close_price)

# The moneyshot
if query_property.list_price < average_close_price:
    print("Undervalued")
else:
    print("Overvalued")

client.client_http.close()


# Not using get_id to locate and handle user selection
# Both printing statements(ln13 of main.py(LIST) and ln182 of
#     api_interface.py(DICT)) are not printing any values
# Further abstraction is possible an might improve clarity
# The mechanisms for receipt and transfer of property information
#     are in place and only need genuine 'connections' from both
#     ends.
# I believe that the 'avg_query' syntax is wrong. The intent is
#     to average the close_price values listed in the subset
#     in sim_results(5-properties)
# Inherent biases exists in our data pool because we are
#     narrowly selecting a range of data against which we
#     compare listing price. Additionally, by using LIMIT,
#     we are choosing from a heavily-skewed small range.
#     We can raise the LIMIT in the get_most_similar() function
#     to increase our sample pool we use for averaging
# (JS)
