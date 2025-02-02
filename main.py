import json
import random
import weaponInfo as generator
import threading
import time

date = time.strftime("%Y-%m-%d")

class colors:
    '''Colors class:reset all colors with colors.reset; two
    sub classes fg for foreground
    and bg for background; use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.greenalso, the generic bold, disable,
    underline, reverse, strike through,
    and invisible work with the main class i.e. colors.bold'''
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'
    
    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'
    
    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'

class Graph:
    def __init__(self,size):
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.size = size
        self.vertexdata = [""] * size

    def add_vertex(self, v, data):
        if 0 <= v < self.size:
            self.vertexdata[v] = data

    def add_edge(self, v1, v2):
        if 0 <= v1 < self.size and 0 <= v2 < self.size:
            self.adj_matrix[v1][v2] = 1
            self.adj_matrix[v2][v1] = 1

    def remove_edge(self, v1, v2):
        if 0 <= v1 < self.size and 0 <= v2 < self.size:
            self.adj_matrix[v1][v2] = 0
            self.adj_matrix[v2][v1] = 0

    def is_neighbour(self, v1, v2): 
        if 0 <= v1 < self.size and 0 <= v2 < self.size:
            return self.adj_matrix[v1][v2] == 1

    def print_graph(self):
        string = ""
        for row in self.adj_matrix:
            string += (' '.join(map(str, row)))
            string += "\n"
        return string
    
    def get_name(self, v):
        if 0 <= v < self.size:
            return self.vertexdata[v]
        return
    
    def get_number_from_name(self, name):
        for i, v in enumerate(self.vertexdata):
            if v == name:
                return i
        return
    
    def get_neighbours(self, v):
        if 0 <= v < self.size:
            return [i for i, x in enumerate(self.adj_matrix[v]) if x == 1]
        return

    def print_neighbours(self, v):
        if 0 <= v < self.size:
            neighbours = [self.vertexdata[i] for i, x in enumerate(self.adj_matrix[v]) if x == 1]
            print(f"Neighbours of vertex {self.vertexdata[v]}: {neighbours}")


class OreInfo():
    def __init__(self):
        self.ores = []
        self.oresLeft = []
        self.oreEquipment = []
        self.oreStats = []

        self.kills = {}
        self.lb = {}

        self.oreNumber = 0
    
    def add(self, ore):
        if ore in self.ores:
            return
        self.ores.append(ore)
        self.oresLeft.append(ore)
        weapon, armour = generator.generateWeapon(ore), generator.generateArmour(ore)
        self.oreEquipment.append([weapon, armour])
    
        self.oreStats.append([20,self.oreEquipment[-1][1][1]["health"] + 20 if self.oreEquipment[-1][1][1].get("health") else 20]) #health

        self.oreNumber += 1

    def add_kill(self,winner,loser):
        self.lb[self.oreNumber] = loser
        self.oreNumber -= 1
        if self.kills.get(winner) == None:
            self.kills[winner] = [loser]
        else:
            self.kills[winner].append(loser)
        self.oresLeft.remove(loser)

    def get_ore_stats(self,graph : Graph,ore):
        killCount = 0
        if self.kills.get(ore) != None:
            killCount = len(self.kills[ore])
        number = graph.get_number_from_name(ore)
        isAlive = ore in self.oresLeft
        neighbors = graph.get_neighbours(number)
        for i in neighbors:
            new = neighbors.pop(0)
            neighbors.append(f"{new} ({g.get_name(new)})")

        weapons, armours = self.oreEquipment[self.ores.index(ore)]
        health = self.oreStats[self.ores.index(ore)]
        other = self.oreEquipment[self.ores.index(ore)][1][1]
        
        return (killCount, number, isAlive, neighbors, weapons, armours, health, other)

    def is_alive(self, ore):
        return ore in self.oresLeft

ores = OreInfo()

with open("ores.txt") as f:
    for line in f:
        ores.add(line.strip())



