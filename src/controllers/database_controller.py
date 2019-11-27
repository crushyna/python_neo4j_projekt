import pandas as pd
import time
from neo4j import GraphDatabase
from src.input_check import InputChecks
from src.preloaded_data import StartingData

# TODO: get connection info from file, and make it more versatile!
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "AllsoP123098"))


class DroneController():

    @staticmethod
    def getDronesSummary():
        with driver.session() as session:
            result = session.run('''
                    MATCH (n:Drone)-[r]->(b)
                    RETURN n.name AS name, n.battery_time AS battery_time, n.cargo AS cargo_hold, b.name AS docked_at, n.in_travel AS in_travel
            ''')
            return pd.DataFrame(result.data())

    @staticmethod
    def getNewDroneSummary(drone_name, battery_time, cargo_hold, new_base):
        with driver.session() as session:
            result = session.run('''
                                    MATCH (b:Loc {name:$base})
                                    CREATE (p:Drone {name:$name, battery_time:$battery_time, cargo:$cargo_hold, in_travel:0})-[:docked_at]->(b)
                                    RETURN p.name AS name, p.battery_time AS battery_time, p.cargo AS cargo_hold, b.name AS docked_at, p.in_travel AS in_travel
                                ''', name=drone_name, battery_time=battery_time, cargo_hold=int(cargo_hold),
                                 base=new_base)
            return pd.DataFrame(result.data())

    @staticmethod
    def deleteDrone(drone_name):
        with driver.session() as session:
            result = session.run('''
                                    MATCH (p:Package)-[r:carried_by]->(s:Drone {name:$name})
                                    SET p.in_travel = 0
                                    DETACH DELETE s
                                ''', name=drone_name)
            '''this need fixing'''
            return result.data()

    @staticmethod
    def changeDroneLoc(name, new_location):
        with driver.session() as session:
            result = session.run('''
                                    MATCH (n:Drone {name:$name}), (p:Loc {name:$location}), (s:Drone {name:$name})-[r]->()
                                    DETACH DELETE r
                                    CREATE (n)-[:docked_at]->(p)
                                ''', name=name, location=new_location)
            return pd.DataFrame(result.data())

    @staticmethod
    def totalFlyTime(drone_name):
        with driver.session() as session:
            result = session.run('''
                                    MATCH (n:Drone {name:$drone_name})
                                    RETURN n.battery_time AS fly_time
                                ''', drone_name=drone_name)
        df = pd.DataFrame(result.data())
        return list(df['fly_time'])[0]

    @staticmethod
    def totalCargoHold(drone_name):
        with driver.session() as session:
            result = session.run('''
                                    MATCH (n:Drone {name:$drone_name})
                                    RETURN n.cargo AS cargo_hold
                                ''', drone_name=drone_name)
        df = pd.DataFrame(result.data())
        return list(df['cargo_hold'])[0]

    @staticmethod
    def getDroneCurrentBase(drone_name):
        with driver.session() as session:
            result = session.run('''
                                    MATCH (n:Drone {name:$drone_name})-[r:docked_at]->(b)
                                    RETURN b.name AS base_location
                                ''', drone_name=drone_name)
        df = pd.DataFrame(result.data())
        return list(df['base_location'])[0]


class LocationController():

    @staticmethod
    def getLocationsSummary():
        with driver.session() as session:
            result = session.run('''
                    MATCH (n:Loc) 
                    RETURN n.name AS name
            ''')
            return pd.DataFrame(result.data())

    @staticmethod
    def getSkybasesSummary():
        with driver.session() as session:
            result = session.run('''
                    MATCH (n:Loc {base:1}) 
                    RETURN n.name AS name, n.base AS is_skybase
            ''')
            return pd.DataFrame(result.data())

    @staticmethod
    def addSkybase(location_name):
        with driver.session() as session:
            result = session.run('''
                                    MATCH (n:Loc {name:$name})
                                    SET n.base = 1
                                    RETURN n.name AS name, n.base AS is_skybase
                                ''', name=location_name)
            return result.data()

    @staticmethod
    def removeSkybase(location_name):
        with driver.session() as session:
            result = session.run('''
                                    MATCH (n:Loc {name:$name})
                                    REMOVE n.base
                                    RETURN n.name AS name, n.base AS is_skybase
                                ''', name=location_name)
            return result.data()


