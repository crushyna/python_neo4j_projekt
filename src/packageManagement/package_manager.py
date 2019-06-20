import time
import pandas as pd
from neo4j import GraphDatabase
from src.input_check import checkPackageWeight
from src.input_check import checkStartPoint
from src.input_check import checkDestinationPoint
from src.input_check import checkPackagesNames
from src.preloaded_data import getLocationNames
from src.preloaded_data import getPackagesList
from src.input_check import checkDroneName
from src.preloaded_data import getDroneNames
from src.droneManagement.drone_management import totalFlyTime
from src.droneManagement.drone_management import totalCargoHold
from src.droneManagement.drone_management import getDroneCurrentBase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "AllsoP123098"))

def getPackagesSummary():
    with driver.session() as session:
        result = session.run('''
                MATCH (a)<-[r:delivery_from]-(n:Package)-[s:delivery_to]->(b)
                RETURN n.name AS package_name, n.weight AS package_weight, a.name AS delivery_from, b.name AS delivery_to, n.in_travel AS in_travel
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
                                CREATE (a)<-[:delivery_from]-(z:Package {name:$name, weight:$weight, in_travel:0})-[:delivery_to]->(b)
                                RETURN z.name AS package_name, z.weight AS weight, a.name AS from_location, b.name AS to_location
                                ''', name=name, start=start, dest=dest, weight=weight)
                return pd.DataFrame(result.data())
            break
    return pd.DataFrame(result.data())

def deletePackage(package_name):
    with driver.session() as session:
        result1 = session.run('''
                                MATCH (n:Package {name:$name})-[r:carried_by]->(d)
                                SET d.in_travel=0
                            ''', name=package_name)
        '''this need fixing'''
        #return result1.data()
        result2 = session.run('''
                                MATCH (n:Package {name:$name})
                                DETACH DELETE n
                            ''', name=package_name)
        '''this need fixing'''
        return result2.data()

def sendPackage(name):
    while True:
        package_name = name
        weight = getPackageWeight(name)
        start = getPackageStart(name)
        dest = getPackageDestination(name)
        selected_drone = checkDroneName(getDroneNames())
        drone_total_fly_time = totalFlyTime(selected_drone)
        drone_total_cargo = totalCargoHold(selected_drone)
        if (weight > drone_total_cargo):
            print("Package is too heavy. Change the drone. \n")
            break
        
        drone_current_base = getDroneCurrentBase(selected_drone)
        fly_time_drone_to_pickup = getFlyTimeForPickup(drone_current_base, start)
        fly_time_drone_to_return = getFlyTimeForReturn(dest, drone_current_base)
        package_fly_time_to_cover = getPackageFlyTime(start, dest)
        total_required_fly_time = fly_time_drone_to_pickup + package_fly_time_to_cover + fly_time_drone_to_return
        print("Total required fly time: ")
        print(total_required_fly_time)
        if (int(total_required_fly_time) > int(drone_total_fly_time)):
            print("Drone has too small battery. Fly time is too short to deliver a package. Change the drone. \n")
            break
        else:
            '''
            Connect package to a specific drone
            '''
            with driver.session() as session:
                result = session.run('''
                                MATCH (n:Drone {name:$drone_name}), (a)<-[r:delivery_from]-(p:Package {name:$package_name})-[s:delivery_to]->(b)
                                SET n.in_travel = 1
                                CREATE (p)-[:carried_by]->(n)
                                RETURN n.name AS drone_name, p.name AS package_name, a.name AS delivered_from, b.name AS delivered_to
                            ''', drone_name=selected_drone, package_name=package_name)
            return pd.DataFrame(result.data())

def getPackageWeight(name):
    with driver.session() as session:
        result = session.run('''
                                MATCH (a)<-[r:delivery_from]-(n:Package {name:$name})-[s:delivery_to]->(b)
                                RETURN n.weight AS package_weight
                            ''', name=name)
        df = pd.DataFrame(result.data())
        return list(df['package_weight'])[0]


def getPackageStart(name):
    with driver.session() as session:
        result = session.run('''
                                MATCH (a)<-[r:delivery_from]-(n:Package {name:$name})-[s:delivery_to]->(b)
                                RETURN a.name AS delivery_from
                            ''', name=name)
        df = pd.DataFrame(result.data())
        return list(df['delivery_from'])[0]


def getPackageDestination(name):
    with driver.session() as session:
        result = session.run('''
                                MATCH (a)<-[r:delivery_from]-(n:Package {name:$name})-[s:delivery_to]->(b)
                                RETURN b.name AS delivery_to
                            ''', name=name)
        df = pd.DataFrame(result.data())
        return list(df['delivery_to'])[0]

def getPackageFlyTime(start, dest):
    with driver.session() as session:
        result = session.run('''
                                MATCH (start:Loc{name:$start_loc}), (end:Loc{name:$dest_loc})
                                CALL algo.kShortestPaths.stream(start, end, 1, 'cost' ,{
                                nodeQuery:'MATCH(n:Loc) RETURN id(n) as id',
                                relationshipQuery:'MATCH (n:Loc)-[r:TIME]-(m:Loc) WITH id(n) AS sources, id(m) AS targets, r.cost AS costs RETURN sources as source, targets as target, costs as weight',
                                graph:'cypher',writePropertyPrefix:'cypher_'})
                                YIELD index, nodeIds, costs
                                RETURN [node in algo.getNodesById(nodeIds) | node.name] AS places,costs, reduce(acc = 0.0, cost in costs | acc + cost) AS totalCost
                                ''', start_loc=start, dest_loc=dest)
        df = pd.DataFrame(result.data())
        return df['totalCost'].values[0]

def getFlyTimeForPickup(start, dest):
    with driver.session() as session:
        result = session.run('''
                                MATCH (start:Loc{name:$start_loc}), (end:Loc{name:$dest_loc})
                                CALL algo.kShortestPaths.stream(start, end, 1, 'cost' ,{
                                nodeQuery:'MATCH(n:Loc) RETURN id(n) as id',
                                relationshipQuery:'MATCH (n:Loc)-[r:TIME]-(m:Loc) WITH id(n) AS sources, id(m) AS targets, r.cost AS costs RETURN sources as source, targets as target, costs as weight',
                                graph:'cypher',writePropertyPrefix:'cypher_'})
                                YIELD index, nodeIds, costs
                                RETURN [node in algo.getNodesById(nodeIds) | node.name] AS places,costs, reduce(acc = 0.0, cost in costs | acc + cost) AS totalCost
                                ''', start_loc=start, dest_loc=dest)
        df = pd.DataFrame(result.data())
        return df['totalCost'].values[0]

def getFlyTimeForReturn(start, dest):
    with driver.session() as session:
        result = session.run('''
                                MATCH (start:Loc{name:$start_loc}), (end:Loc{name:$dest_loc})
                                CALL algo.kShortestPaths.stream(start, end, 1, 'cost' ,{
                                nodeQuery:'MATCH(n:Loc) RETURN id(n) as id',
                                relationshipQuery:'MATCH (n:Loc)-[r:TIME]-(m:Loc) WITH id(n) AS sources, id(m) AS targets, r.cost AS costs RETURN sources as source, targets as target, costs as weight',
                                graph:'cypher',writePropertyPrefix:'cypher_'})
                                YIELD index, nodeIds, costs
                                RETURN [node in algo.getNodesById(nodeIds) | node.name] AS places,costs, reduce(acc = 0.0, cost in costs | acc + cost) AS totalCost
                                ''', start_loc=start, dest_loc=dest)
        df = pd.DataFrame(result.data())
        return df['totalCost'].values[0]