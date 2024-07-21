import json
import os

# Import Menus
import Menus.ProfileMenu as ProfileMenu

def GetVersion():
    updatesfile = open("updates.txt", "r")

    for pos, text in enumerate(updatesfile): 
        if pos in [0]: 
            return text.replace("Version: ", "")
    updatesfile.close() 

mainProfile = None
def CreateProfile(jsonfile, newprofile = True):

    global mainProfile
    global tempLines

    print("Creating a new profile...")

    profile = {}

    while True:
        profile["username"] = input("Enter your username: ")
        if not profile["username"]:
            print("Invalid username, please input a valid username.")
            tempLines += 2
        else:
            break

    while True:
        modifiervalue = input("Enter your profile modifier (Survival modifier): ")
        if (len(modifiervalue) < 2 ):
            print("Invalid modifier, please input a valid modifier. (+/-Modifier), lenerror")
            tempLines += 2
        elif modifiervalue[0] != "+" and modifiervalue[0] != "-":
            print("Invalid modifier, please input a valid modifier. (+/-Modifier), moderror")
            tempLines += 2
        elif not modifiervalue[1:].isdigit():
            print("Invalid modifier, please input a valid modifier. (+/-Modifier), numerror")
            tempLines += 2
        else:
            profile["modifier"] = modifiervalue
            break
    
    while True:
        multipliervalue = input("Enter your profile multiplier (Natural explorer ect.): ")
        if not (multipliervalue.isdigit()):
            print("Invalid multiplier, please enter a number. (1,2,3 etc)")
            tempLines += 2
        else:
            profile["multiplier"] = multipliervalue
            break

    profile["inuse"] = newprofile

    if newprofile == True:
        mainProfile = profile

    ClearLines(5 + tempLines)

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

mainmenuClearCount = 9
def PrintMainMenu():
    print(" --- Kasvichecker Pro ---" + "\n" +
          " -[K]- Help" + "\n" + 
          " -[K]- Profiles" + "\n" +
          " -[K]- Check" + "\n" +
          " -[K]- Import plants" + "\n" +
          " -[K]- Edit plants" + "\n" +
          " -[K]- Exit" + "\n")

helpClearCount = 6
def PrintHelp():
    print(" --- Help ---" + "\n" +
          " KEYWORDS: Type word marked with [K] to perform actions. Some keywords can be combined." + "\n" +
          " INPUTTING: Type keywords to perform actions. Capitalization can be ignored." + "\n" + 
          " - Input anything to continue - " + "\n")
    input("Enter command: ").lower()
    ClearLines(helpClearCount)
    PrintMainMenu()
    
profileClearCount = 7
def PrintProfile():
    global tempLines, mainProfile
    print(" --- Profile Manager ---" + "\n" +
          " -[k]- New (Add new profile)" + "\n" +
          " -[k]- Delete (Delete profile)" + "\n" + 
          " -[k]- Switch (Switch)" + "\n" +
          " -[k]- Back (Back to main menu)" + "\n")
    while True:
        command = input("Enter command: ").lower()
        if command == "new":
            CreateProfile(profiles, False)
        elif command == "delete":
            ClearLines(profileClearCount + tempLines)
            ProfileMenu.DeleteProfile(profiles)
        elif command == "switch":
            ClearLines(profileClearCount + tempLines)
            mainProfile = ProfileMenu.SwitchProfile(profiles, mainProfile)
        elif command == "back":
            ClearLines(profileClearCount + tempLines)
            PrintMainMenu()
            break
        else:
            tempLines += 2
            print("Invalid command.")

# Main
## Variables
mainProfile = None

ClearTerminal()
print(" WELCOME TO KASVICHEKER PRO - VERSION: " + GetVersion())
print(" - Created by Iivari van Uden - ")
print(" Check out the github page for the latest releases: link" + "\n")

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
        PrintHelp()
    elif command == "profiles":
        ClearLines(mainmenuClearCount + tempLines)
        PrintProfile()
    elif command == "check":
        print("Check menu")
    elif command == "import plants":
        print("Import plants menu")
    elif command == "edit plants":
        print("Edit plants menu")
    elif command == "exit":
        print("Exiting...")
        break
    else:
        tempLines += 2
        print("Invalid command, type 'Help' for more information.")