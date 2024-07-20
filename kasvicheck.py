import json
import os

def GetVersion():
    updatesfile = open("updates.txt", "r")

    for pos, text in enumerate(updatesfile): 
        if pos in [0]: 
            return text.replace("Version: ", "")
    updatesfile.close() 

def CreateProfile(jsonfile):
    print("Creating a new profile...")

    profile = {}
    profile["name"] = input("Enter profile name: ")
    profile["modifier"] = input("Enter your profile modifier (Survival modifier): ")
    profile["multiplier"] = input("Enter your profile multiplier (Natural explorer ect.): ")
    profile["inuse"] = True

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
helpExit = "any"    
def PrintHelp():
    print(" --- Help ---" + "\n" +
          " KEYWORDS: Type word marked with [K] to perform actions. Some keywords can be combined." + "\n" +
          " INPUTTING: Type keywords to perform actions. Capitalization can be ignored." + "\n" + 
          " - Input anything to continue - " + "\n")

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
            print("Logging in as " + profile["name"] + "...")
            break
print("Logged in as " + mainProfile["name"] + "!")
print("Type/combine keywords[k] to perform actions. Type 'Help' for more information." + "\n")
PrintMainMenu()

while True:
    command = input("Enter command: ").lower()
    if command == "help":
        ClearLines(mainmenuClearCount + tempLines)
        PrintHelp()
        input("Enter command: ").lower()
        ClearLines(helpClearCount)
        PrintMainMenu()
    elif command == "profiles":
        print("Profiles menu")
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