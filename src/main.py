import db_handler
import env
import aiohttp
import asyncio
from api_interface import *
import json

client = ApiClient("src/db.sqlite", env.KEY_WALK_SCORE, env.KEY_GOOGLE_GEO)

# We need to link the FrontEnd input to this constructor
user_property = Property('1234 Main St.', 1500, 2, 2, 1965, 130000, 140000)

# returns dict-like string of 5 properties and float of 5-value closing price avg
similar_properties = client.get_most_similar(user_property)
print(similar_properties)
# Writes json to file for frontend
with open('similar_properties.json', 'w') as f:
    json.dump(similar_properties, f, ensure_ascii=False, indent=4)

json_to_dict = json.loads(similar_properties)
average_close_price = client.get_average_close_price(json_to_dict)
print(average_close_price)


# The moneyshot
if user_property.list_price < average_close_price:
    print("Undervalued")
else:
    print("Overvalued")



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