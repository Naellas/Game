# utilities.py
import random
from character import Companion

def display_map(character, cities, bosses, map_size):
    map_grid = [["." for _ in range(map_size)] for _ in range(map_size)]

    for city in cities:
        x, y = city
        map_grid[y][x] = "C"

    for boss in bosses:
        x, y = boss
        map_grid[y][x] = "B"

    x, y = character.position
    map_grid[y][x] = "P"

    for row in map_grid:
        print(" ".join(row))

def generate_city_names(num_cities):
    return [f"City_{i+1}" for i in range(num_cities)]

def generate_cities(num_cities, map_size):
    cities = []
    while len(cities) < num_cities:
        x = random.randint(0, map_size - 1)
        y = random.randint(0, map_size - 1)
        if (x, y) not in cities:
            cities.append((x, y))
    return cities

def generate_bosses(num_bosses, map_size):
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
