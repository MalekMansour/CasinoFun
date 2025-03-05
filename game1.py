import tkinter as tk
from tkinter import messagebox
import random

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Desert Survival Game")

        # Player stats
        self.health = 100
        self.hunger = 100
        self.thirst = 100
        self.money = 10
        self.miles_walked = 0

        # Inventory
        self.inventory = {
            'Canned Soup': 5,
            'Water Bottle': 5,
            'Money': 10,
        }

        # Set up UI elements
        self.setup_ui()

    def setup_ui(self):
        # Top Frame for stats (Health, Hunger, Thirst, Miles, Money)
        self.stats_frame = tk.Frame(self.root)
        self.stats_frame.pack(side=tk.TOP, fill=tk.X)

        self.health_label = tk.Label(self.stats_frame, text=f"Health: {self.health}%")
        self.health_label.pack(side=tk.LEFT)

        self.hunger_label = tk.Label(self.stats_frame, text=f"Hunger: {self.hunger}%")
        self.hunger_label.pack(side=tk.LEFT)

        self.thirst_label = tk.Label(self.stats_frame, text=f"Thirst: {self.thirst}%")
        self.thirst_label.pack(side=tk.LEFT)

        self.miles_label = tk.Label(self.stats_frame, text=f"Miles Walked: {self.miles_walked}")
        self.miles_label.pack(side=tk.LEFT)

        self.money_label = tk.Label(self.stats_frame, text=f"Money: ${self.money}")
        self.money_label.pack(side=tk.LEFT)

        # Bottom Frame for actions (Walk, Eat, Drink)
        self.action_frame = tk.Frame(self.root)
        self.action_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.walk_button = tk.Button(self.action_frame, text="Walk", command=self.walk)
        self.walk_button.pack(side=tk.LEFT)

        self.eat_button = tk.Button(self.action_frame, text="Eat", command=self.eat)
        self.eat_button.pack(side=tk.LEFT)

        self.drink_button = tk.Button(self.action_frame, text="Drink", command=self.drink)
        self.drink_button.pack(side=tk.LEFT)

        # Inventory display (can expand later with backpack button)
        self.inventory_frame = tk.Frame(self.root)
        self.inventory_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.inventory_label = tk.Label(self.inventory_frame, text="Inventory: " + self.display_inventory())
        self.inventory_label.pack(side=tk.LEFT)

        # Map icon in the top right (for opening map)
        self.map_button = tk.Button(self.root, text="Map", command=self.open_map)
        self.map_button.pack(side=tk.TOP, anchor=tk.E)

    def walk(self):
        # Walking reduces hunger and thirst, and increases miles walked
        if self.hunger <= 0 or self.thirst <= 0:
            messagebox.showwarning("Game Over", "You died due to hunger or thirst!")
            self.root.quit()
        else:
            self.miles_walked += 1
            self.hunger -= 5
            self.thirst -= 10
            self.update_stats()
            self.check_for_checkpoint()

    def eat(self):
        # You can eat Canned Soup to restore hunger
        if 'Canned Soup' in self.inventory and self.inventory['Canned Soup'] > 0:
            self.hunger = min(self.hunger + 50, 100)  # Restore 50% hunger
            self.inventory['Canned Soup'] -= 1
            self.update_stats()
        else:
            messagebox.showwarning("Inventory", "No Canned Soup to eat!")

    def drink(self):
        # You can drink Water Bottle to restore thirst
        if 'Water Bottle' in self.inventory and self.inventory['Water Bottle'] > 0:
            self.thirst = min(self.thirst + 100, 100)  # Restore 100% thirst
            self.inventory['Water Bottle'] -= 1
            self.update_stats()
        else:
            messagebox.showwarning("Inventory", "No Water Bottle to drink!")

    def check_for_checkpoint(self):
        # Random chance to encounter a checkpoint
        if random.random() < 0.1:  
            checkpoint_type = random.choice(['Empty', 'Crate', 'Important'])
            if checkpoint_type == 'Crate':
                self.encounter_crate()
            elif checkpoint_type == 'Important':
                self.encounter_important_checkpoint()

    def encounter_crate(self):
        # Randomly determine what's in the crate
        crate_items = ['Food', 'Water', 'Bandages', 'Knife', 'Sword', 'Bomb']
        item = random.choice(crate_items)
        if item == 'Bomb' and random.random() < 0.02:
            self.health = 0  
            self.update_stats()
            messagebox.showwarning("Game Over", "You were killed by a bomb!")
            self.root.quit()
        else:
            messagebox.showinfo("Crate", f"You found a {item} in the crate!")

    def encounter_important_checkpoint(self):
        # Implement logic for important checkpoints (Shop, Gas Station, etc.)
        messagebox.showinfo("Important Checkpoint", "You have encountered an important checkpoint!")

    def update_stats(self):
        # Update stats labels
        self.health_label.config(text=f"Health: {self.health}%")
        self.hunger_label.config(text=f"Hunger: {self.hunger}%")
        self.thirst_label.config(text=f"Thirst: {self.thirst}%")
        self.miles_label.config(text=f"Miles Walked: {self.miles_walked}")
        self.money_label.config(text=f"Money: ${self.money}")
        self.inventory_label.config(text="Inventory: " + self.display_inventory())

    def display_inventory(self):
        return ', '.join([f"{item}: {qty}" for item, qty in self.inventory.items()])

root = tk.Tk()
game = Game(root)
root.mainloop()
