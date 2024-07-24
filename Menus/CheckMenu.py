import os
import random
import math
import json

import Menus.resultTable as resultTable
import Menus.General as General


def PrintCheck(mainprofile):

    ClearCount = 14

    config = json.loads(open("config.json", "r").read())

    print(" --- Check for plants ---" + "\n" +
          " - " + str(mainprofile['username']) + "'s modfier: " + str(mainprofile["modifier"]) + "\n" +
          " - " + str(mainprofile['username']) + "'s multiplier: " + str(mainprofile["multiplier"]) + "\n")
    
    ## Additional modifiers
    modifiervalue, returnLines = General.CheckIfModifier("Additional modifier (leave blank if no additional modifiers): ", "Invalid modifier, please input a valid modifier. (+/-Modifier)")
    ClearCount += returnLines

    validAreas = ["Arctic","Coast","Desert","Plains","Forest","Mountain","Swamp","Jungle","Cave","Depths"]
    validRegions = ["Jyrnimm", "Ekobis", "Amalra", "Worngar", "Arcalus", "Ylaidya", "Ellaria"]

    ## Check area and region
    if (config["defaultArea"] not in validAreas):
        while True:
            area = input("Enter the area you are in: ")
            ClearCount += 1
            if area not in validAreas:
                print("Invalid area, please input a valid area.")
                print("Valid areas: " + ", ".join(validAreas))
                ClearCount += 2
            else:
                break
    else:
        area = config["defaultArea"]

    if (config["defaultRegion"] not in validRegions):     
        while True:
            region = input("Enter the region you are in: ")
            ClearCount += 1
            if region not in validRegions:
                print("Invalid area, please input a valid region.")
                print("Valid areas: " + ", ".join(validRegions))
                ClearCount += 2
            else:
                break
    else:
        region = config["defaultRegion"]   
    
    ## Check availability
    availability, returnLines = General.CheckIfModifier("Plant availability (leave blank for Standard): ", "Invalid availability, please enter a modifier (+/- value).")
    ClearCount += returnLines

    mainprofilemodifier = General.ReturnModifierValue(mainprofile["modifier"])

    totalModifier = mainprofilemodifier + modifiervalue
    sign = "+" if totalModifier > 0 else ""
    
    print("\n" + " -- Total modifier: " + sign + str(totalModifier) + " --" + "\n")

    ## Handle dice roll
    if (config["selfRoll"]):
        while True:
            value = input(" - What did you roll (Base die)? > ")
            if value.isdigit():
                result = int(value) + totalModifier
                print(" - You rolled a " + str(result) + "!" + "\n") 
                break
            else:
                print("Invalid input, please input a valid number.")
                ClearCount += 2
    else:
        input(" - Roll the dice > ENTER < ")     
        result = random.randint(1, 20) + totalModifier
        print(" - You rolled a " + str(result) + "!" + "\n") 

    # Plant discovery logic
    ## The higher the roll, the larger the chance of discovering rare plants.
    rollResults = {
    entry["Roll"]: {
        "Common": entry["Common"],
        "Uncommon": entry["Uncommon"],
        "Rare": entry["Rare"],
        "Very rare": entry["Very rare"],
        "Legendary": entry["Legendary"]
    } for entry in resultTable.rollresults
    }

    plantAmount = math.floor(result / 10)
    ## Check nat 20
    if (result -  totalModifier) == 20:
        plantAmount += 1
    plantAmount = (plantAmount + availability) * int(mainprofile["multiplier"])

    if (result > 40):
        result = 40
    elif (result < 0 ):
        result = 1

    if (rollResults[result]["Common"] > 0 and plantAmount > 0):
        rarityResults = random.choices(["Common","Uncommon","Rare","Very Rare","Legendary"],weights=(rollResults[result]["Common"], rollResults[result]["Uncommon"], rollResults[result]["Rare"], rollResults[result]["Very rare"], rollResults[result]["Legendary"]), k=plantAmount)  
        
        allplants = json.loads(open("allplants.json", "r").read())
        checkResults = []

        for r in rarityResults:
            matchedPlants = [plant for plant in allplants if plant["rarity"] == r and area in plant["Area"] and region in plant["Region"]]
            plantPull = random.choice(matchedPlants)
            checkResults.append(plantPull)
            print(" - " + plantPull["name"] + " plant discovered!")
            ClearCount += 1
        ExportResults(checkResults, config, result, area, region, availability)
        input("\n" + " - Enter anything to continue:  ")
        return ClearCount     
    else:
        ClearCount += 1
        print(" - You didn't find any plants." + "\n")
        input( " - Enter anything to continue:  ")
        return ClearCount

def ExportResults(checkResults, config, roll, area, region, availability):
    if (config["downloadCheckResults"]):

        folder_path = os.path.join(os.getcwd(), "CheckResults")

        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        filenum = len(files) + 1

        file_path = os.path.join(folder_path, "CheckResults["+ str(filenum) +"].txt")

        plantContent = []
        for p in checkResults:
            plantContent.append("Plant name: " + p["name"] + "\n" +
                                "Plant rarity: " + p["rarity"] + "\n" +
                                "Plant effects: " + ",".join(p["Effects"]) + "\n"+
                                "Description: " + p["Description"] + "\n")
            
        if availability > 0:
            availability = "+" + str(availability)
        else:
            availability = str(availability)

        infoContent = "Roll: " + str(roll) + ", Area: " + area + ", Availability: " +  availability + ", Region: " + region

        content = " "*(math.ceil((len(infoContent)-23)/2)) + "-- Plants Discovered --" + "\n" + infoContent + "\n" + "\n" + "\n".join(plantContent)

        # Write to the file
        with open(file_path, 'w') as file:
            file.write(content)