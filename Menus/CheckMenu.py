import random

def PrintCheck(mainprofile):
    print(" --- Check for plants ---" + "\n" +
          " - " + str(mainprofile['username']) + "'s modfier: " + str(mainprofile["modifier"]) + "\n" +
          " - " + str(mainprofile['username']) + "'s multiplier: " + str(mainprofile["multiplier"]) + "\n")
    modifiervalue = input("Additional modifier (leave blank if no additional modifiers): ")
    if (len(modifiervalue) != 0 and len(modifiervalue) < 2):
        print("Invalid modifier, please input a valid modifier. (+/-Modifier)")
        tempLines += 2
    elif (len (modifiervalue) == 0):
        modifiervalue = 0
    elif modifiervalue[0] != "+" and modifiervalue[0] != "-":
        print("Invalid modifier, please input a valid modifier. (+/-Modifier)")
        tempLines += 2
    elif not modifiervalue[1:].isdigit():
        print("Invalid modifier, please input a valid modifier. (+/-Modifier)")
        tempLines += 2
    else:
        if (modifiervalue[0] == "+"):
            modifiervalue = int(modifiervalue[1:])
        else:
            modifiervalue = int(modifiervalue[1:]) * -1
    if (mainprofile["modifier"][0] == "+"):
        mainprofilemodifier = int(mainprofile["modifier"][1:])
    else:
        mainprofilemodifier = int(mainprofile["modifier"][1:]) * -1

    totalModifier = mainprofilemodifier + modifiervalue
    sign = "+" if totalModifier > 0 else ""
    print("\n" + " -- Total modifier: " + sign + str(totalModifier) + " --" + "\n")
    input(" - Roll the dice > ENTER < ")     
    result = random.randint(1, 20) + totalModifier
    print(" - You rolled a " + str(result) + "!" + "\n") 

    # Plant discovery logic
    ## The higher the roll, the larger the chance of discovering rare plants.

   
