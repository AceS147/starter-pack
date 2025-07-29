import requests
import random
from pathlib import Path 
from collections import deque

class TestHand:
    API_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php?id="

    def __init__(self):
        self.deck = deque()
        self.e_deck = []
        self.grave = []
        self.banished = []
        self.hand = []
        self.m_zones = [[None],[None],[None],[None],[None]]
        self.st_zones = [None,None,None,None,None]
        self.em_zones = [None,None]

    def start_game(self):
        filename = input("Enter the name of the desired ydk file: ")
        if not filename.endswith(".ydk"):
            filename += ".ydk"
        self.build_deck(filename)
        self.first_hand()
        print("Extra Deck: "+ ", ".join(self.e_deck))
        #print(len(self.e_deck))
        print("Extra Monster Zones" + ", ".join(self.em_zones))
        print("Monster Zones" + ", ".join(self.m_zones))
        print("Spell/Trap Zones" + ", ".join(self.st_zones))

    def build_deck(self, filename):
        card_ids = []
        in_main_or_extra = False
        in_extra = False

        try:
            file_path = Path.cwd() / filename
            if not file_path.exists():
                raise(FileNotFoundError)
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line == "#main":
                        in_main_or_extra = True
                    elif line == "#extra":
                        card_ids.append("EXTRA")
                    elif line == "!side":
                        in_main_or_extra = False
                    elif in_main_or_extra and line.isdigit():
                        card_ids.append(line)

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return

        for card_id in card_ids:
            try:
                if card_id.isdigit():
                    response = requests.get(f"{self.API_URL}{card_id}")
                    response.raise_for_status()

                    data = response.json()["data"][0]
                    name = data["name"]
                    if not in_extra:
                        self.deck.append(name)
                    else:
                        self.e_deck.append(name)
                else:
                    in_extra = True
                    continue

            except Exception as e:
                print(f"Failed to fetch card ID {card_id}: {e}")

        random.shuffle(self.deck)
        # print(len(self.e_deck))
        # print(len(self.deck))

    def first_hand(self):
        if len(self.deck) < 5:
            print("Not enough cards in deck for a starting hand.")
            return
        for _ in range(5):
            self.hand.append(self.deck.popleft())
        print("Starting Hand:", self.hand)

    def move_card(self, source_name, destination_name, card_name):
        source = getattr(self, source_name)
        destination = getattr(self, destination_name)
        if card_name in source:
            source.remove(card_name)
            destination.append(card_name)
            print(f"Moved '{card_name}' from {source} to {destination}")
        else:
            print(f"Card '{card_name}' not found in source zone.")

    def mill(self):
        self.grave.append(self.deck.popleft())

    def overlay(self,field_pos_1,field_pos_2):
        self.m_zones[field_pos_1+1][0].append(self.m_zones[field_pos_2+1][0])
        self.m_zones[field_pos_2][0] = None


# Only run if this is the main file
if __name__ == "__main__":
    game = TestHand()
    game.start_game()

