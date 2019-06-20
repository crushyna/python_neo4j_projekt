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
        df = pd.DataFrame(result.data())
        return list(df['drone_name'])

def getLocationNames():
    with driver.session() as session:
        result = session.run('''
        MATCH (n:Loc) 
        RETURN n.name AS location_name
        ''')
        df = pd.DataFrame(result.data())
        return list(df['location_name'])

def getBasesNames():
    with driver.session() as session:
        result = session.run('''
        MATCH (n:Loc {base:1}) 
        RETURN n.name AS location_name
        ''')
        df = pd.DataFrame(result.data())
        return list(df['location_name'])

def getPackagesList():
    with driver.session() as session:
        result = session.run('''
        MATCH (n:Package) 
        RETURN n.name AS package_name
        ''')
        df = pd.DataFrame(result.data())
        if df.empty:
                return ("No packages defined! \n")
        else:
                return list(df['package_name'])