import tkinter as tk
import random

class ZombieGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Zombie Survival Game")
        self.root.configure(bg="black")
        
        self.inventory = {"soup": 5, "water": 5, "weapons": {"knife": 0, "gun": 0, "axe": 0, "sword": 0}}
        self.health = 100
        self.hunger = 100
        self.thirst = 100
        self.miles_walked = 0
        
        self.info_label = tk.Label(root, text="", bg="black", fg="#94FC13", font=("Courier", 12))
        self.info_label.pack()
        
        self.text = tk.Text(root, height=20, width=60, bg="black", fg="#94FC13", font=("Courier", 12))
        self.text.pack()
        
        self.button_frame = tk.Frame(root, bg="black")
        self.button_frame.pack()
        
        self.create_main_buttons()
        
        self.update_info()
        self.update_text("Game Started! You have 5 cans of soup and 5 bottles of water.")
    
    def update_info(self):
        self.info_label.config(text=f"Health: {self.health} | Hunger: {self.hunger} | Thirst: {self.thirst} | Miles: {self.miles_walked}")
    
    def update_text(self, message):
        self.text.insert(tk.END, message + "\n")
        self.text.see(tk.END)
        self.update_info()
    
    def create_main_buttons(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        
        tk.Button(self.button_frame, text="Walk", command=self.walk, bg="black", fg="#94FC13").pack(side=tk.LEFT)
        tk.Button(self.button_frame, text="Eat", command=self.eat, bg="black", fg="#94FC13").pack(side=tk.LEFT)
        tk.Button(self.button_frame, text="Drink", command=self.drink, bg="black", fg="#94FC13").pack(side=tk.LEFT)
        tk.Button(self.button_frame, text="Inventory", command=self.show_inventory, bg="black", fg="#94FC13").pack(side=tk.LEFT)
    
    def eat(self):
        if self.inventory["soup"] > 0:
            self.inventory["soup"] -= 1
            self.hunger = min(100, self.hunger + 20)
            self.update_text("You ate a can of soup.")
        else:
            self.update_text("You have no soup left!")
    
    def drink(self):
        if self.inventory["water"] > 0:
            self.inventory["water"] -= 1
            self.thirst = min(100, self.thirst + 20)
            self.update_text("You drank a bottle of water.")
        else:
            self.update_text("You have no water left!")
    
    def show_inventory(self):
        weapons = ", ".join([f"{w} ({c})" for w, c in self.inventory["weapons"].items() if c > 0]) or "None"
        items = f"Soup: {self.inventory['soup']}, Water: {self.inventory['water']}, Weapons: {weapons}"
        self.update_text("Inventory: " + items)
    
    def walk(self):
        miles = random.randint(1, 10)
        self.miles_walked += miles
        self.health = min(100, self.health + (miles * 2))
        self.hunger = max(0, self.hunger - 10)
        self.thirst = max(0, self.thirst - 10)
        
        if self.hunger == 0 or self.thirst == 0:
            self.health = 0
        
        if self.health <= 0:
            self.update_text("You died! Game Over!")
            return
        
        event_roll = random.random()
        if event_roll < 0.2:
            self.zombie_encounter()
        elif event_roll < 0.4:
            self.crate_drop()
        else:
            self.update_text(f"You walked {miles} miles.")
    
    def zombie_encounter(self):
        self.update_text("A zombie approaches!")
        available_weapons = [w for w, c in self.inventory["weapons"].items() if c > 0]
        if available_weapons:
            self.update_text("Choose a weapon to fight!")
            self.create_decision_buttons([(weapon.capitalize(), lambda w=weapon: self.fight(w)) for weapon in available_weapons] + [("Run", self.run_away)])
        else:
            self.update_text("You have no weapons! Prepare to fight bare-handed!")
            self.fight(None)
    
    def fight(self, weapon):
        success = random.random()
        if weapon:
            self.update_text(f"You attack the zombie with your {weapon}!")
            if success > 0.3:
                self.update_text("You killed the zombie!")
            else:
                self.health -= 20
                self.update_text("The zombie injured you! -20 health")
        else:
            if success > 0.6:
                self.update_text("You barely managed to kill the zombie!")
            else:
                self.health -= 30
                self.update_text("The zombie badly injured you! -30 health")
        self.create_main_buttons()
    
    def run_away(self):
        if random.random() > 0.5:
            self.update_text("You successfully ran away!")
        else:
            self.health -= 15
            self.update_text("You failed to escape! The zombie attacked you! -15 health")
        self.create_main_buttons()
    
    def crate_drop(self):
        self.update_text("You found a crate! Open it?")
        self.create_decision_buttons([("Open", self.open_crate), ("Ignore", self.create_main_buttons)])
    
    def open_crate(self):
        loot = random.choices(["empty", "soup", "water", "weapon", "bomb"], [0.3, 0.3, 0.3, 0.08, 0.02])[0]
        if loot == "soup":
            self.inventory["soup"] += 1
            self.update_text("You found a can of soup!")
        elif loot == "water":
            self.inventory["water"] += 1
            self.update_text("You found a bottle of water!")
        elif loot == "weapon":
            weapon = random.choice(list(self.inventory["weapons"].keys()))
            self.inventory["weapons"][weapon] += 1
            self.update_text(f"You found a {weapon}!")
        elif loot == "bomb":
            self.update_text("The crate exploded! You died.")
            self.health = 0
        else:
            self.update_text("The crate was empty.")
        self.create_main_buttons()
    
if __name__ == "__main__":
    root = tk.Tk()
    game = ZombieGame(root)
    root.mainloop()
