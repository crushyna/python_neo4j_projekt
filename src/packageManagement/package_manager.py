import time
import pandas as pd
from neo4j import GraphDatabase
from src.input_check import checkPackageWeight
from src.input_check import checkStartPoint
from src.input_check import checkDestinationPoint
from src.input_check import checkPackagesNames
from src.preloaded_data import getLocationNames
from src.preloaded_data import getPackagesList

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "AllsoP123098"))

def getPackagesSummary():
    with driver.session() as session:
        result = session.run('''
                MATCH (a)<-[r:delivery_from]-(n:Package)-[s:delivery_to]->(b)
                RETURN n.name AS package_name, n.weight AS package_weight, a.name AS delivery_from, b.name AS delivery_to
        ''')
        return pd.DataFrame(result.data())

def createNewPackage():
    while True:
        name = checkPackagesNames(getPackagesList())
        weight = checkPackageWeight()
        start = checkStartPoint(getLocationNames())
        dest = checkDestinationPoint(getLocationNames())
        if (start == dest):
            print("Start and destination are the same location! Try different!")
            time.sleep(2)
            continue
        else:
            with driver.session() as session:
                result = session.run('''
                                MATCH (a:Loc {name:$start}), (b:Loc {name:$dest})
                                CREATE (a)<-[:delivery_from]-(z:Package {name:$name, weight:$weight})-[:delivery_to]->(b)
                                RETURN z.name AS package_name, z.weight AS weight, a.name AS from_location, b.name AS to_location
                                ''', name=name, start=start, dest=dest, weight=weight)
                return pd.DataFrame(result.data())
            break
    return pd.DataFrame(result.data())

def deletePackage(package_name):
    with driver.session() as session:
        result = session.run('''
                                MATCH (n:Package {name:$name})
                                DETACH DELETE n
                            ''', name=package_name)
        '''this need fixing'''
        return result.data()