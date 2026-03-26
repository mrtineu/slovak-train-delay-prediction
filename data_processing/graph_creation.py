import networkx as nx
from database import get_database

database = get_database()

collection = database['trainStateSnaphots']

sample = collection.find_one()
print(sample)

