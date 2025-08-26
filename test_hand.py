import requests
import random
from pathlib import Path 
from collections import deque
from ratelimit import limits, sleep_and_retry
from card import Card

#TODO: add in extra deck stuff to move_card()
class TestHand:
    API_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php?id="

    def __init__(self):
        self.deck = deque()
        self.e_deck = []
        self.grave = []
        self.banished = []
        self.hand = []
        self.m_zones = [[None],[None],[None],[None],[None]]
        self.fs_zone = [None]
        self.st_zones = [None,None,None,None,None]
        self.em_zones = [[None],[None]]

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

    @limits(calls=20,period=1)
    @sleep_and_retry
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
                   
                    card = Card(data["name"],data["desc"],data["type"])

                    if not in_extra:
                        self.deck.append(card)
                    else:
                        self.e_deck.append(card)
                else:
                    in_extra = True
                    continue

            except Exception as e:
                print(f"Failed to fetch card ID {card_id}: {e}")

        if ((len(self.deck) < 40) and (len(self.deck)) > 60):
            print("Sorry. There is not enough cards in the Main Deck. Please add more cards to the main deck and try again.")
            return
        if (len(self.e_deck) > 15):
            print("Sorry. There are too manmy cards in the Extra Deck. Please remove some and try again.")
            return
        random.shuffle(self.deck)
        # print(len(self.e_deck))
        # print(len(self.deck))

    def first_hand(self):
        if len(self.deck) < 5:
            print("Not enough cards in deck for a starting hand.")
            return
        for _ in range(5):
            self.hand.append(self.deck.popleft())
        print("Starting Hand: " + ", ".join(str(card) for card in self.hand))

    def move_card(self, source_name, destination_name, card_name):
        source = getattr(self, source_name)
        destination = getattr(self, destination_name)
        if source_name == "deck" and destination_name == "e_deck":
            print("You cannot put cards from the main deck in the extra deck")
            return
        if source_name == "e_deck" and destination_name == "deck":
            print("You cannot put cards form the extra deck in the main deck")
            return
        for target in source:
            if card_name == target.name:
                source.remove(target)
                #destination.append(card_name)
                if source_name == "deck" and not ((destination_name == "m_zones") or (destination_name == "st_zones") or (destination_name == "fs_zone")):
                    destination.append(target)
                    return
                for x in range(len(destination)):
                    if destination_name == "m_zones":
                        if destination[x][0] == None:
                            destination[x][0] = target
                            break
                    if destination[x] == None:
                        destination[x] = target
                        break
                    else:
                        continue
                print(f"Moved '{card_name}' from {source} to {destination}")
                return
            
        print(f"Card '{card_name}' not found in source zone.")
        return

    def mill(self):
        self.grave.append(self.deck.popleft())

    def draw(self):
        self.hand.append(self.deck.popleft())

    def overlay(self,field_pos_1,field_pos_2):
        self.m_zones[field_pos_1+1][0].append(self.m_zones[field_pos_2+1][0])
        self.m_zones[field_pos_2][0] = None

    def check(self, location_name):
        zone = None 
        match location_name:
            case "Hand":
                print("Hand: " + ", ".join(str(card) for card in self.hand))
                zone = self.hand
            case "Grave":
                print("Graveyard: " + ", ".join(str(card) for card in self.grave))
                zone = self.grave
            case "Banishment":
                print("Banishment: " + ", ".join(str(card) for card in self.banished))
                zone = self.banished
            case "Field":
                print("Extra Monster Zones: " + ", ".join([str(zone) if zone is not None else "Empty" for zone in self.em_zones]))
                print("Field Spell Zone: " + ", ".join([str(zone) if zone is not None else "Empty" for zone in self.fs_zone]))
                print("Monster Zones: " + ", ".join([str(zone[0]) if zone[0] is not None else "Empty" for zone in self.m_zones]))
                print("Spell/Trap Zones: " + ", ".join([str(zone) if zone is not None else "Empty" for zone in self.st_zones]))
                # For field we don’t have a single zone list, so no simple zone variable
             

        further_check = input("Do you wish to check the effect of a card in this zone? (y)es or (n)o ")
        if further_check.lower() == "y":
            card_name = input("Enter the card’s name: ").strip()

            # Search the appropriate zone
            if zone is not None:  # hand, grave, banish
                for card in zone:
                    if card.name == card_name:
                        print(card.desc)
                        return
                print("Card not found in this zone.")

            else:  # field is spread across multiple lists
                all_field_cards = []
                all_field_cards.extend([z for z in self.em_zones if z is not None])
                all_field_cards.extend([z for z in self.fs_zone if z is not None])
                all_field_cards.extend([z[0] for z in self.m_zones if z[0] is not None])
                all_field_cards.extend([z for z in self.st_zones if z is not None])

                for card in all_field_cards:
                    if card.name == card_name:
                        print(card.desc)
                        return
                print("Card not found on the field.")

    def perform_action(self):
        action = input("Choose an action ((m)ove, mil(l), (d)raw, (o)verlay, (c)heck, (q)uit): ").strip().lower()
        #TODO: be sure to specify what zones on field cards are going to ie monster or s/t
        if action == "move" or action == "m":
            source = input("Enter source zone (e.g. hand, grave, deck): ").strip().lower()
            destination = input("Enter destination zone (e.g. hand, grave, m_zones, st_zones): ").strip().lower()
            card_name = input("Enter card name: ").strip()
            self.move_card(source, destination, card_name)

        elif action == "mill" or action == "l":
            self.mill()

        elif action == "draw" or action == "d":
            self.draw()

        elif action == "overlay" or action == "o":
            try:
                pos1 = int(input("Enter the index of the first monster zone: "))
                pos2 = int(input("Enter the index of the second monster zone to overlay: "))
                self.overlay(pos1, pos2)
            except ValueError:
                print("Invalid input. Please enter integer positions.")

        elif action == "check" or action == "c":
            zone = input("Which zone do you want to check? (hand, grave, field): ").strip().capitalize()
            self.check(zone)

        elif action == "quit" or action == "q":
            confirm = input("Are you sure? Yes(y) or No(n) ")
            if(confirm == "Yes" or confirm == "y"):
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
