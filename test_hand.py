import requests
import random
from pathlib import Path 
from collections import deque

#TODO: simplify inputs & continue testing
class TestHand:
    API_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php?id="

    def __init__(self):
        self.deck = deque()
        self.e_deck = []
        self.grave = []
        self.banished = []
        self.hand = []
        self.m_zones = [[None],[None],[None],[None],[None]]
        self.fs_zone = []
        self.st_zones = [None,None,None,None,None]
        self.em_zones = [None,None]

    def start_game(self):
        filename = input("Enter the name of the desired ydk file: ")
        if not filename.endswith(".ydk"):
            filename += ".ydk"
        self.build_deck(filename)
        self.first_hand()
        #print("Extra Deck: "+ ", ".join(self.e_deck))
        #print(len(self.e_deck))
        # print("Extra Monster Zones: " + ", ".join([str(zone) if zone is not None else "Empty" for zone in self.em_zones]))
        # print("Monster Zones: " + ", ".join([str(zone[0]) if zone[0] is not None else "Empty" for zone in self.m_zones]))
        # print("Spell/Trap Zones: " + ", ".join([str(zone) if zone is not None else "Empty" for zone in self.st_zones]))

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
        print("Starting Hand: "+ ", ".join(self.hand))

    def move_card(self, source_name, destination_name, card_name):
        source = getattr(self, source_name)
        destination = getattr(self, destination_name)
        if card_name in source:
            source.remove(card_name)
            #destination.append(card_name)
            if source_name == "deck" and not ((destination_name == "m_zones") or (destination_name == "st_zones") or (destination_name == "fs_zone")):
                destination.append(card_name)
                return
            for x in range(len(destination)):
                if destination[x] == None:
                    destination[x] = card_name
                    break
                else:
                    continue
            print(f"Moved '{card_name}' from {source} to {destination}")
        else:
            print(f"Card '{card_name}' not found in source zone.")

    def mill(self):
        self.grave.append(self.deck.popleft())

    def draw(self):
        self.hand.append(self.deck.popleft)

    def overlay(self,field_pos_1,field_pos_2):
        self.m_zones[field_pos_1+1][0].append(self.m_zones[field_pos_2+1][0])
        self.m_zones[field_pos_2][0] = None

    def check(self,location_name):
        match(location_name):
            case("Hand"):
                print("Hand: " +", ".join(self.hand))
            case("Grave"):
                print("Graveyard: "+ ", ".join(self.grave))
            case("Banishment"):
                print("Banishment: "+", ".join(self.banished))
            case("Field"):
                print("Extra Monster Zones: " + ", ".join([str(zone) if zone is not None else "Empty" for zone in self.em_zones]))
                print("Field Spell Zone: " + ", ".join([str(zone) if zone is not None else "Empty" for zone in self.fs_zone]))
                print("Monster Zones: " + ", ".join([str(zone[0]) if zone[0] is not None else "Empty" for zone in self.m_zones]))
                print("Spell/Trap Zones: " + ", ".join([str(zone) if zone is not None else "Empty" for zone in self.st_zones]))

    def perform_action(self):
        action = input("Choose an action (move, mill, draw, overlay, check, quit): ").strip().lower()
        #TODO: be sure to specify what zones on field cards are going to ie monster or s/t
        if action == "move":
            source = input("Enter source zone (e.g. hand, grave, deck): ").strip().lower()
            destination = input("Enter destination zone (e.g. hand, grave, m_zones, st_zones): ").strip().lower()
            card_name = input("Enter card name: ").strip()
            self.move_card(source, destination, card_name)

        elif action == "mill":
            self.mill()

        elif action == "draw":
            self.draw()

        elif action == "overlay":
            try:
                pos1 = int(input("Enter the index of the first monster zone: "))
                pos2 = int(input("Enter the index of the second monster zone to overlay: "))
                self.overlay(pos1, pos2)
            except ValueError:
                print("Invalid input. Please enter integer positions.")

        elif action == "check":
            zone = input("Which zone do you want to check? (hand, grave, field): ").strip().capitalize()
            self.check(zone)

        elif action == "quit":
            confirm = input("Are you sure? Yes or No ")
            if(confirm == "Yes"):
                print("Thank you for playing!")
                quit()
            else:
                self.perform_action()
        else:
            print("Invalid action.")

if __name__ == "__main__":
    game = TestHand()
    game.start_game()
    while(True):
          game.perform_action()

