def CheckIfModifier(askmessage, errormessage):
    tempLines = 0 # Not global
    while True:
            modifiervalue = input(askmessage)
            if (len(modifiervalue) != 0 and len(modifiervalue) < 2):
                print(errormessage)
                tempLines += 2
            elif (len(modifiervalue) == 0):
                modifiervalue = 0
                break
            elif modifiervalue[0] != "+" and modifiervalue[0] != "-":
                print(errormessage)
                tempLines += 2
            elif not modifiervalue[1:].isdigit():
                print(errormessage)
                tempLines += 2
            else:
                if (modifiervalue[0] == "+"):
                    modifiervalue = int(modifiervalue[1:])
                else:
                    modifiervalue = int(modifiervalue[1:]) * -1
                break
    return modifiervalue, tempLines

def ReturnModifierValue(modifier):
    if (modifier[0] == "+"):
        value = int(modifier[1:])
    else:
        value = int(modifier[1:]) * -1
    return value