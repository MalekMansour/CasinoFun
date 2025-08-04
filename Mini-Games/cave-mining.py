import random
import sys

# Upgrade definitions (cost = required ingots to upgrade pickaxe)
PICKAXE_UPGRADES = [
    {"name": "Stone", "efficiency": 1, "cost": 0},
    {"name": "Copper", "efficiency": 1.5, "cost": 4},   # 4kg Copper ingots
    {"name": "Iron", "efficiency": 2, "cost": 10},    # 10kg Iron ingots
    {"name": "Gold", "efficiency": 2.5, "cost": 24},   # 24kg Gold ingots
    {"name": "Diamond", "efficiency": 3, "cost": 36}, # 36kg Diamond ingots
]

# Backpack and chest upgrades
BACKPACK_UPGRADES = [
    {"capacity": 100, "cost": 0},
    {"capacity": 150, "cost": 4000},
    {"capacity": 200, "cost": 10000},
    {"capacity": 250, "cost": 24000},
    {"capacity": 300, "cost": 45000},
]
CHEST_UPGRADES = [
    {"capacity": 30, "cost": 0},
    {"capacity": 60, "cost": 3000},
    {"capacity": 90, "cost": 12000},
    {"capacity": 120, "cost": 36000},
    {"capacity": 150, "cost": 60000},
]

SHOP_ITEMS = {
    "Water Bucket": 56000,
    "Lava Bucket": 80000,
    "Bucket": 45000,
    "Beacon": 25000,
    "Scuba Diving Suit": 35000,
    "Thermal Suit": 65000,
    "Fur Suit": 95000,
}

AREAS = [
    "Easy", "Medium", "Hard", "Extreme", "Nutty Putty", "Bottomless", "Backrooms",
    "Poolrooms", "Swamp", "Frozen Lake", "Lava Zone", "Hell Hole", "Thai Rescue",
    "Impossible", "The Lost River", "Red Cave"
]

# Map pickaxe level to ore type
ORE_TYPES = ["Copper", "Iron", "Gold", "Diamond"]

