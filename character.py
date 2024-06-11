import random

class Character:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class
        self.level = 1
        self.base_health = 100
        self.health = self.base_health
        self.base_mana = 50
        self.mana = self.base_mana
        self.position = [10, 10]
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

    def move(self, direction, map_size):
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

class Companion(Character):
    def __init__(self, name, char_class):
        super().__init__(name, char_class)
        self.is_companion = True
