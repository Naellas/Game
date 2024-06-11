import random
from character import Character
from enemy import Enemy, Boss

def encounter(character, map_size):
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
    distance_from_center = max(abs(character.position[0] - map_size // 2), abs(character.position[1] - map_size // 2))
    num_enemies = random.randint(1, 3)
    enemies = []
    for _ in range(num_enemies):
        enemy_name, enemy_ability = random.choice(possible_enemies)
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