g = Graph(len(ores.ores))
for i, ore in enumerate(ores.ores):
    g.add_vertex(i, ore)

for i in range(len(ores.ores)):
    num1 = i
    add = []
    while True:
        num2 = random.randint(0, len(ores.ores) - 1)
        if num1 != num2:
            add.append(num2)
            if random.randint(1,2) == 1:
                break

    
    for num in add:    
        if g.is_neighbour(num1, num) == False and g.is_neighbour(num, num1) == False:
            g.add_edge(num1, num)

def log(type,string):
    global line
    with open(f"Logs/{date}.txt","a") as f:
        f.write(f"[{time.strftime("%H:%M:%S")}][{type.upper()}] {string}\n")

currentRound = 0
validResponse = False
speed = 1
def rollDamage(times,sides):
    total = 0
    for i in range(times):
        total += random.randint(1,sides)
    return total

def dealDamage(ore,other):
    damageovertime = [0,0,0]
    while ores.oreStats[ores.ores.index(ore)][0] > 0 and ores.oreStats[ores.ores.index(other)][0] > 0:
        info = ""
        oreStats = ores.oreEquipment[ores.ores.index(ore)]
        otherStats = ores.oreEquipment[ores.ores.index(other)]
        critamount = 1 + oreStats[0][1]["critstrength"] if oreStats[0][1].get("critstrength") else 1
        armourpierce = (oreStats[0][1]["armourpierce"] - otherStats[1][1]["toughness"]) if oreStats[0][1].get("armourpierce") else 0
        crit = True if random.uniform(0,1) < oreStats[0][1]["critchance"] else False
        damage = rollDamage(oreStats[0][1]["damage"]["number"] + critamount if crit else oreStats[0][1]["damage"]["number"],oreStats[0][1]["damage"]["sides"]) + (oreStats[0][1]["damageadd"] if oreStats[0][1].get("damageadd") else 0) * (oreStats[0][1]["damagemulti"] if oreStats[0][1].get("damagemulti") else 1)
        truedamage = oreStats[0][1]["truedamage"] if oreStats[0][1].get("truedamage") else 0
        dodge = otherStats[0][1]["dodge"] if otherStats[0][1].get("dodge") else 0
        if oreStats[0][1]["accuracy"] > random.uniform(0,1) and  dodge < random.uniform(0,1):
            reduction = (1 - (((otherStats[1][1]["defense"] * (otherStats[1][1]["defensemulti"] if otherStats[1][1].get("defensemulti") else 1)) - armourpierce) / 100))+ ((oreStats[0][1]["armourshred"] / 100) if oreStats[1][1].get("armourshred") else 0)
            ores.oreStats[ores.ores.index(other)][0] -= damage * reduction #base damage
            ores.oreStats[ores.ores.index(ore)][0] -= damage * otherStats[1][1]["thorns"] if otherStats[1][1].get("thorns") else 0 # thorns
            ores.oreStats[ores.ores.index(other)][0] -= truedamage # damage unaffected by defense
            ores.oreStats[ores.ores.index(other)][0] -= ores.oreStats[ores.ores.index(other)][0] * (oreStats[0][1]["currenthpdamage"] if oreStats[0][1].get("currenthpdamage") else 0) #current hp damage
            # give damage over time effects
            damageovertime[0] += oreStats[0][1]["firedamage"] if oreStats[0][1].get("firedamage") else 0
            damageovertime[1] += oreStats[0][1]["colddamage"] if oreStats[0][1].get("colddamage") else 0
            damageovertime[2] += oreStats[0][1]["bleeding"] if oreStats[0][1].get("bleeding") else 0
            print(f"{colors.fg.green}{colors.bold}[{ore}] Hit {colors.reset}", end="",flush=True)
        else:
            print(f"{colors.fg.red}[{ore}] Missed {colors.reset}", end="",flush=True)
        print(f"{colors.bold}{other}: {"■"*round(ores.oreStats[ores.ores.index(other)][0])}{"□" * (int(round(ores.oreStats[ores.ores.index(other)][1]))-int(round(ores.oreStats[ores.ores.index(other)][0])))} {ores.oreStats[ores.ores.index(other)][0]:.2f}/{ores.oreStats[ores.ores.index(other)][1]:.0f}hp".center(50," "),colors.reset,flush=True)
        #damage over time (cannot be dodged)
        ores.oreStats[ores.ores.index(other)][0] -= damageovertime[0] / 5 if damageovertime[0] > 0 else 0
        ores.oreStats[ores.ores.index(other)][0] -= damageovertime[1] / 5 if damageovertime[1] > 0 else 0
        ores.oreStats[ores.ores.index(other)][0] -= damageovertime[2] / 7 if damageovertime[2] > 0 else 0
        time.sleep((max(0,oreStats[0][1]["delay"]) * max(0,oreStats[1][1]["encumbrance"])) / speed)
    if ores.oreStats[ores.ores.index(other)][0] <= 0:
        excess = ores.oreStats[ores.ores.index(other)][0] * -1
        ores.oreStats[ores.ores.index(ore)][0] += round(excess * oreStats[0][1]["lifesteal"] if oreStats[0][1].get("lifesteal") else 0)
        if otherStats[0][1]["rarity"] > oreStats[0][1]["rarity"]:
            ores.oreEquipment[ores.ores.index(ore)][0] = ores.oreEquipment[ores.ores.index(other)][0]

        if otherStats[1][1]["rarity"] > oreStats[1][1]["rarity"]:
            ores.oreEquipment[ores.ores.index(ore)][1] = ores.oreEquipment[ores.ores.index(other)][1]

        return True
    return False

