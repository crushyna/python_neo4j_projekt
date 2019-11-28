from neo4j import GraphDatabase
from src.controllers.dataflow_controller import *
from src.input_check import *
from src.preloaded_data import StartingData

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "AllsoP123098"))


print("Downloading start-up data..")

drone_list = StartingData.getDroneNames()
location_list = StartingData.getLocationNames()
base_list = StartingData.getBasesNames()

main_menu = True
while main_menu:
    print("""
    Welcome to 'Skypost' Manager Application!
    // small post made fast ///

    Select one of options below:

    1.Drone management
    2.Locations management
    3.Send a package!
    4.Exit/Quit
    """)
    ans = input("What would you like to do? ")

    if ans == "1":
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
            if select1 == "1":
                print("Drones summary: \n")
                drones_summary = DroneController.getDronesSummary()
                print(drones_summary)
                time.sleep(2)

            if select1 == "2":
                print("New drone: \n")
                new_drone_name = input("Drone name: ")
                new_drone_battery_time = input("Battery time (minutes): ")
                new_drone_cargo_hold = input("Cargo hold (grams): ")
                new_drone_base = InputChecks.checkBaseName(StartingData.getBasesNames())
                new_drone_summary = DroneController.getNewDroneSummary(new_drone_name,
                                                                       new_drone_battery_time,
                                                                       new_drone_cargo_hold,
                                                                       new_drone_base)
                print(new_drone_summary)
                time.sleep(2)

            if select1 == "3":
                print("Delete drone: \n")
                delete_drone_name = InputChecks.checkDroneName(StartingData.getDroneNames())
                delete_drone = DroneController.deleteDrone(delete_drone_name)
                print(delete_drone)
                time.sleep(2)

            if select1 == "4":
                print("Change drone location: \n")
                drone_name = InputChecks.checkDroneName(StartingData.getDroneNames())
                new_location = InputChecks.checkLocationName(StartingData.getBasesNames())
                change_drone_location = DroneController.changeDroneLoc(drone_name, new_location)
                print(change_drone_location)
                time.sleep(2)

            if select1 == "5":
                drone_management = False

    elif ans == "2":
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
            if select1 == "1":
                print("Locations summary: \n")
                locations_summary = LocationController.getLocationsSummary()
                print(locations_summary)
                time.sleep(2)

            if select1 == "2":
                print("List of Skybases: \n")
                skybases_summary = LocationController.getSkybasesSummary()
                print(skybases_summary)
                time.sleep(2)

            if select1 == "3":
                print("Add Skybase: \n")
                new_location = InputChecks.checkLocationName(StartingData.getLocationNames())
                skybases_summary = LocationController.addSkybase(new_location)
                print(skybases_summary)
                time.sleep(2)

            if select1 == "4":
                print("Remove Skybase: \n")
                select_location = InputChecks.checkLocationName(StartingData.getBasesNames())
                skybases_summary = LocationController.removeSkybase(select_location)
                print(skybases_summary)
                time.sleep(2)

            if select1 == "5":
                locations_management = False

    elif ans == "3":
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
            if select1 == "1":
                print("List all packages: \n")
                packages_summary = PackageController.getPackagesSummary()
                print(packages_summary)
                time.sleep(2)

            if select1 == "2":
                print("Create new package: \n")
                new_package_summary = PackageController.createNewPackage()
                print(new_package_summary)
                time.sleep(2)

            if select1 == "3":
                print("Delete package: \n")
                if StartingData.getPackagesList() != "No packages defined! \n":
                    delete_package_name = InputChecks.checkPackagesNamesForDelete(StartingData.getPackagesList())
                    delete_drone_summary = PackageController.deletePackage(delete_package_name)
                    print(delete_drone_summary)
                    time.sleep(2)
                else:
                    print("No packages to delete!")
                    time.sleep(2)
                    continue

            if select1 == "4":
                print("Send package! \n")
                if StartingData.getPackagesListToSend() != "No packages defined! \n":
                    package_to_send = InputChecks.checkPackagesNamesForDelete(StartingData.getPackagesListToSend())
                    send_package_summary = PackageController.sendPackage(package_to_send)
                    print(send_package_summary)
                    time.sleep(2)
                else:
                    print("No packages found! Create a new package to send it!")
                    time.sleep(2)
                    continue

            if select1 == "5":
                package_manager = False

    elif ans == "4":
        driver.close()
        print("\n Goodbye!")
        main_menu = None
        time.sleep(2)

    else:
        print("\n Not valid choice, try again!")
        time.sleep(2)
