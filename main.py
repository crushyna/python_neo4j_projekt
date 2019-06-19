import pandas as pd
import time
#from neo4j import GraphDatabase
from src.preloaded_data import getDroneNames
from src.preloaded_data import getLocationNames
from src.drone_management import getDronesSummary
from src.drone_management import getNewDroneSummary
from src.drone_management import deleteDrone

def refreshData():
  drone_names = list(getDroneNames()['drone_name'])
  #print(drone_names)
  location_names = list(getLocationNames()['location_name'])
  #print(location_names)

#uri = "bolt://localhost:7687"
#driver = GraphDatabase.driver(uri, auth=("neo4j", "AllsoP123098"))
#session = driver.session()

drone_names = []
location_names = []

print("Downloading start-up data..")
refreshData()

main_menu = True
while main_menu:
    print("""
    Welcome to 'Skypost' Manager Application!
    // small post made fast ///

    Select one of options below:

    1.Drone management
    2.Locations summary
    3.Send a package!
    4.Refresh data
    5.Exit/Quit
    """)
    ans=input("What would you like to do? ")

    if ans=="1":
      print("\n Drone management:")
      drone_management = True
      while drone_management:
        print(
          '''
          Select option:
          1. Get drones summary
          2. Add new drone
          3. Delete drone
          4. Change drone location
          5. Return to Main menu
          ''')
        select1 = input("What would you like to do? ")
        if select1=="1":
          print("Drones summary: \n")
          drones_summary = getDronesSummary()
          print(drones_summary)
          time.sleep(2)

        if select1=="2":
          print("New drone: \n")
          new_drone_name = input("Drone name: ")
          new_drone_battery_time = input("Battery time (minutes): ")
          new_drone_cargo_hold = input("Cargo hold (grams): ")
          new_drone_base = input("Base name: ")
          new_drone_summary = getNewDroneSummary(new_drone_name, new_drone_battery_time, new_drone_cargo_hold, new_drone_base)
          print(new_drone_summary)
          time.sleep(2)

        if select1=="3":
          print("Delete drone: \n")
          delete_drone_name = input("Drone name: ")
          delete_drone = deleteDrone(delete_drone_name)
          print(delete_drone)
          time.sleep(2)

        if select1=="5":
          drone_management = False

    elif ans=="2":
      print("\n Locations summary: ")

    elif ans=="3":
      print("\n Send a package:")

    elif ans=="4":
      print("\n Refresh data: ")
      refreshData()
      print("Data refreshed! \n")
      time.sleep(2)

    elif ans=="5":
      print("\n Goodbye!")
      main_menu = None

    else:
       print("\n Not Valid Choice Try again")