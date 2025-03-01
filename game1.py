import tkinter as tk
from tkinter import messagebox
import random

# Game Variables
health = 100
hunger = 100
thirst = 100
money = 20
miles_walked = 0
inventory = []
backpack = []
weapons = []
checkpoints = list(range(120))

# Items and Prices
shop_items = {
    "Water Bottle": 2,
    "Canned Peas": 2,
    "Canned Soup": 3,
    "Bandage": 4,
    "Knife": 12,
    "Sword": 24,
    "Gun": 90,
    "Medkit": 18,
}

sell_prices = {
    "Water Bottle": 1,
    "Canned Peas": 1,
    "Canned Soup": 1,
    "Bandage": 1,
    "Knife": 8,
    "Sword": 18,
    "Gun": 30,
    "Medkit": 16,
    "Beer": 7,
    "Wine": 12,
}

# Tkinter Setup
root = tk.Tk()
root.title("Desert Survival Game")
root.geometry("800x600")
root.configure(bg="black")

def update_status():
    status_label.config(text=f"Health: {health}% | Hunger: {hunger}% | Thirst: {thirst}% | Miles Walked: {miles_walked}")
    money_label.config(text=f"Money: ${money}")

def walk():
    global hunger, thirst, miles_walked
    hunger -= 5
    thirst -= 10
    miles_walked += 1
    update_status()
    check_for_checkpoint()
    if hunger <= 0 or thirst <= 0:
        messagebox.showinfo("Game Over", "You died from hunger or thirst!")
        root.quit()

def check_for_checkpoint():
    if miles_walked in checkpoints:
        result = random.randint(1, 100)
        if result <= 30:
            open_crate()
        elif result == 100:
            random_event()

def open_crate():
    global inventory
    roll = random.randint(1, 100)
    if roll <= 30:
        item = "Canned Peas"
    elif roll <= 60:
        item = "Water Bottle"
    elif roll <= 90:
        item = "Bandage"
    elif roll <= 94:
        item = "Knife"
    elif roll <= 98:
        item = "Sword"
    else:
        messagebox.showinfo("Crate", "The crate exploded! You died.")
        root.quit()
        return
    inventory.append(item)
    messagebox.showinfo("Crate", f"You found: {item}")
    update_inventory()

def update_inventory():
    inventory_label.config(text=f"Inventory: {', '.join(inventory)}")

def eat():
    global hunger
    if "Canned Peas" in inventory:
        inventory.remove("Canned Peas")
        hunger += 50
    elif "Canned Soup" in inventory:
        inventory.remove("Canned Soup")
        hunger += 50
        thirst += 20
    else:
        messagebox.showinfo("Eat", "No food available!")
    update_status()
    update_inventory()

def drink():
    global thirst
    if "Water Bottle" in inventory:
        inventory.remove("Water Bottle")
        thirst = 100
    elif "Koka Kola Drink" in inventory:
        inventory.remove("Koka Kola Drink")
        thirst += 50
    elif "Energy Drink" in inventory:
        inventory.remove("Energy Drink")
        thirst += 70
    elif "Coffee" in inventory:
        inventory.remove("Coffee")
        thirst += 60
    else:
        messagebox.showinfo("Drink", "No drinks available!")
    update_status()
    update_inventory()

def open_shop():
    shop_window = tk.Toplevel(root)
    shop_window.title("Shop")
    shop_window.geometry("300x400")
    shop_window.configure(bg="green")
    
    tk.Label(shop_window, text="Old Man Jerry's Shop", bg="green", fg="black", font=("Arial", 14)).pack()
    
    for item, price in shop_items.items():
        tk.Button(shop_window, text=f"Buy {item} - ${price}", command=lambda i=item, p=price: buy_item(i, p)).pack()

def buy_item(item, price):
    global money
    if money >= price:
        money -= price
        inventory.append(item)
        update_status()
        update_inventory()
    else:
        messagebox.showinfo("Shop", "Not enough money!")

# UI Elements
status_label = tk.Label(root, text="", font=("Arial", 14), bg="black", fg="green")
status_label.pack()
money_label = tk.Label(root, text="", font=("Arial", 14), bg="black", fg="green")
money_label.pack()
inventory_label = tk.Label(root, text="Inventory: ", font=("Arial", 12), bg="black", fg="green")
inventory_label.pack()

walk_button = tk.Button(root, text="Walk", command=walk, font=("Arial", 12), bg="green", fg="black")
walk_button.pack()
eat_button = tk.Button(root, text="Eat", command=eat, font=("Arial", 12), bg="green", fg="black")
eat_button.pack()
drink_button = tk.Button(root, text="Drink", command=drink, font=("Arial", 12), bg="green", fg="black")
drink_button.pack()
shop_button = tk.Button(root, text="Shop", command=open_shop, font=("Arial", 12), bg="green", fg="black")
shop_button.pack()

update_status()
root.mainloop()
