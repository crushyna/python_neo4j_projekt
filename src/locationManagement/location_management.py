import pandas as pd
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "AllsoP123098"))
#session = driver.session()

def getLocationsSummary():
    with driver.session() as session:
        result = session.run('''
                MATCH (n:Loc) 
                RETURN n.name AS name
        ''')
        return pd.DataFrame(result.data())

def getSkybasesSummary():
    with driver.session() as session:
        result = session.run('''
                MATCH (n:Loc {base:1}) 
                RETURN n.name AS name, n.base AS is_skybase
        ''')
        return pd.DataFrame(result.data())

def addSkybase(location_name):
    with driver.session() as session:
        result = session.run('''
                                MATCH (n:Loc {name:$name})
                                SET n.base = 1
                                RETURN n.name AS name, n.base AS is_skybase
                            ''', name=location_name)
        return result.data()

def removeSkybase(location_name):
    with driver.session() as session:
        result = session.run('''
                                MATCH (n:Loc {name:$name})
                                REMOVE n.base
                                RETURN n.name AS name, n.base AS is_skybase
                            ''', name=location_name)
        return result.data()