class PackageController():

    @staticmethod
    def getPackagesSummary():
        with driver.session() as session:
            result = session.run('''
                    MATCH (a)<-[r:delivery_from]-(n:Package)-[s:delivery_to]->(b)
                    RETURN n.name AS package_name, n.weight AS package_weight, a.name AS delivery_from, b.name AS delivery_to, n.in_travel AS in_travel
                    ''')
            return pd.DataFrame(result.data())

    @staticmethod
    def createNewPackage():
        while True:
            name = InputChecks.checkPackagesNames(StartingData.getPackagesList())
            weight = InputChecks.checkPackageWeight()
            start = InputChecks.checkStartPoint(StartingData.getLocationNames())
            dest = InputChecks.checkDestinationPoint(StartingData.getLocationNames())
            if start == dest:
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
                    break  # TODO: try to fix this 'break' issue here
        return pd.DataFrame(result.data())

    @staticmethod
    def deletePackage(package_name):
        # TODO: revisit this method
        with driver.session() as session:
            result1 = session.run('''
                                    MATCH (n:Package {name:$name})-[r:carried_by]->(d)
                                    SET d.in_travel=0
                                ''', name=package_name)
            '''this need fixing'''
            result2 = session.run('''
                                    MATCH (n:Package {name:$name})
                                    DETACH DELETE n
                                ''', name=package_name)
            '''this need fixing'''
            return result2.data()

    @staticmethod
    def sendPackage(name):
        while True:
            package_name = name
            weight = PackageController.getPackageWeight(name)
            start = PackageController.getPackageStart(name)
            dest = PackageController.getPackageDestination(name)
            selected_drone = InputChecks.checkDroneName(StartingData.getDroneNamesToFly())
            drone_total_fly_time = DroneController.totalFlyTime(selected_drone)
            drone_total_cargo = DroneController.totalCargoHold(selected_drone)
            if weight > drone_total_cargo:
                print("Package is too heavy. Change the drone. \n")
                break

            drone_current_base = DroneController.getDroneCurrentBase(selected_drone)
            fly_time_drone_to_pickup = PackageController.getFlyTimeForPickup(drone_current_base, start)
            package_fly_time_to_cover = PackageController.getPackageFlyTime(start, dest)
            fly_time_drone_to_return = PackageController.getFlyTimeForReturn(dest, drone_current_base)
            total_required_fly_time = fly_time_drone_to_pickup + package_fly_time_to_cover + fly_time_drone_to_return
            print("Total required fly time: ")
            print(total_required_fly_time)
            if int(total_required_fly_time) > int(drone_total_fly_time):
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
                                    SET p.in_travel = 1
                                    CREATE (p)-[:carried_by]->(n)
                                    RETURN n.name AS drone_name, p.name AS package_name, a.name AS delivered_from, b.name AS delivered_to
                                ''', drone_name=selected_drone, package_name=package_name)
                return pd.DataFrame(result.data())

    @staticmethod
    def getPackageWeight(name):
        with driver.session() as session:
            result = session.run('''
                                    MATCH (a)<-[r:delivery_from]-(n:Package {name:$name})-[s:delivery_to]->(b)
                                    RETURN n.weight AS package_weight
                                ''', name=name)
            df = pd.DataFrame(result.data())
            return list(df['package_weight'])[0]

    @staticmethod
    def getPackageStart(name):
        with driver.session() as session:
            result = session.run('''
                                    MATCH (a)<-[r:delivery_from]-(n:Package {name:$name})-[s:delivery_to]->(b)
                                    RETURN a.name AS delivery_from
                                ''', name=name)
            df = pd.DataFrame(result.data())
            return list(df['delivery_from'])[0]

    @staticmethod
    def getPackageDestination(name):
        with driver.session() as session:
            result = session.run('''
                                    MATCH (a)<-[r:delivery_from]-(n:Package {name:$name})-[s:delivery_to]->(b)
                                    RETURN b.name AS delivery_to
                                ''', name=name)
            df = pd.DataFrame(result.data())
            return list(df['delivery_to'])[0]

    @staticmethod
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
            print("Delivery fly-path: ")
            print(df['places'].values[0])
            time.sleep(2)
            return df['totalCost'].values[0]

    @staticmethod
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
            print("Pick-up fly-path: ")
            print(df['places'].values[0])
            time.sleep(2)
            return df['totalCost'].values[0]

    @staticmethod
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
            print("Return to base fly-path: ")
            print(df['places'].values[0])
            time.sleep(2)
            return df['totalCost'].values[0]
