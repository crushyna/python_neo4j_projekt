import pandas as pd
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "AllsoP123098"))
#session = driver.session()

def getDronesSummary():
    with driver.session() as session:
        result = session.run('''
                MATCH (n:Drone)-[r]->(b)
                RETURN n.name AS name, n.battery_time AS battery_time, n.cargo AS cargo_hold, b.name AS docked_at, n.in_travel AS in_travel
        ''')
        return pd.DataFrame(result.data())
    
def getNewDroneSummary(drone_name, battery_time, cargo_hold, new_base):
    with driver.session() as session:
        result = session.run('''
                                MATCH (b:Loc {name:$base})
                                CREATE (p:Drone {name:$name, battery_time:$battery_time, cargo:$cargo_hold, in_travel:0})-[:docked_at]->(b)
                                RETURN p.name AS name, p.battery_time AS battery_time, p.cargo AS cargo_hold, b.name AS docked_at, p.in_travel AS in_travel
                            ''', name=drone_name, battery_time=battery_time, cargo_hold=int(cargo_hold), base=new_base)
        return pd.DataFrame(result.data())

def deleteDrone(drone_name):
    with driver.session() as session:
        result = session.run('''
                                MATCH (p:Package)-[r:carried_by]->(s:Drone {name:$name})
                                SET p.in_travel = 0
                                DETACH DELETE s
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

def totalFlyTime(drone_name):
        with driver.session() as session:
                result = session.run('''
                                MATCH (n:Drone {name:$drone_name})
                                RETURN n.battery_time AS fly_time
                            ''', drone_name=drone_name)
        df = pd.DataFrame(result.data())
        return list(df['fly_time'])[0]

def totalCargoHold(drone_name):
        with driver.session() as session:
                result = session.run('''
                                MATCH (n:Drone {name:$drone_name})
                                RETURN n.cargo AS cargo_hold
                            ''', drone_name=drone_name)
        df = pd.DataFrame(result.data())
        return list(df['cargo_hold'])[0]

def getDroneCurrentBase(drone_name):
        with driver.session() as session:
                result = session.run('''
                                MATCH (n:Drone {name:$drone_name})-[r:docked_at]->(b)
                                RETURN b.name AS base_location
                            ''', drone_name=drone_name)
        df = pd.DataFrame(result.data())
        return list(df['base_location'])[0]