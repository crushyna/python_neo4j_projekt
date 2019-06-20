import pandas as pd
import time
from src.preloaded_data import getDroneNames
from src.preloaded_data import getLocationNames
from src.preloaded_data import getBasesNames
from src.preloaded_data import getPackagesList
from src.droneManagement.drone_management import getDronesSummary
from src.droneManagement.drone_management import getNewDroneSummary
from src.droneManagement.drone_management import deleteDrone
from src.droneManagement.drone_management import changeDroneLoc
from src.locationManagement.location_management import getLocationsSummary
from src.locationManagement.location_management import getSkybasesSummary
from src.locationManagement.location_management import addSkybase
from src.locationManagement.location_management import removeSkybase
from src.packageManagement.package_manager import createNewPackage
from src.packageManagement.package_manager import getPackagesSummary
from src.packageManagement.package_manager import deletePackage
from src.packageManagement.package_manager import sendPackage
from src.input_check import checkBaseName
from src.input_check import checkDroneName
from src.input_check import checkLocationName
from src.input_check import checkPackagesNamesForDelete

drone_list = getDroneNames()
location_list = getLocationNames()
base_list = getBasesNames()

print("Downloading start-up data..")

main_menu = True
while main_menu:
    print("""
    Welcome to 'Skypost' Manager Application!
    // small post made fast ///

    Select one of options below:

    1.Drone management
    2.Locations management
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
          new_drone_base = checkBaseName(getBasesNames())
          new_drone_summary = getNewDroneSummary(new_drone_name, new_drone_battery_time, new_drone_cargo_hold, new_drone_base)
          print(new_drone_summary)
          time.sleep(2)

        if select1=="3":
          print("Delete drone: \n")
          delete_drone_name = checkDroneName(getDroneNames())
          delete_drone = deleteDrone(delete_drone_name)
          print(delete_drone)
          time.sleep(2)

        if select1=="4":
          print("Change drone location: \n")
          drone_name = checkDroneName(getDroneNames())
          new_location = checkLocationName(getBasesNames())
          change_drone_location = changeDroneLoc(drone_name, new_location)
          print(change_drone_location)
          time.sleep(2)

        if select1=="5":
          drone_management = False

    elif ans=="2":
      print("\n Locations management: ")
      locations_management = True
      while locations_management:
        print(
          '''
          Select option:
          1. Locations summary
          2. List of Skybases
          3. Add Skybase
          4. Remove Skybase
          5. Return to Main menu
          '''
          )
        select1 = input("What would you like to do? ")
        if select1=="1":
          print("Locations summary: \n")
          locations_summary = getLocationsSummary()
          print(locations_summary)
          time.sleep(2)

        if select1=="2":
          print("List of Skybases: \n")
          skybases_summary = getSkybasesSummary()
          print(skybases_summary)
          time.sleep(2)

        if select1=="3":
          print("Add Skybase: \n")
          new_location = checkLocationName(getLocationNames())
          skybases_summary = addSkybase(new_location)
          print(skybases_summary)
          time.sleep(2)

        if select1=="4":
          print("Remove Skybase: \n")
          select_location = checkLocationName(getBasesNames())
          skybases_summary = removeSkybase(select_location)
          print(skybases_summary)
          time.sleep(2)
        
        if select1=="5":
          locations_management = False

    elif ans=="3":
      print("\n Send a package:")
      package_manager = True
      while package_manager:
        print(
          '''
          Select option:
          1. List all packages
          2. Create new package
          3. Delete package
          4. Send package!
          5. Return to Main menu
          ''')
        select1 = input("What would you like to do? ")
        if select1=="1":
          print("List all packages: \n")
          packages_summary = getPackagesSummary()
          print(packages_summary)
          time.sleep(2)

        if select1=="2":
          print("Create new package: \n")
          new_package_summary = createNewPackage()
          print(new_package_summary)
          time.sleep(2)

        if select1=="3":
          print("Delete package: \n")
          if (getPackagesList() != ("No packages defined! \n")):
            delete_package_name = checkPackagesNamesForDelete(getPackagesList())
            delete_drone_summary = deletePackage(delete_package_name)
            print(delete_drone_summary)
            time.sleep(2)
          else:
            print("No packages to delete!")
            time.sleep(2)
            continue

        if select1=="4":
          print("Send package! \n")
          if (getPackagesList() != ("No packages defined! \n")):
            package_to_send = checkPackagesNamesForDelete(getPackagesList())
            send_package_summary = sendPackage(package_to_send)
            print(send_package_summary)
            time.sleep(2)
          else:
            print("No packages found! Create a new package to send it!")
            time.sleep(2)
            continue

        if select1=="5":
          package_manager = False








    elif ans=="4":
      print("\n Refresh data: ")
      print("Data refreshed! \n")
      time.sleep(2)

    elif ans=="5":
      print("\n Goodbye!")
      main_menu = None

    else:
       print("\n Not Valid Choice Try again")