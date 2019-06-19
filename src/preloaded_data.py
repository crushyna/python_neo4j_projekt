from neo4j import GraphDatabase
import pandas as pd

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "AllsoP123098"))

def getDroneNames():
    with driver.session() as session:
        result = session.run('''
        MATCH (n:Drone) 
        RETURN n.name AS drone_name
        ''')
        session.close()
        return pd.DataFrame(result.data())

def getLocationNames():
    with driver.session() as session:
        result = session.run('''
        MATCH (n:Loc) 
        RETURN n.name AS location_name
        ''')
        session.close()
        return pd.DataFrame(result.data())