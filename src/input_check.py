import time

def checkBaseName(list):
  while True:
        try:
            print(list)
            value = input("Base name: ")
        except ValueError:
            print("Sorry, I didn't understand that. \n")
            continue

        if (value not in list):
            print("Sorry, this base location doesn't exist!. \n")
            time.sleep(2)
            continue
        else:
            break
  return value

def checkLocationName(list):
  while True:
        try:
            print(list)
            value = input("Location name: ")
        except ValueError:
            print("Sorry, I didn't understand that. \n")
            continue

        if (value not in list):
            print("Sorry, this location doesn't exist!. \n")
            time.sleep(2)
            continue
        else:
            break
  return value

def checkDroneName(list):
  while True:
        try:
            print(list)
            value = input("Drone name: ")
        except ValueError:
            print("Sorry, I didn't understand that. \n")
            continue

        if (value not in list):
            print("Sorry, this drone doesn't exist!. \n")
            time.sleep(2)
            continue
        else:
            break
  return value

def checkPackageWeight():
  while True:
        try:
            value = int(input("Package weight (grams): "))
        except ValueError:
            print("Sorry, but that's not a number (int). \n")
            continue

        if (value < 1):
            print("Sorry, but package must weight at least 1 gram! \n")
            time.sleep(2)
            continue
        else:
            break
  return value

def checkStartPoint(list):
    while True:
        try:
            print(list)
            value = input("Start location: ")
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if (value not in list):
            print("Sorry, this location doesn't exist!. \n")
            time.sleep(2)
            continue
        else:
            break
    return value

def checkDestinationPoint(list):
    while True:
        try:
            print(list)
            value = input("Destination: ")
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if (value not in list):
            print("Sorry, this location doesn't exist!. \n")
            time.sleep(2)
            continue
        else:
            break
    return value

def checkPackagesNames(list):
  while True:
        try:
            print(list)
            value = input("Enter package unique name: ")
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if (value in list):
            print("Sorry, this package already exist!. \n")
            time.sleep(2)
            continue
        else:
            break
  return value

def checkPackagesNamesForDelete(list):
    while True:
        try:
            print(list)
            value = input("Enter package name: ")
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if (value not in list):
            print("Sorry, this package doesn't exist!. \n")
            time.sleep(2)
            continue
        else:
            break
    return value