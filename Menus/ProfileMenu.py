import json

def SwitchProfile(jsonfile, mainprofile):

    switched = False
    if len(jsonfile) < 2:
        print("You have no other profiles to switch to.")
        return mainprofile
    else:
        while not switched:
            print(" --- Profiles --- ")
            for profile in jsonfile:
                if not profile["inuse"]:
                    print(" -" + profile["username"])
            print("\n" + "What profile would you like to switch to?")
            inputProfile = input("Enter the name of the profile: ")
            
            for profile in jsonfile:
                if profile["username"] == inputProfile and mainprofile["username"] != inputProfile:
                    mainprofile["inuse"] = False
                    profile["inuse"] = True
                    mainprofile = profile
                    print("Switched to profile " + profile["username"] + "!")
                    switched = True
                    break
            else:
                print("Profile not found.")
            json.dump(jsonfile, open("profiles.json", "w"), indent=4)    
        return mainprofile

def DeleteProfile():
    pass



