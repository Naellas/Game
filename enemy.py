import random

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