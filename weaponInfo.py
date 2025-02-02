import random
from copy import deepcopy

## ATTRIBUTES ##
# WEAPONS #
# name: name of the weapon
# damage: rolls each time to decide weapon damage, for the amount of rolls per weapon
# critchance: if a roll crits it adds another dice to the roll
# delay: time in seconds before can swing again
# accuracy: chance to hit opponent

# firedamage: damage over 10s
# colddamage: damage over 10s
# bleeding: damage over 15s
# armourpierce: number of defense to ignore
# armourshred: percent of defense to ignore
# critstrength: number of extra dice to add (def op)
# lifesteal: percentage of damage after killing to heal you
# truedamage: damage that ignores defense
# currenthpdamage: deals damage related to the enemies current hp in %
# parry: chance to negate damage and stun opponent for 1.5s
# damageadd: additional damage to attack
# damagemulti: damage multiplier to attack

# ARMOUR #

# name: name of the armour
# defense: percentage reduction from incoming damage
# toughness: reduce armour reduction from enemies
# encumbrance: percentage increase in delay

# health: increase max health
# defensemult: defense multiplier
# regeneration: increase regen between battles
# dodge chance: percent to avoid getting hit
# thorns: percent of damage from attacker reflected back, is true damage


# Add custom rarities here, make sure they have a colour
rarityCol = {
    'Common':'\033[97m',
    'Uncommon':'\033[32m',
    'Rare':'\033[34m',
    'Epic':'\033[95m',
    'Legendary':'\033[93m',
    'Mythical':'\033[91m',
    'Cosmic':'\033[35m',
}
TIERS = {
    "Common": [0.6,1,0], #60%
    "Uncommon": [0.85,2,1], #25%
    "Rare": [0.95,3,2], #10%
    "Epic": [0.98,4,3], #3%
    "Legendary": [0.993,5,4], #1.7%
    "Mythical": [0.997,5,5], #0.23% (there many be 2 of these)
    "Cosmic": [1,6,6] #0.07% (there may not be a cosmic weapon in play)
}


# Add weapons here, they should all have these base stats
weaponTypes = {
    1: {
        "name": "Shortsword",
        "damage": {"number": 1, "sides": 5},
        "critchance": 0.1,
        "delay": 0.9,
        "accuracy": 0.9
    },
    2: {
        "name": "Broadsword",
        "damage": {"number": 1, "sides": 7},
        "critchance": 0.16,
        "delay": 1.2,
        "accuracy": 0.86
    },
    2: {
        "name": "Longsword",
        "damage": {"number": 1, "sides": 8},
        "critchance": 0.16,
        "delay": 1.4,
        "accuracy": 0.83
    },
    3: {
        "name": "Greatsword",
        "damage": {"number": 1, "sides": 12},
        "critchance": 0.2,
        "delay": 2,
        "accuracy": 0.8
    },
    4: {
        "name": "Katana",
        "damage": {"number": 2, "sides": 4},
        "critchance": 0.2,
        "delay": 0.8,
        "accuracy": 0.7
    },
    5: {
        "name": "Nail",
        "damage": {"number": 2, "sides": 5},
        "critchance": 0.3,
        "delay": 1,
        "accuracy": 0.78
    },
    6: {
        "name": "Dagger",
        "damage": {"number": 1, "sides": 12},
        "critchance": 0.5,
        "delay": 2,
        "accuracy": 0.5
    },
    6: {
        "name": "Flail",
        "damage": {"number": 3, "sides": 6},
        "critchance": 0.3,
        "delay": 2.5,
        "accuracy": 0.5
    },
    7: {
        "name": "Quarterstaff",
        "damage": {"number": 1, "sides": 8},
        "critchance": 0.1,
        "delay": 1,
        "accuracy": 0.75
    },
    8: {
        "name": "Waraxe",
        "damage": {"number": 2, "sides": 8},
        "critchance": 0.6,
        "delay": 1.8,
        "accuracy": 0.75
    },
    9: {
        "name": "Greathammer",
        "damage": {"number": 3, "sides": 8},
        "critchance": 0.3,
        "delay": 3,
        "accuracy": 0.5
    },
}

