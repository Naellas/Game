class Item:
    def __init__(self, name, item_type, strength_bonus=0, agility_bonus=0, intelligence_bonus=0):
        self.name = name
        self.item_type = item_type
        self.strength_bonus = strength_bonus
        self.agility_bonus = agility_bonus
        self.intelligence_bonus = intelligence_bonus

    def __str__(self):
        return f"{self.name} ({self.item_type}, STR: {self.strength_bonus}, AGI: {self.agility_bonus}, INT: {self.intelligence_bonus})"
    
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
