import json

def MenuText():
    print(" --- Profile Manager ---" + "\n" +
          " -[k]- New (Add new profile)" + "\n" +
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



