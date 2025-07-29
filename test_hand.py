import requests
import random
from collections import deque

class TestHand:
    API_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php?id="

    def __init__(self):
        self.deck = deque()
        self.e_deck = []
        self.grave = []
        self.banished = []
        self.hand = []
        self.m_zones = [None] * 5
        self.st_zones = [None] * 6
        self.em_zones = [None] * 2

    def start_game(self):
        self.build_deck("deck.ydk")
        self.first_hand()
        # You can later implement gameplay actions here
        raise NotImplementedError("Unimplemented method 'start_game'")

    def build_deck(self, file_path):
        card_ids = []
        in_main_or_extra = False

        try:
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line == "#main" or line == "#extra":
                        in_main_or_extra = True
                    elif line == "!side":
                        in_main_or_extra = False
                    elif in_main_or_extra and line.isdigit():
                        card_ids.append(line)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return

        for card_id in card_ids:
            try:
                response = requests.get(f"{self.API_URL}{card_id}")
                response.raise_for_status()

                data = response.json()["data"][0]
                name = data["name"]
                ctype = data["type"]

                print(f"[{card_id}] {name} - {ctype}")
                self.deck.append(name)  # or use card_id if simulating draws

            except Exception as e:
                print(f"Failed to fetch card ID {card_id}: {e}")

        random.shuffle(self.deck)

    def first_hand(self):
        if len(self.deck) < 5:
            print("Not enough cards in deck for a starting hand.")
            return
        for _ in range(5):
            self.hand.append(self.deck.popleft())
        print("Starting Hand:", self.hand)

    def move_card(self, source, destination, card_name):
        if card_name in source:
            source.remove(card_name)
            destination.append(card_name)
            print(f"Moved '{card_name}' from {source} to {destination}")
        else:
            print(f"Card '{card_name}' not found in source zone.")

    def mill(self):
        self.grave.append(self.deck.popleft())
#TODO: monsters make an array with their names 
#and index 0 is the xyz
    def overlay(self):
        return

# Only run if this is the main file
if __name__ == "__main__":
    game = TestHand()
    game.start_game()