print(f"{colors.bold}{colors.underline}Type cmds for a list of all commands{colors.reset}")
while True:
    currentRound += 1
    try:
        selected = random.choice(ores.ores)
        neighbor = g.get_name(random.choice(g.get_neighbours(ores.ores.index(selected))))

        assert(ores.is_alive(selected))
        assert(ores.is_alive(neighbor))
    except:
        currentRound -= 1
        continue
        
    roundString = f"{colors.reset}ROUND {currentRound}".center(50, "-")
    print(roundString)
    print(f"{colors.bold}Ores left: {ores.oreNumber}{colors.reset}" )
    print(f"{colors.fg.red}{colors.bold}First ore chosen: {selected}{colors.reset}")
    print(f"{colors.fg.blue}{colors.bold}Second ore chosen: {neighbor}{colors.reset}")
    log("info",f"First ore: {selected}, Second ore: {neighbor}")
    validResponse = False
    while not validResponse:
        response = input(f"{colors.reset}> ").split(">")
        if response[0] == "kills":
            if response[1] in ores.ores:
                if ores.kills.get(response[1]) == None:
                    print(f"{response[1]} has no kills")
                else:
                    print(f"{response[1]} kills: {ores.kills[response[1]]}")
            elif response[1] == "all":
                aliveOnly = False
                if "alive" in response:
                    aliveOnly = True
                for key,value in ores.kills.items():
                    if aliveOnly and ores.is_alive(key) == False:
                        continue
                    if ores.is_alive(key):
                        print(f"{colors.fg.green}{key} kills: {value}{colors.reset}")
                    else:
                        print(f"{colors.fg.red}{colors.strikethrough}{key} kills: {value}{colors.reset}")
        elif response[0] == "stats":
            if response[1] in ores.ores:
                stats = ores.get_ore_stats(g,response[1])
                lbPlace = 0
                for key,value in ores.lb.items():
                    if value == response[1]:
                        lbPlace = key
                        break
                print(f"{colors.underline}{response[1]}{colors.reset}".center(50, "-"))
                print(f"{colors.fg.green if stats[2] else colors.fg.red}{colors.bold}Alive".center(50," ") if stats[2] else f"Dead(#{lbPlace})".center(50," "),colors.reset)
                print(f"{colors.fg.green}{colors.bold}{"■"*round(stats[6][0])}{"□" * (int(round(stats[6][1]))-int(round(stats[6][0])))} {stats[6][0]:.2f}/{stats[6][1]:.0f}hp".center(50," "),colors.reset)
                print(f"{colors.fg.cyan}Ore Number: {stats[1]}{colors.reset}")
                print(f"{colors.fg.orange}Kills: {stats[0]}{colors.reset}")
                print(f"{colors.fg.pink}Weapon: {colors.reset}{stats[4][0]}{colors.reset}")
                print(f"{colors.fg.purple}Armour: {colors.reset}{stats[5][0]}{colors.reset}")
                if stats[2]:
                    print(f"{colors.bold}Neighbours: {stats[3]}{colors.reset}")
        elif response[0] == "lb":
            for key,value in ores.lb.items():
                print(f"{colors.bold}{key}: {value}{colors.reset}")
        elif response[0] == "speed":
            try:
                speed = int(response[1])
            except:
                print(f"{colors.fg.red}{colors.bold}Invalid command{colors.reset}")
        elif response[0] == "cmds":
            print(f"{colors.reset}{colors.fg.purple}{colors.bold}kills>[ore]>(aliveornot){colors.reset}: Returns the list of all kills by an ore. Use 'all' to get all kills. If using 'all', you can type 'alive' after to show only alive ores.\n\
{colors.fg.purple}{colors.bold}stats>[ore]{colors.reset}: Returns an ores stats. Includes health, kill count, ore number, weapon, armour and neighbors.\n\
{colors.fg.purple}{colors.bold}lb{colors.reset}: Prints out the current leaderboard of all dead ores. \n{colors.fg.purple}{colors.bold}speed>[number]{colors.reset}: Sets the speed of combat to be multiplied by that number.")
        elif response[0] == "":
            validResponse = True
        else:
            print("Invalid command")

    # get winner for the battle
    
    threading.Thread(target=dealDamage,args=(selected,neighbor)).start()
    threading.Thread(target=dealDamage,args=(neighbor,selected)).start()

    while ores.oreStats[ores.ores.index(neighbor)][0] > 0 and ores.oreStats[ores.ores.index(selected)][0] > 0: #wait for the battle to finish
        pass
    
    hp = ores.oreStats[ores.ores.index(neighbor)][0]
    otherhp = ores.oreStats[ores.ores.index(selected)][0]
    
    winner = neighbor if hp > otherhp else selected
    loser = selected if winner == neighbor else neighbor
    numbers = (g.get_number_from_name(winner),g.get_number_from_name(loser))

    for edge in g.get_neighbours(numbers[1]):
        if numbers[0] != edge:
            g.add_edge (numbers[0], edge)
        g.remove_edge(numbers[1], edge)

    ores.add_kill(winner, loser)
    print("\n")
    print(f"{colors.fg.green}Winner: {winner}(number {numbers[0]})")
    print(f"{colors.fg.red}Eliminated: {loser}(number {numbers[1]})")
    log("info",f"Winner: {winner}, Eliminated: {loser}")

    for ore in ores.oresLeft:
        healths = ores.oreStats[ores.ores.index(ore)]
        stats = ores.oreEquipment[ores.ores.index(ore)]
        regen = 1 + stats[1][1]["regeneration"] if stats[1][1].get("regeneration") else 1
        healths[0] = min(healths[0] + regen,healths[1])
        healths[1] = 20 + (stats[1][1]["health"] if stats[1][1].get("health") else 0)

    if ores.oreNumber == 1:
        for key,value in ores.lb.items():
            print(f"{key}: {value}")
            log("Leaderboard",f"{key}: {value}")
        break
    elif ores.oreNumber <= 20:
        print("Ores left: ", ores.oresLeft)

    





