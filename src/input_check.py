def checkBaseName(list):
  while True:
        try:
            print(list)
            value = input("Base name: ")
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if (value not in list):
            print("Sorry, this base location doesn't exist!.")
            continue
        else:
            break
  return value

def checkLocationName(list):
  while True:
        try:
            print(list)
            value = input("New location name: ")
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if (value not in list):
            print("Sorry, this location doesn't exist!.")
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
            print("Sorry, I didn't understand that.")
            continue

        if (value not in list):
            print("Sorry, this drone doesn't exist!.")
            continue
        else:
            break
  return value