# Add armour here, they should all have these base stats
armourTypes = {
    1: {
        "name": "Leather",
        "defense": 5,
        "toughness": 0,
        "encumbrance": 1.05
    },
    2: {
        "name": "Chainmail",
        "defense": 15,
        "toughness": 3,
        "encumbrance": 1.25
    },
    3: {
        "name": "Scalemail",
        "defense": 20,
        "toughness": 6,
        "encumbrance": 1.45
    },
    4: {
        "name": "Platemail",
        "defense": 30,
        "toughness": 9,
        "encumbrance": 1.65
    },
    5: {
        "name": "Cloak",
        "defense": 3,
        "toughness": 1,
        "encumbrance": 0.9,
        "dodge": 0.08
    },
}
# Add weapon attributes here, damage cannot be modified so use damageadd/damagemulti instead
weaponAttributes = {
    "Light": {
        "delay":[-0.08,-0.12,-0.16,-0.2,-0.3,-0.4,-0.6]
    },
    "Intricate": {
        "critchance":[0.02,0.04,0.06,0.1,0.14,0.2,0.3]
    },
    "Lenghty": {
        "accuracy":[0.02,0.05,0.09,0.14,0.2,0.3,0.5]
    },
    "Sharp": {
        "bleeding":[1,1.5,3,6,9,14,21]
    },
    "Violent": {
        "damageadd":[1,2,4,6,9,11,16]
    },
    "Piercing": {
        "armourpierce":[2,4,7,10,14,20,30]
    },
    "Shredding": {
        "armourshred":[5,8,12,15,25,35,50]
    },
    "Piercing": {
        "armourpierce":[2,4,7,10,14,20,30]
    },
    "Infernal": {
        "firedamage":[None,2,3,5,8,12,18]
    },
    "Glacial": {
        "colddamage":[None,2,3,5,8,12,18]
    },
    "Agile": {
        "parry":[None,0.02,0.04,0.06,0.1,0.14,0.24]
    },
    "Murderous": {
        "damagemulti":[None,None,1.2,1.3,1.5,1.8,2.2]
    },
    "Beserking": {
        "overheal":[None,None,0.15,0.25,0.35,0.6,1]
    },
    "Vampiric": {
        "lifesteal":[None,None,0.15,0.25,0.35,0.6,1]
    },
    "Enchanted": {
        "truedamage":[None,None,1,2,4,7,10]
    },
    "Lacerating": {
        "critstrength":[None,None,None,1,2,3,4]
    },
    "Frostburn": {
        "firedamage":[None,None,None,4,7,10,15],
        "colddamage":[None,None,None,4,7,10,15]
    },
    "Hollow": {
        "parry":[None,None,None,0.08,0.13,0.18,0.3],
        "armourpierce":[None,None,None,10,14,20,30]
    }
}

# Add armour attributes here
armourAttributes = {
    "Ironforged": {
        "defense": [1,2,4,6,10,14,20]
    },
    "Reinforced": {
        "toughness": [0.5,1,2,4,6,10,15]
    },
    "Lightweight": {
        "encumbrance": [-0.03,-0.06,-0.1,-0.15,-0.2,-0,3,-0.5]
    },
    "Vital": {
        "health": [None,3,5,8,12,16,24]
    },
    "Winged": {
        "dodge": [None,0.03,0.06,0.1,0.13,0.18,0.35]
    },
    "Spiritual": {
        "regeneration": [None,None,1,2,3,5,8]
    },
    "Spiked": {
        "thorns": [None,None,0.2,0.3,0.4,0.6,0.8]
    },
    "Darkforged": {
        "defensemulti": [None,None,1.1,1.3,1.7,2,2.3]
    },
}

def generateWeapon(oreName):
    name = ""
    baseStats = weaponTypes[random.randint(1,9)]
    weaponStats = deepcopy(baseStats)  # Create a new dictionary for each weapon's stats

    rng = random.uniform(0,1)
    rarity = ""
    asNumber = 0
    attributes = 0
    for key, value in TIERS.items():
        if rng < value[0]:
            rarity = key
            asNumber = value[2]
            attributes = value[1]
            break
    
    name = weaponStats["name"]
    currentAttributes = []
    weaponStats["rarity"] = asNumber

    for i in range(random.randint(max(0,attributes-2),attributes)):
        valid = False
        attributeName = ""
        while not valid:
            n, attributeSelected = random.choice(list(weaponAttributes.items()))
            for x, val in dict(attributeSelected).items():
                if val[asNumber] and x not in currentAttributes:
                    valid = True
                    if weaponStats.get(x):
                        weaponStats.update({x: weaponStats[x] + val[asNumber]})
                    else:
                        weaponStats.update({x: val[asNumber]})
                    attributeName = n
                    currentAttributes.append(x)
        
        name = f"{attributeName} {name}"

    return f"{rarityCol[rarity]}{oreName}'s {name}", weaponStats

def generateArmour(oreName):
    name = ""
    baseStats = armourTypes[random.randint(1,5)]
    armourStats = deepcopy(baseStats)  # Create a new dictionary for each armour's stats

    rng = random.uniform(0,1)
    rarity = ""
    asNumber = 0
    attributes = 0
    for key, value in TIERS.items():
        if rng < value[0]:
            rarity = key
            asNumber = value[2]
            attributes = value[1]
            break
    
    name = armourStats["name"] + f" Armour"
    currentAttributes = []
    armourStats["rarity"] = asNumber

    for i in range(random.randint(max(0,attributes-2),attributes)):
        valid = False
        attributeName = ""
        while not valid:
            n, attributeSelected = random.choice(list(armourAttributes.items()))
            for x, val in dict(attributeSelected).items():
                if val[asNumber] and x not in currentAttributes:
                    valid = True
                    if armourStats.get(x):
                        armourStats.update({x: armourStats[x] + val[asNumber]})
                    else:
                        armourStats.update({x: val[asNumber]})
                    attributeName = n
                    currentAttributes.append(x)
        name = f"{attributeName} {name}"

    return f"{rarityCol[rarity]}{oreName}'s {name}", armourStats
                