class Player:
    def __init__(self):
        self.money = 0
        self.pickaxe_level = 0
        self.backpack_level = 0
        self.chest_level = 0
        self.backpack = []
        self.chest = []
        self.suits = set()
        self.items = set()
        self.beacons = []
        self.ingots = {ore: 0 for ore in ORE_TYPES}

    @property
    def pickaxe(self):
        return PICKAXE_UPGRADES[self.pickaxe_level]["name"]

    @property
    def pickaxe_efficiency(self):
        return PICKAXE_UPGRADES[self.pickaxe_level]["efficiency"]

    @property
    def backpack_capacity(self):
        return BACKPACK_UPGRADES[self.backpack_level]["capacity"]

    @property
    def chest_capacity(self):
        return CHEST_UPGRADES[self.chest_level]["capacity"]

    def explore(self):
        print("\nAreas:")
        for idx, area in enumerate(AREAS):
            print(f"{idx+1}. {area}")
        choice = input("Choose an area to explore (number): ")
        if not choice.isdigit() or not (1 <= int(choice) <= len(AREAS)):
            print("Invalid choice.")
            return
        area = AREAS[int(choice)-1]
        ore_type = ORE_TYPES[min(self.pickaxe_level, len(ORE_TYPES)-1)]
        yield_amount = int(random.randint(5, 15) * self.pickaxe_efficiency)
        earnings = yield_amount * 10
        print(f"\nYou explored {area} and found {yield_amount}kg of {ore_type} ore.")
        self.money += earnings
        print(f"You earned ${earnings} from selling surplus ore.")
        # Add to backpack
        if len(self.backpack) < self.backpack_capacity:
            self.backpack.append((f"{ore_type} Ore", yield_amount))
            print(f"Ore added to backpack ({len(self.backpack)}/{self.backpack_capacity}).")
        else:
            print("Backpack full! Deposit to chest or empty backpack.")

    def show_status(self):
        print("\n=== Status ===")
        print(f"Money: ${self.money}")
        print(f"Pickaxe: {self.pickaxe}")
        print(f"Backpack: {len(self.backpack)}/{self.backpack_capacity}")
        print(f"Chest: {len(self.chest)}/{self.chest_capacity}")
        ingot_status = ", ".join(f"{ore}: {amt}kg" for ore, amt in self.ingots.items())
        print(f"Ingots: {ingot_status}")
        print(f"Suits: {', '.join(self.suits) if self.suits else 'None'}")
        print(f"Items: {', '.join(self.items) if self.items else 'None'}")
        print(f"Beacons placed: {len(self.beacons)}")
        print("==============")

    def deposit_backpack(self):
        while self.backpack and len(self.chest) < self.chest_capacity:
            self.chest.append(self.backpack.pop(0))
        print(f"Deposited items. Chest now {len(self.chest)}/{self.chest_capacity}")

    def upgrade_pickaxe(self):
        next_level = self.pickaxe_level + 1
        if next_level >= len(PICKAXE_UPGRADES):
            print("Your pickaxe is at max level.")
            return
        ore_type = PICKAXE_UPGRADES[next_level]["name"]
        cost = PICKAXE_UPGRADES[next_level]["cost"]
        if self.ingots.get(ore_type, 0) >= cost:
            self.ingots[ore_type] -= cost
            self.pickaxe_level = next_level
            print(f"Upgraded pickaxe to {self.pickaxe}.")
        else:
            print(f"Need {cost}kg of {ore_type} ingots to upgrade pickaxe.")

    def upgrade_backpack(self):
        next_level = self.backpack_level + 1
        if next_level >= len(BACKPACK_UPGRADES):
            print("Backpack is at max capacity.")
            return
        cost = BACKPACK_UPGRADES[next_level]["cost"]
        if self.money >= cost:
            self.money -= cost
            self.backpack_level = next_level
            print(f"Upgraded backpack to capacity {self.backpack_capacity}.")
        else:
            print(f"Need ${cost} to upgrade backpack.")

    def upgrade_chest(self):
        next_level = self.chest_level + 1
        if next_level >= len(CHEST_UPGRADES):
            print("Chest is at max capacity.")
            return
        cost = CHEST_UPGRADES[next_level]["cost"]
        if self.money >= cost:
            self.money -= cost
            self.chest_level = next_level
            print(f"Upgraded chest to capacity {self.chest_capacity}.")
        else:
            print(f"Need ${cost} to upgrade chest.")

    def shop(self):
        print("\n=== Shop ===")
        for idx, (item, cost) in enumerate(SHOP_ITEMS.items(), 1):
            print(f"{idx}. {item} - ${cost}")
        choice = input("Choose item to buy (number): ")
        if not choice.isdigit() or not (1 <= int(choice) <= len(SHOP_ITEMS)):
            print("Invalid choice.")
            return
        item = list(SHOP_ITEMS.keys())[int(choice)-1]
        cost = SHOP_ITEMS[item]
        if self.money >= cost:
            self.money -= cost
            if item in ("Scuba Diving Suit", "Thermal Suit", "Fur Suit"):
                self.suits.add(item)
            else:
                self.items.add(item)
            print(f"Purchased {item}.")
        else:
            print("Not enough money.")

    def smelt(self):
        if "Lava Bucket" not in self.items:
            print("You need a Lava Bucket to fuel the furnace.")
            return
        # Gather available ores in chest
        ore_inventory = {}
        for typ, amt in self.chest:
            if "Ore" in typ:
                ore_type = typ.replace(" Ore", "")
                ore_inventory[ore_type] = ore_inventory.get(ore_type, 0) + amt
        if not ore_inventory:
            print("No ore in chest to smelt.")
            return
        print("\nOre in Chest:")
        for idx, (ore, amt) in enumerate(ore_inventory.items(), 1):
            print(f"{idx}. {ore} Ore - {amt}kg")
        choice = input("Choose ore to smelt (number): ")
        if not choice.isdigit() or not (1 <= int(choice) <= len(ore_inventory)):
            print("Invalid choice.")
            return
        ore_type = list(ore_inventory.keys())[int(choice)-1]
        available = ore_inventory[ore_type]
        amount = input(f"Enter kg of {ore_type} Ore to smelt (max {available}): ")
        if not amount.isdigit() or not (1 <= int(amount) <= available):
            print("Invalid amount.")
            return
        amount = int(amount)
        # Remove ore from chest
        removed = 0
        new_chest = []
        for typ, amt in self.chest:
            if typ == f"{ore_type} Ore" and removed < amount:
                take = min(amt, amount - removed)
                leftover = amt - take
                removed += take
                if leftover > 0:
                    new_chest.append((typ, leftover))
            else:
                new_chest.append((typ, amt))
        self.chest = new_chest
        # Consume one Lava Bucket
        self.items.remove("Lava Bucket")
        # Add ingots
        self.ingots[ore_type] += amount
        print(f"Smelted {amount}kg of {ore_type} Ore into {amount}kg of {ore_type} Ingots.")

    def place_beacon(self):
        if "Beacon" not in self.items:
            print("You don't have a beacon.")
            return
        area = input("Enter the name of the area to place beacon: ")
        if area:
            self.beacons.append(area)
            print(f"Beacon placed at {area}.")


def main():
    player = Player()
    actions = {
        "1": player.show_status,
        "2": player.explore,
        "3": player.deposit_backpack,
        "4": player.upgrade_pickaxe,
        "5": player.upgrade_backpack,
        "6": player.upgrade_chest,
        "7": player.shop,
        "8": player.smelt,
        "9": player.place_beacon,
        "0": lambda: sys.exit(0)
    }

    while True:
        print("""
=== Menu ===
1. Show Status
2. Explore
3. Deposit Backpack to Chest
4. Upgrade Pickaxe
5. Upgrade Backpack
6. Upgrade Chest
7. Shop
8. Smelt Ore in Furnace
9. Place Beacon
0. Exit
""")
        choice = input("Choose an action: ")
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
