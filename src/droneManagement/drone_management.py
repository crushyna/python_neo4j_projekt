import pandas as pd
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "AllsoP123098"))
#session = driver.session()

def getDronesSummary():
    with driver.session() as session:
        result = session.run('''
                MATCH (n:Drone)-[r]->(b)
                RETURN n.name AS name, n.battery_time AS battery_time, n.cargo AS cargo_hold, b.name AS docked_at
        ''')
        return pd.DataFrame(result.data())
    
def getNewDroneSummary(drone_name, battery_time, cargo_hold, new_base):
    with driver.session() as session:
        result = session.run('''
                                MATCH (b:Loc {name:$base})
                                CREATE (p:Drone {name:$name, battery_time:$battery_time, cargo:$cargo_hold})-[:docked_at]->(b)
                                RETURN p.name AS name, p.battery_time AS battery_time, p.cargo AS cargo_hold, b.name AS docked_at
                            ''', name=drone_name, battery_time=battery_time, cargo_hold=cargo_hold, base=new_base)
        return pd.DataFrame(result.data())

def deleteDrone(drone_name):
    with driver.session() as session:
        result = session.run('''
                                MATCH (n:Drone {name:$name})
                                DETACH DELETE n
                            ''', name=drone_name)
        '''this need fixing'''
        return result.data()

def changeDroneLoc(name, new_location):
    with driver.session() as session:
        result = session.run('''
                                MATCH (n:Drone {name:$name}), (p:Loc {name:$location}), (s:Drone {name:$name})-[r]->()
                                DETACH DELETE r
                                CREATE (n)-[:docked_at]->(p)
                            ''', name=name, location=new_location)
        return pd.DataFrame(result.data())