import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random
import os

# Paths to the images
grass_tile_path = 'grass.png'
forest_tile_path = 'forest.png'
mountain_tile_path = 'mountain.png'
city_tile_path = 'city.png'

# Check if image files exist
def check_file_exists(file_path):
    print(f"Checking if file exists: {file_path}")  # Debug statement
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    print(f"File exists: {file_path}")  # Debug statement

# Function to display images
def display_image(image_path, title=""):
    check_file_exists(image_path)
    img = mpimg.imread(image_path)
    plt.figure(figsize=(5, 5))
    plt.imshow(img)
    plt.axis('off')
    if title:
        plt.title(title)
    plt.show()

def display_map(character, cities, city_names, bosses, map_size):
    fig, ax = plt.subplots(figsize=(10, 10))
    map_grid = [["" for _ in range(map_size)] for _ in range(map_size)]

    for city, name in zip(cities, city_names):
        x, y = city
        map_grid[y][x] = "C"
        ax.text(x, y, name, fontsize=8, ha='center')

    for boss in bosses:
        x, y = boss
        map_grid[y][x] = "B"

    x, y = character.position
    if 0 <= x < map_size and 0 <= y < map_size:
        map_grid[y][x] = "P"

    tile_paths = {
        "": grass_tile_path,
        "C": city_tile_path,
        "B": mountain_tile_path,
        "P": grass_tile_path  # Player on grass for simplicity
    }

    for y in range(map_size):
        for x in range(map_size):
            img_path = tile_paths[map_grid[y][x]]
            check_file_exists(img_path)
            img = mpimg.imread(img_path)
            ax.imshow(img, extent=(x, x + 1, y, y + 1))

    ax.set_xlim(0, map_size)
    ax.set_ylim(0, map_size)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()

def generate_city_names(num_cities):
    return [f"City_{i+1}" for i in range(num_cities)]

class Item:
    def __init__(self, name, item_type, strength_bonus=0, agility_bonus=0, intelligence_bonus=0):
        self.name = name
        self.item_type = item_type
        self.strength_bonus = strength_bonus
        self.agility_bonus = agility_bonus
        self.intelligence_bonus = intelligence_bonus

    def __str__(self):
        return f"{self.name} ({self.item_type}, STR: {self.strength_bonus}, AGI: {self.agility_bonus}, INT: {self.intelligence_bonus})"

