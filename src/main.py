import db_handler
import env
import aiohttp
import asyncio
from api_interface import ApiClient

client = ApiClient("src/db.sqlite", env.KEY_WALK_SCORE, env.KEY_GOOGLE_GEO)

# creating the connection 


cursor = connection.cursor()

query = """
SELECT * from property
WHERE (num_bedrooms = ?
AND num_bathrooms = ?
AND ABS(? - close_price) < (? * 0.1))
ORDER BY id
"""

params = [num_beds, num_br, list_price, list_price]
result_set = db_handler.execute_read_query(connection, query, params)

#data_points = execute_read_query(connection, q)
#for data_pt in data_points:
#    print(data_pt)

for row in result_set:
    print(row)

connection.close()