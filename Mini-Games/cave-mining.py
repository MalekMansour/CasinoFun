import random
import sys

# Upgrade definitions
PICKAXE_UPGRADES = [
    {"name": "Stone", "efficiency": 1, "cost": 0},
    {"name": "Copper", "efficiency": 1.5, "cost": 2000},
    {"name": "Iron", "efficiency": 2, "cost": 8000},
    {"name": "Gold", "efficiency": 2.5, "cost": 20000},
    {"name": "Diamond", "efficiency": 3, "cost": 50000},
]

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
    "Scuba Diving Suit": 35000,
    "Thermal Suit": 65000,
    "Fur Suit": 95000,
    "Camera": 38000,
    "Rope": 6000,
    "Bucket": 45000,
    "Water Bucket": 56000,
    "Lava Bucket": 80000,
    "Beacon": 25000,
}

AREAS = [
    "Easy", "Medium", "Hard", "Extreme", "Nutty Putty", "Bottomless", "Backrooms",
    "Poolrooms", "Swamp", "Frozen Lake", "Lava Zone", "Hell Hole", "Thai Rescue",
    "Impossible", "The Lost River", "Red Cave"
]

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
        self.photos = []
        self.beacons = []

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
        yield_amount = int(random.randint(5, 15) * self.pickaxe_efficiency)
        earnings = yield_amount * 10
        print(f"\nYou explored {area} and found {yield_amount} ore, earning ${earnings}.")
        self.money += earnings
        # Add to backpack
        if len(self.backpack) < self.backpack_capacity:
            self.backpack.append(("ore", yield_amount))
            print(f"Ore added to backpack (Total items: {len(self.backpack)}/{self.backpack_capacity}).")
        else:
            print("Backpack full! Deposit to chest or empty backpack.")

    def show_status(self):
        print("\n=== Status ===")
        print(f"Money: ${self.money}")
        print(f"Pickaxe: {self.pickaxe}")
        print(f"Backpack: {len(self.backpack)}/{self.backpack_capacity}")
        print(f"Chest: {len(self.chest)}/{self.chest_capacity}")
        print(f"Suits: {', '.join(self.suits) if self.suits else 'None'}")
        print(f"Items: {', '.join(self.items) if self.items else 'None'}")
        print(f"Photos taken: {len(self.photos)}/25")
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
        cost = PICKAXE_UPGRADES[next_level]["cost"]
        if self.money >= cost:
            self.money -= cost
            self.pickaxe_level = next_level
            print(f"Upgraded pickaxe to {self.pickaxe}.")
        else:
            print(f"Need ${cost} to upgrade pickaxe.")

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

    def use_camera(self):
        if "Camera" not in self.items:
            print("You don't have a camera.")
            return
        if len(self.photos) >= 25:
            print("Photo memory full. Delete some first.")
            return
        photo_desc = input("Enter description for the photo: ")
        self.photos.append(photo_desc)
        print(f"Photo taken: '{photo_desc}'")

    def delete_photo(self):
        if not self.photos:
            print("No photos to delete.")
            return
        print("\nPhotos:")
        for idx, p in enumerate(self.photos, 1):
            print(f"{idx}. {p}")
        choice = input("Choose photo to delete (number): ")
        if choice.isdigit() and 1 <= int(choice) <= len(self.photos):
            removed = self.photos.pop(int(choice)-1)
            print(f"Deleted photo: {removed}")
        else:
            print("Invalid choice.")

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
        "8": player.use_camera,
        "9": player.delete_photo,
        "10": player.place_beacon,
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
8. Use Camera
9. Delete Photo
10. Place Beacon
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
