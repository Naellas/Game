import random
from character import Character, Companion
from item import Item, items
from utilities import display_map, generate_cities, generate_bosses, hire_companion
from encounter import encounter

def main():
    name = input("Enter your character's name: ")
    print("Choose your class: (warrior, mage, rogue)")
    char_class = input("Class: ").lower()
    if char_class not in ["warrior", "mage", "rogue"]:
        print("Invalid class. Defaulting to warrior.")
        char_class = "warrior"
    
    map_size = 20
    player = Character(name, char_class)
    num_cities = 10
    num_bosses = 5
    cities = generate_cities(num_cities, map_size)
    bosses = generate_bosses(num_bosses, map_size)

    companions = []

    in_city = False
    cities_with_taverns = random.sample(cities, len(cities) // 2)

    while player.health > 0:
        print(f"\n{player.name}'s status: Level {player.level}, Health {player.health}, Mana {player.mana}, Position {player.position}, Gold {player.gold}")
        player.show_inventory()
        display_map(player, cities, bosses, map_size)

        if tuple(player.position) in cities:
            if not in_city:
                enter_city = input("Do you want to enter the city? (y/n): ").lower()
                if enter_city == "y":
                    print(f"{player.name} entered the city!")
                    in_city = True
                else:
                    player.move("s", map_size)  # Move south to simulate staying outside of the city
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
                player.move(direction, map_size)
                if(random.randint(1,100)+ max(abs(player.position[0] - map_size // 2), abs(player.position[1] - map_size // 2))>50):
                    encounter(player, map_size)
                elif direction == "i":
                    item_name = input("Enter the name of the item to equip: ")
                    player.equip_item(item_name)
                else:
                    print("Invalid action!")

    print(f"{player.name} has been defeated. Game over!")

if __name__ == "__main__":
    main()
