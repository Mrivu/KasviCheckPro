import json
import os

# Import Menus
import Menus.ProfileMenu as ProfileMenu
import Menus.CheckMenu as CheckMenu

def GetVersion():
    updatesfile = open("updates.txt", "r")
    for pos, text in enumerate(updatesfile): 
        if pos in [0]: 
            return text.replace("Version: ", "")
    updatesfile.close() 

mainProfile = None
def CreateProfile(jsonfile, setAsMain = True):

    global mainProfile
    
    ClearCount = 5

    print("Creating a new profile...")

    profile = {}

    while True:
        profile["username"] = input("Enter your username: ")
        if not profile["username"]:
            print("Invalid username, please input a valid username.")
            ClearCount += 2
        elif any(p["username"] == profile["username"] for p in jsonfile):
            print("Username already exists, please input a different username.")
            ClearCount += 2
        else:
            break

    while True:
        modifiervalue = input("Enter your profile modifier (Survival modifier): ")
        if (len(modifiervalue) < 2 ):
            print("Invalid modifier, please input a valid modifier. (+/-Modifier)")
            ClearCount += 2
        elif modifiervalue[0] != "+" and modifiervalue[0] != "-":
            print("Invalid modifier, please input a valid modifier. (+/-Modifier)")
            ClearCount += 2
        elif not modifiervalue[1:].isdigit():
            print("Invalid modifier, please input a valid modifier. (+/-Modifier)")
            ClearCount += 2
        else:
            profile["modifier"] = modifiervalue
            break
    
    while True:
        multipliervalue = input("Enter your profile multiplier (Natural explorer ect.): ")
        if not (multipliervalue.isdigit()):
            print("Invalid multiplier, please enter a number. (1,2,3 etc)")
            ClearCount += 2
        else:
            profile["multiplier"] = multipliervalue
            break

    profile["inuse"] = setAsMain

    if setAsMain == True:
        mainProfile = profile

    ClearLines(ClearCount)

    jsonfile.append(profile)
    json.dump(jsonfile, open("profiles.json", "w"), indent=4)

tempLines = 0
def ClearLines(n):
    for _ in range(n):
        print("\033[A\033[K", end='')
    global tempLines
    tempLines = 0

def ClearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

mainmenuClearCount = 8
def PrintMainMenu():
    print(" --- Kasvichecker Pro ---" + "\n" +
          " -[K]- Help" + "\n" + 
          " -[K]- Profiles" + "\n" +
          " -[K]- Check" + "\n" +
          " -[K]- Import plants" + "\n" +
          " -[K]- Exit" + "\n")

def PrintHelp():
    ClearCount = 7
    print(" --- Help ---" + "\n" +
          " KEYWORDS: Type word marked with [K] to perform actions. Some keywords can be combined." + "\n" +
          " INPUTTING: Type keywords to perform actions. Capitalization can be ignored." + "\n" + 
          " QUICK EXIT: Ctrl + C closes the program at any time." + "\n" +
          " - Input anything to continue - " + "\n")
    input("Enter command: ").lower()
    return ClearCount
    
def PrintProfile():
    global mainProfile
    ClearCount = 8
    ProfileMenu.MenuText()
    while True:
        command = input("Enter command: ").lower()
        if command == "new":
            CreateProfile(profiles, False)
        elif command == "delete":
            result = ProfileMenu.DeleteProfile(profiles, mainProfile)
            if result:
                ProfileMenu.MenuText()
            else:
                ClearCount += 2
        elif command == "edit":
            ProfileMenu.EditProfile(profiles)
        elif command == "switch":
            result, mainProfile = ProfileMenu.SwitchProfile(profiles, mainProfile)
            if result:
                ProfileMenu.MenuText()
            else:
                ClearCount += 2
        elif command == "back":
            break
        else:
            ClearCount += 2
            print("Invalid command.")
    return ClearCount

def PrintImportPlants():

    ClearCount = 7 # not global

    print(" --- Import Plants ---" + "\n" +
          " - Place plant JSON file under 'ImportFolder'" + "\n")
    importFolderContents = os.listdir("ImportFolder")
    if importFolderContents:
        print(" --- Files found in 'ImportFolder': ---")
        for file in importFolderContents:
            print(" - " + file)
        print("\n" + " - Input 'IMPORT' to continue - ")
        if (input("Enter command: ") == "IMPORT"): 
            print("\n" + "Importing plants...")
            allplants = json.loads(open("allplants.json", "r").read())

            for file in importFolderContents:
                plants = json.loads(open("ImportFolder/" + file, "r").read())
                for plant in plants:
                    if any(p["name"] == plant["name"] for p in allplants):
                        print(f"Plant {plant['name']} already exists in the database, type 'w' to overwrite.")
                        if input("Enter command: ") == "w":
                            # Remove the existing plant with the same name
                            allplants = [p for p in allplants if p["name"] != plant["name"]]
                            allplants.append(plant)
                            print(f"Plant {plant['name']} was overwritten.")
                            ClearCount += 3
                        else:
                            print(f"Plant {plant['name']} was not imported.")
                            ClearCount += 3
                    else:
                        allplants.append(plant)
                        print(f"Plant {plant['name']} was imported.")
                        ClearCount += 1
            allplants = sorted(allplants, key=lambda x: x['name'])

            json.dump(allplants, open("allplants.json", "w"), indent=1)

            print("\n" + "Plants imported successfully!" + "\n" + " - Input anything to continue - ")
            input("Enter command: ")
            return ClearCount + 7
        else:
            return ClearCount + len(importFolderContents)
    else:
        print("No files found in 'ImportFolder'. Nothing to import." + "\n" + "\n"
              " - Input anything to continue - ")
        input("Enter command: ")
        return ClearCount


# Main
## Variables
mainProfile = None

if not os.path.exists("ImportFolder"):
    os.makedirs("ImportFolder")

ClearTerminal()
print(" WELCOME TO KASVICHEKER PRO - VERSION: " + GetVersion())
print(" - Created by Iivari van Uden - ")
print(" Check out the github page for the latest releases: https://github.com/Mrivu/KasviCheckPro" + "\n")

profiles = json.loads(open("profiles.json", "r").read())
if not profiles:
    print("No profiles created yet, let's get you started!")
    CreateProfile(profiles)
else:
    for profile in profiles:
        if profile["inuse"]:
            mainProfile = profile
            print("Logging in as " + profile["username"] + "...")
            break
print("Logged in as " + mainProfile["username"] + "!")
print("Type/combine keywords[k] to perform actions. Type 'Help' for more information." + "\n")
PrintMainMenu()

while True:
    command = input("Enter command: ").lower()
    if command == "help":
        ClearLines(mainmenuClearCount + tempLines)
        ClearLines(PrintHelp())
        PrintMainMenu()
    elif command == "profiles":
        ClearLines(mainmenuClearCount + tempLines)
        ClearLines(PrintProfile())
        PrintMainMenu()
    elif command == "check":
        ClearLines(mainmenuClearCount + tempLines)
        ClearLines(CheckMenu.PrintCheck(mainProfile))
        PrintMainMenu()
    elif command == "import plants":
        ClearLines(mainmenuClearCount + tempLines)
        ClearLines(PrintImportPlants())
        PrintMainMenu()
    elif command == "exit":
        print("Exiting...")
        break
    else:
        tempLines += 2
        print("Invalid command, type 'Help' for more information.")