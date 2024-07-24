import json

def MenuText():
    print(" --- Profile Manager ---" + "\n" +
          " -[k]- New (Add new profile)" + "\n" +
          " -[k]- Edit (Edit existing profile)" + "\n" +
          " -[k]- Delete (Delete profile)" + "\n" + 
          " -[k]- Switch (Switch)" + "\n" +
          " -[k]- Back (Back to main menu)" + "\n")

def SwitchProfile(jsonfile, mainProfile):
    switched = False
    if len(jsonfile) < 2:
        print("You have no other profiles to switch to.")
        return False, mainProfile
    else:
        while not switched:
            print(" --- Profiles --- ")
            for profile in jsonfile:
                if not profile["inuse"]:
                    print(" -" + profile["username"])
            print("\n" + "What profile would you like to switch to?")
            inputProfile = input("Enter the name of the profile: ")
            
            for profile in jsonfile:
                if profile["username"] == inputProfile and mainProfile["username"] != inputProfile:
                    mainProfile["inuse"] = False
                    profile["inuse"] = True
                    mainProfile = profile
                    print("Switched to profile " + profile["username"] + "!" + "\n")
                    switched = True
                    break
            else:
                print("Profile not found.")
            json.dump(jsonfile, open("profiles.json", "w"), indent=4)    
        return True, mainProfile

def DeleteProfile(jsonfile, mainProfile):
    deleted = False
    if len(jsonfile) < 2:
        print("You have no other profiles to delete.")
    else:
        while not deleted:
            print(" --- Profiles --- ")
            for profile in jsonfile:
                if not profile["inuse"]:
                    print(" -" + profile["username"])
            print("\n" + "What profile would you like to delete?")
            inputProfile = input("Enter the name of the profile: ")
            
            for profile in jsonfile:
                if profile["username"] == inputProfile and mainProfile["username"] != inputProfile:
                    print("Deleted profile " + profile["username"] + "!" + "\n")
                    jsonfile.remove(profile)
                    deleted = True
                    break
            else:
                print("Profile not found.")
            json.dump(jsonfile, open("profiles.json", "w"), indent=4)    
        return True


def EditProfile(profiles):

    ClearCount = 8

    print(" --- Profiles --- ")
    for profile in profiles:
        print(" -" + profile["username"])
    print("\n" + "What profile would you like to edit?")

    while True:
        inputProfile = input("Enter the name of the profile: " + "\n")
        inputProfile = next((profile for profile in profiles if profile["username"] == inputProfile), None)
        if inputProfile:
            break
        else:
            print("Profile not found.")

    while True:
        newName = input("Enter your username (Previous: " + inputProfile["username"] + "):")
        if not inputProfile["username"]:
            print("Invalid username, please input a valid username.")
        elif any(p["username"] == inputProfile["username"] for p in profiles):
            if newName != inputProfile["username"]:
                print("Username already exists, please input a different username.")
            else:
                inputProfile["username"] = newName
                break
        else:
            inputProfile["username"] = newName
            break

    while True:
        modifiervalue = input("Enter your profile modifier (Previous: " + inputProfile["modifier"] + "): ")
        if (len(modifiervalue) < 2 ):
            print("Invalid modifier, please input a valid modifier. (+/-Modifier)")
        elif modifiervalue[0] != "+" and modifiervalue[0] != "-":
            print("Invalid modifier, please input a valid modifier. (+/-Modifier)")
        elif not modifiervalue[1:].isdigit():
            print("Invalid modifier, please input a valid modifier. (+/-Modifier)")
        else:
            profile["modifier"] = modifiervalue
            break
    
    while True:
        multipliervalue = input("Enter your profile multiplier (Previous: " + inputProfile["multiplier"] + "): ")
        if not (multipliervalue.isdigit()):
            print("Invalid multiplier, please enter a number. (1,2,3 etc)")
        else:
            inputProfile["multiplier"] = multipliervalue
            break

    json.dump(profiles, open("profiles.json", "w"), indent=4)