class Character:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class
        self.level = 1
        self.base_health = 100
        self.health = self.base_health
        self.base_mana = 50
        self.mana = self.base_mana
        self.position = [map_size // 2, map_size // 2]
        self.exp = 0
        self.exp_to_next_level = 10
        self.gold = 50
        self.status_effects = []
        self.inventory = []
        self.equipment = {
            "weapon": None,
            "armor": None,
            "helmet": None,
            "boots": None,
            "trousers": None,
            "shoulderpads": None,
            "ring": None
        }
        self.set_class_attributes()

    def set_class_attributes(self):
        if self.char_class == "warrior":
            self.strength = 10
            self.agility = 5
            self.intelligence = 3
            self.health_per_level = 10
            self.mana_per_level = 5
            self.damage_factor = 2
            self.abilities = {
                "Heavy Smash": {"level": 1, "mana_cost": 10, "damage_multiplier": 2, "status_effect": None, "targets": 1},
                "Shield Bash": {"level": 3, "mana_cost": 15, "damage_multiplier": 1.5, "status_effect": "stun", "targets": 1},
                "Battle Cry": {"level": 5, "mana_cost": 20, "damage_multiplier": 3, "status_effect": None, "targets": "all"}
            }
        elif self.char_class == "mage":
            self.strength = 3
            self.agility = 5
            self.intelligence = 10
            self.health_per_level = 5
            self.mana_per_level = 10
            self.damage_factor = 3
            self.abilities = {
                "Fireball": {"level": 1, "mana_cost": 10, "damage_multiplier": 2, "status_effect": "burn", "targets": 1},
                "Ice Blast": {"level": 3, "mana_cost": 15, "damage_multiplier": 1.5, "status_effect": "freeze", "targets": 1},
                "Lightning Strike": {"level": 5, "mana_cost": 20, "damage_multiplier": 3, "status_effect": None, "targets": "all"}
            }
        elif self.char_class == "rogue":
            self.strength = 5
            self.agility = 10
            self.intelligence = 3
            self.health_per_level = 7
            self.mana_per_level = 7
            self.damage_factor = 2.5
            self.abilities = {
                "Backstab": {"level": 1, "mana_cost": 10, "damage_multiplier": 2, "status_effect": "bleed", "targets": 1},
                "Poison Dagger": {"level": 3, "mana_cost": 15, "damage_multiplier": 1.5, "status_effect": "poison", "targets": 1},
                "Shadow Strike": {"level": 5, "mana_cost": 20, "damage_multiplier": 3, "status_effect": None, "targets": "all"}
            }

    def move(self, direction):
        if direction == "n":
            self.position[1] = max(0, self.position[1] - 1)
        elif direction == "s":
            self.position[1] = min(map_size - 1, self.position[1] + 1)
        elif direction == "e":
            self.position[0] = min(map_size - 1, self.position[0] + 1)
        elif direction == "w":
            self.position[0] = max(0, self.position[0] - 1)
        else:
            print("Invalid direction!")
        print(f"{self.name} moved to {self.position}")

    def gain_exp(self, amount):
        self.exp += amount
        print(f"{self.name} gained {amount} exp!")
        if self.exp >= self.exp_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        self.base_health += self.health_per_level * self.level
        self.health = self.base_health
        self.base_mana += self.mana_per_level * self.level
        self.mana = self.base_mana
        print(f"{self.name} leveled up to level {self.level}!")

    def calculate_total_stats(self):
        total_strength = self.strength
        total_agility = self.agility
        total_intelligence = self.intelligence
        for item in self.equipment.values():
            if item:
                total_strength += item.strength_bonus
                total_agility += item.agility_bonus
                total_intelligence += item.intelligence_bonus
        return total_strength, total_agility, total_intelligence

    def buy_potion(self):
        if self.gold >= 10:
            self.gold -= 10
            self.health = self.base_health
            print(f"{self.name} bought a potion and restored health to {self.base_health}!")
        else:
            print("Not enough gold to buy a potion!")

    def buy_mana_potion(self):
        if self.gold >= 10:
            self.gold -= 10
            self.mana = self.base_mana
            print(f"{self.name} bought a mana potion and restored mana to {self.base_mana}!")
        else:
            print("Not enough gold to buy a mana potion!")

    def buy_equipment(self, item):
        if self.gold >= (item.strength_bonus + item.agility_bonus + item.intelligence_bonus) * 10:
            self.gold -= (item.strength_bonus + item.agility_bonus + item.intelligence_bonus) * 10
            self.inventory.append(item)
            print(f"{self.name} bought {item.name}!")
        else:
            print("Not enough gold to buy this item!")

    def equip_item(self, item_name):
        for item in self.inventory:
            if item.name == item_name:
                self.equipment[item.item_type] = item
                self.inventory.remove(item)
                print(f"{self.name} equipped {item.name}!")
                return
        print(f"{item_name} not found in inventory!")

    def show_inventory(self):
        print("Inventory:")
        for item in self.inventory:
            print(item)
        print("Equipped:")
        for slot, item in self.equipment.items():
            print(f"{slot}: {item}")

    def apply_status_effect(self, effect):
        self.status_effects.append(effect)

    def process_status_effects(self):
        for effect in self.status_effects[:]:
            if effect == "burn":
                self.health -= 5
                print(f"{self.name} takes 5 burn damage!")
            elif effect == "bleed":
                self.health -= 3
                print(f"{self.name} takes 3 bleed damage!")
            elif effect == "poison":
                self.health -= 4
                print(f"{self.name} takes 4 poison damage!")
            elif effect == "freeze":
                print(f"{self.name} is frozen and cannot move!")
                self.status_effects.remove(effect)

    def attack(self, enemy):
        total_strength, total_agility, total_intelligence = self.calculate_total_stats()
        base_damage = random.randint(5, 15)
        if self.char_class == "warrior":
            damage = base_damage + self.damage_factor * total_strength
        elif self.char_class == "mage":
            damage = base_damage + self.damage_factor * total_intelligence
        elif self.char_class == "rogue":
            damage = base_damage + self.damage_factor * total_agility
        enemy.health -= damage
        print(f"{self.name} dealt {damage} damage to {enemy.name}!")

    def use_ability(self, ability_name, targets):
        ability = self.abilities[ability_name]
        if self.mana >= ability["mana_cost"]:
            self.mana -= ability["mana_cost"]
            for target in targets:
                if self.char_class == "warrior":
                    damage = self.damage_factor * ability["damage_multiplier"] * self.strength + random.randint(10, 20)
                elif self.char_class == "mage":
                    damage = self.damage_factor * ability["damage_multiplier"] * self.intelligence + random.randint(10, 20)
                elif self.char_class == "rogue":
                    damage = self.damage_factor * ability["damage_multiplier"] * self.agility + random.randint(10, 20)
                target.health -= damage
                print(f"{self.name} used {ability_name} and dealt {damage} damage to {target.name}!")
                if ability["status_effect"]:
                    target.apply_status_effect(ability["status_effect"])
        else:
            print(f"Not enough mana to use {ability_name}!")

class Enemy:
    def __init__(self, name, level, health, ability=None):
        self.name = name
        self.level = level
        self.health = health
        self.ability = ability
        self.status_effects = []

    def attack(self, character):
        damage = random.randint(5, 15) * self.level
        character.health -= damage
        print(f"{self.name} dealt {damage} damage to {character.name}!")

    def use_ability(self, character):
        if self.ability == "Savage Bite":
            damage = self.level * 3 + random.randint(10, 20)
            character.apply_status_effect("bleed")
        elif self.ability == "Poison Spit":
            damage = self.level * 2 + random.randint(5, 15)
            character.apply_status_effect("poison")
        elif self.ability == "Fire Breath":
            damage = self.level * 4 + random.randint(15, 25)
            character.apply_status_effect("burn")
        else:
            damage = 0
        character.health -= damage
        print(f"{self.name} used {self.ability} and dealt {damage} damage to {character.name}!")

    def apply_status_effect(self, effect):
        self.status_effects.append(effect)

    def process_status_effects(self):
        for effect in self.status_effects[:]:
            if effect == "burn":
                self.health -= 5
                print(f"{self.name} takes 5 burn damage!")
            elif effect == "bleed":
                self.health -= 3
                print(f"{self.name} takes 3 bleed damage!")
            elif effect == "poison":
                self.health -= 4
                print(f"{self.name} takes 4 poison damage!")
            elif effect == "freeze":
                print(f"{self.name} is frozen and cannot move!")
                self.status_effects.remove(effect)

class Boss(Enemy):
    def __init__(self, name, level, health, ability=None):
        super().__init__(name, level, health, ability)
        self.boss = True
        self.health *= 2
        self.level *= 2

class Companion(Character):
    def __init__(self, name, char_class):
        super().__init__(name, char_class)
        self.is_companion = True

def encounter(character):
    possible_enemies = [
        ("Goblin", "Savage Bite"),
        ("Orc", "Smash"),
        ("Wolf", "Savage Bite"),
        ("Troll", "Club Smash"),
        ("Skeleton", "Bone Throw"),
        ("Zombie", "Infectious Bite"),
        ("Vampire", "Life Drain"),
        ("Dragon", "Fire Breath"),
        ("Witch", "Hex"),
        ("Demon", "Hellfire")
    ]
    num_enemies = random.randint(1, 3)
    enemies = []
    for _ in range(num_enemies):
        enemy_name, enemy_ability = random.choice(possible_enemies)
        distance_from_center = max(abs(character.position[0] - map_size // 2), abs(character.position[1] - map_size // 2))
        enemy_level = max(1, distance_from_center // 2 + random.randint(-1, 1), character.level)
        enemy_health = enemy_level * 30
        enemies.append(Enemy(f"{enemy_name} Lvl {enemy_level}", enemy_level, enemy_health, enemy_ability))
    
    print(f"{character.name} encountered {', '.join([enemy.name for enemy in enemies])}!")
    fight(character, enemies)

def fight(character, enemies):
    while character.health > 0 and any(enemy.health > 0 for enemy in enemies):
        print("\nEnemies:")
        for enemy in enemies:
            print(f"{enemy.name} - HP: {enemy.health} - Effects: {enemy.status_effects}")
        
        character.process_status_effects()
        for enemy in enemies:
            enemy.process_status_effects()

        action = input("Do you want to (a)ttack, use (b)ilities, or (r)un? ").lower()
        if action == "a":
            target = select_target(enemies)
            character.attack(target)
            if target.health <= 0:
                print(f"{character.name} defeated {target.name}!")
                enemies.remove(target)
                character.gain_exp(target.level * 5)
                character.gold += target.level * 3
                print(f"{character.name} found {target.level * 3} gold!")
            if not enemies:
                return
            for enemy in enemies:
                if enemy.health > 0:
                    if "freeze" in enemy.status_effects:
                        print(f"{enemy.name} is frozen and cannot move!")
                    elif enemy.ability and random.random() < 0.3:
                        enemy.use_ability(character)
                    else:
                        enemy.attack(character)
        elif action == "b":
            available_abilities = [ability for ability in character.abilities if character.level >= character.abilities[ability]["level"]]
            if available_abilities:
                print("Available abilities:")
                for ability in available_abilities:
                    print(f"- {ability} (Mana Cost: {character.abilities[ability]['mana_cost']})")
                ability_choice = input("Choose an ability: ")
                if ability_choice in available_abilities:
                    if character.abilities[ability_choice]["targets"] == "all":
                        character.use_ability(ability_choice, enemies)
                    else:
                        target = select_target(enemies)
                        character.use_ability(ability_choice, [target])
                    if any(enemy.health <= 0 for enemy in enemies):
                        for enemy in enemies:
                            if enemy.health <= 0:
                                print(f"{character.name} defeated {enemy.name}!")
                                enemies.remove(enemy)
                                character.gain_exp(enemy.level * 5)
                                character.gold += enemy.level * 3
                                print(f"{character.name} found {enemy.level * 3} gold!")
                    if not enemies:
                        return
                    for enemy in enemies:
                        if enemy.health > 0:
                            if "freeze" in enemy.status_effects:
                                print(f"{enemy.name} is frozen and cannot move!")
                            elif enemy.ability and random.random() < 0.3:
                                enemy.use_ability(character)
                            else:
                                enemy.attack(character)
                else:
                    print("Invalid ability choice.")
            else:
                print("No abilities available at your current level.")
        elif action == "r":
            print(f"{character.name} ran away!")
            return
        else:
            print("Invalid action!")

def select_target(enemies):
    print("Select a target:")
    for i, enemy in enumerate(enemies):
        print(f"{i + 1}. {enemy.name} - HP: {enemy.health}")
    choice = int(input("Enter the number of the target: ")) - 1
    return enemies[choice]

def generate_cities(num_cities):
    cities = []
    while len(cities) < num_cities:
        x = random.randint(0, map_size - 1)
        y = random.randint(0, map_size - 1)
        if (x, y) not in cities:
            cities.append((x, y))
    return cities

def generate_bosses(num_bosses):
    bosses = []
    while len(bosses) < num_bosses:
        x = random.randint(0, map_size - 1)
        y = random.randint(0, map_size - 1)
        if (x, y) not in bosses:
            bosses.append((x, y))
    return bosses

def hire_companion():
    print("Available companions:")
    companions = [
        Companion("Aragorn", "warrior"),
        Companion("Gandalf", "mage"),
        Companion("Legolas", "rogue")
    ]
    for i, companion in enumerate(companions):
        print(f"{i + 1}. {companion.name} - {companion.char_class.capitalize()} - Cost: 50 gold")
    choice = int(input("Enter the number of the companion to hire: ")) - 1
    return companions[choice]

def main():
    print("Current working directory:", os.getcwd())  # Debug statement
    name = input("Enter your character's name: ")
    print("Choose your class: (warrior, mage, rogue)")
    char_class = input("Class: ").lower()
    if char_class not in ["warrior", "mage", "rogue"]:
        print("Invalid class. Defaulting to warrior.")
        char_class = "warrior"
    
    global map_size
    map_size = 20
    player = Character(name, char_class)
    num_cities = 10
    num_bosses = 5
    cities = generate_cities(num_cities)
    city_names = generate_city_names(num_cities)
    bosses = generate_bosses(num_bosses)
    items = [
        Item("Sword of Strength", "weapon", strength_bonus=5),
        Item("Staff of Wisdom", "weapon", intelligence_bonus=5),
        Item("Robe of Protection", "armor", intelligence_bonus=3),
        Item("Helmet of Insight", "helmet", intelligence_bonus=2),
        Item("Boots of Swiftness", "boots", agility_bonus=3),
        Item("Trousers of Might", "trousers", strength_bonus=3),
        Item("Shoulderpads of Fortitude", "shoulderpads", strength_bonus=2),
        Item("Ring of Dexterity", "ring", agility_bonus=2),
        Item("Amulet of Power", "neck", strength_bonus=2, intelligence_bonus=2),
        Item("Gloves of Precision", "gloves", agility_bonus=2),
        Item("Shield of Resilience", "shield", strength_bonus=3, agility_bonus=2),
        Item("Cloak of Shadows", "cloak", agility_bonus=3, intelligence_bonus=2)
    ]

    companions = []

    in_city = False
    cities_with_taverns = random.sample(cities, len(cities) // 2)

    while player.health > 0:
        print(f"\n{player.name}'s status: Level {player.level}, Health {player.health}, Mana {player.mana}, Position {player.position}, Gold {player.gold}")
        player.show_inventory()
        display_map(player, cities, city_names, bosses, map_size)

        if tuple(player.position) in cities:
            if not in_city:
                enter_city = input("Do you want to enter the city? (y/n): ").lower()
                if enter_city == "y":
                    print(f"{player.name} entered the city!")
                    in_city = True
                else:
                    player.move("s")  # Move south to simulate staying outside of the city
            if in_city:
                city_action = input("Do you want to buy a (p)otion, (m)ana potion, (e)quipment, (h)ire companion, or (l)eave city? ").lower()
                if city_action == "p":
                    player.buy_potion()
                elif city_action == "m":
                    player.buy_mana_potion()
                elif city_action == "e":
                    print("Available items:")
                    for item in items:
                        print(item)
                    item_name = input("Enter the name of the item to buy: ")
                    for item in items:
                        if item.name == item_name:
                            player.buy_equipment(item)
                            break
                    else:
                        print("Item not found.")
                elif city_action == "h":
                    if tuple(player.position) in cities_with_taverns:
                        if len(companions) < 2:
                            companion = hire_companion()
                            if player.gold >= 50:
                                player.gold -= 50
                                companions.append(companion)
                                print(f"{companion.name} the {companion.char_class} has joined your party!")
                            else:
                                print("Not enough gold to hire a companion.")
                        else:
                            print("You can only have up to two companions.")
                    else:
                        print("There is no tavern in this city.")
                elif city_action == "l":
                    in_city = False
                else:
                    print("Invalid action.")
        else:
            if in_city:
                in_city = False
            direction = input("Move (n)orth, (s)outh, (e)ast, (w)est or (i)nventory: ").lower()
            if direction in ["n", "s", "e", "w"]:
                player.move(direction)
                encounter(player)
            elif direction == "i":
                item_name = input("Enter the name of the item to equip: ")
                player.equip_item(item_name)
            else:
                print("Invalid action!")

    print(f"{player.name} has been defeated. Game over!")

if __name__ == "__main__":
    main()
