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
        session.close()
        return pd.DataFrame(result.data())
    
def getNewDroneSummary(drone_name, battery_time, cargo_hold, new_base):
    with driver.session() as session:
        result = session.run('''
                            MERGE (nextDrone:Drone {name:$name, battery_time:$battery_time, cargo:$cargo_hold})
                            MERGE (nextDrone)-[:docked_at]->(a:Loc {name:$base})
                            RETURN nextDrone.name AS name, nextDrone.battery_time AS battery_time, nextDrone.cargo AS cargo_hold
                            ''', name=drone_name, battery_time=battery_time, cargo_hold=cargo_hold, base=new_base)
        return pd.DataFrame(result.data())

def deleteDrone(drone_name):
    with driver.session() as session:
        result = session.run('''
                            MATCH (n:Drone {name:$name})
                            DELETE n
                            ''', name=drone_name)
        '''this need fixing'''
        return result.data()