# gui.py
import tkinter as tk
from tkinter import messagebox
from character import Character
from item import items
from utilities import display_map, generate_cities, generate_bosses
from encounter import encounter

class RPGGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RPG Game")

        self.map_size = 20
        self.player = None
        self.cities = generate_cities(10, self.map_size)
        self.bosses = generate_bosses(5, self.map_size)
        self.companions = []
        self.in_city = False

        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.label = tk.Label(self.frame, text="Enter your character's name:")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.class_label = tk.Label(self.frame, text="Choose your class:")
        self.class_label.grid(row=1, column=0, padx=10, pady=10)

        self.class_var = tk.StringVar(value="warrior")
        self.class_option = tk.OptionMenu(self.frame, self.class_var, "warrior", "mage", "rogue")
        self.class_option.grid(row=1, column=1, padx=10, pady=10)

        self.start_button = tk.Button(self.frame, text="Start Game", command=self.start_game)
        self.start_button.grid(row=2, column=0, columnspan=2, pady=10)

    def start_game(self):
        name = self.name_entry.get()
        char_class = self.class_var.get()
        self.player = Character(name, char_class)
        self.frame.pack_forget()
        self.create_game_widgets()

    def create_game_widgets(self):
        self.status_label = tk.Label(self.root, text=f"{self.player.name}'s status: Level {self.player.level}, Health {self.player.health}, Mana {self.player.mana}, Position {self.player.position}, Gold {self.player.gold}")
        self.status_label.pack(pady=10)

        self.map_canvas = tk.Canvas(self.root, width=400, height=400)
        self.map_canvas.pack()

        self.update_map()

        self.move_frame = tk.Frame(self.root)
        self.move_frame.pack(pady=10)

        self.move_label = tk.Label(self.move_frame, text="Move:")
        self.move_label.grid(row=0, column=0, padx=10)

        self.move_buttons = {
            "n": tk.Button(self.move_frame, text="North", command=lambda: self.move("n")),
            "s": tk.Button(self.move_frame, text="South", command=lambda: self.move("s")),
            "e": tk.Button(self.move_frame, text="East", command=lambda: self.move("e")),
            "w": tk.Button(self.move_frame, text="West", command=lambda: self.move("w"))
        }
        self.move_buttons["n"].grid(row=0, column=1, padx=5)
        self.move_buttons["s"].grid(row=0, column=2, padx=5)
        self.move_buttons["e"].grid(row=0, column=3, padx=5)
        self.move_buttons["w"].grid(row=0, column=4, padx=5)

    def update_map(self):
        self.map_canvas.delete("all")
        self.map_grid = [["." for _ in range(self.map_size)] for _ in range(self.map_size)]

        for city in self.cities:
            x, y = city
            self.map_grid[y][x] = "C"

        for boss in self.bosses:
            x, y = boss
            self.map_grid[y][x] = "B"

        x, y = self.player.position
        self.map_grid[y][x] = "P"

        for i, row in enumerate(self.map_grid):
            for j, cell in enumerate(row):
                color = "white"
                if cell == "C":
                    color = "blue"
                elif cell == "B":
                    color = "red"
                elif cell == "P":
                    color = "green"
                self.map_canvas.create_rectangle(j * 20, i * 20, (j + 1) * 20, (i + 1) * 20, fill=color)

    def move(self, direction):
        self.player.move(direction, self.map_size)
        self.update_map()
        self.update_status()
        if tuple(self.player.position) in self.cities:
            self.enter_city()

    def update_status(self):
        self.status_label.config(text=f"{self.player.name}'s status: Level {self.player.level}, Health {self.player.health}, Mana {self.player.mana}, Position {self.player.position}, Gold {self.player.gold}")

    def enter_city(self):
        self.in_city = True
        city_action = messagebox.askquestion("City", "Do you want to enter the city?")
        if city_action == "yes":
            self.city_menu()

    def city_menu(self):
        city_window = tk.Toplevel(self.root)
        city_window.title("City Menu")

        potion_button = tk.Button(city_window, text="Buy Potion", command=lambda: self.buy_potion(city_window))
        potion_button.pack(pady=5)

        mana_potion_button = tk.Button(city_window, text="Buy Mana Potion", command=lambda: self.buy_mana_potion(city_window))
        mana_potion_button.pack(pady=5)

        equipment_button = tk.Button(city_window, text="Buy Equipment", command=lambda: self.buy_equipment(city_window))
        equipment_button.pack(pady=5)

        leave_button = tk.Button(city_window, text="Leave City", command=city_window.destroy)
        leave_button.pack(pady=5)

    def buy_potion(self, window):
        self.player.buy_potion()
        self.update_status()
        window.destroy()

    def buy_mana_potion(self, window):
        self.player.buy_mana_potion()
        self.update_status()
        window.destroy()

    def buy_equipment(self, window):
        equipment_window = tk.Toplevel(window)
        equipment_window.title("Buy Equipment")

        for item in items:
            item_button = tk.Button(equipment_window, text=str(item), command=lambda i=item: self.purchase_item(i, equipment_window))
            item_button.pack(pady=5)

    def purchase_item(self, item, window):
        self.player.buy_equipment(item)
        self.update_status()
        window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RPGGameGUI(root)
    root.mainloop()