import pygame
import test_hand



class GameUI:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 1200, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("TCG Prototype")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial',15)
        self.game = test_hand.TestHand()
        self.build_zones()
        self.start = False

    def build_zones(self):
        CARD_W, CARD_H = 80, 120
        GAP = 15

        center_x = self.WIDTH // 2

        # --- Monster Zones (5) ---
        self.monster_zones = []
        self.text = self.font.render('Main Zone', True, (255,255,255))
        m_y = self.HEIGHT // 2

        m_start_x = center_x - (CARD_W * 5 + GAP * 4) // 2
        for i in range(5):
            rect = pygame.Rect(
                m_start_x + i * (CARD_W + GAP),
                m_y,
                CARD_W,
                CARD_H
            )
            self.monster_zones.append(rect)

        # --- Spell / Trap Zones (5) ---
        self.spell_zones = []
        s_y = m_y + CARD_H + 20

        for i in range(5):
            rect = pygame.Rect(
                m_start_x + i * (CARD_W + GAP),
                s_y,
                CARD_W,
                CARD_H
            )
            self.spell_zones.append(rect)

# --- Extra Monster Zones (2) ---
        self.extra_zones = []
        em_y = m_y - CARD_H - 40

        EM_GAP = 100  # <-- fixed 100px gap between EM zones

        total_width = CARD_W * 2 + EM_GAP
        start_x = center_x - total_width // 2

        for i in range(2):
            rect = pygame.Rect(
                start_x + i * (CARD_W + EM_GAP),
                em_y,
                CARD_W,
                CARD_H
            )
            self.extra_zones.append(rect)


        # --- Field Spell Zone (1) ---
        self.field_spell_zone = pygame.Rect(
            m_start_x - 185 // 2,
            m_y,
            CARD_W,
            CARD_H
        )
        #self.field_spell_zone.move(-50,100)

        # --- Extra Deck ---
        self.e_deck_zone = pygame.Rect(
            m_start_x - 185 // 2,
            m_y + CARD_H + 20,
            CARD_W,
            CARD_H
        )

        # --- Graveyard ---
        self.grave_zone = pygame.Rect(
            center_x + (CARD_W * 5 + GAP * 6) // 2,
            m_y,
            CARD_W,
            CARD_H
        )

        # --- Main Deck ---
        self.deck_zone = pygame.Rect(
            center_x + (CARD_W * 5 + GAP * 6) // 2,
            m_y + CARD_H + 20,
            CARD_W,
            CARD_H
        )



        # --- Hand Area (visual only) ---
        self.hand_y = pygame.Rect(
            center_x,
            self.HEIGHT - CARD_H - 20,
            CARD_W * len(self.game.hand),
            CARD_H * len(self.game.hand)
        )
        self.game.start_game()

    def draw_field(self):
        self.screen.fill((30, 120, 30))  # green playmat
        text = self.font.render('EM ZONE',True,(255,255,255))

        # --- Extra Monster Zones ---
        for rect in self.extra_zones:
            pygame.draw.rect(self.screen, (255, 150, 150), rect, 2)
            self.screen.blit(text,rect)

        # --- Monster Zones ---
        text = self.font.render('MAIN ZONE',True,(255,255,255))
        for i, rect in enumerate(self.monster_zones):
            pygame.draw.rect(self.screen, (200, 200, 200), rect, 2)
            self.screen.blit(text,rect)

            card = self.game.m_zones[i][0]
            if card:
                self.draw_card(rect, card)

        # --- Spell / Trap Zones ---
        text = self.font.render('S/T ZONE',True,(255,255,255))
        for i, rect in enumerate(self.spell_zones):
            pygame.draw.rect(self.screen, (150, 150, 255), rect, 2)
            self.screen.blit(text,rect)

            card = self.game.st_zones[i]
            if card:
                self.draw_card(rect, card)

         # --- Field Spell Zone ---
        text = self.font.render('FS ZONE',True,(255,255,255))
        pygame.draw.rect(self.screen, (255, 255, 100), self.field_spell_zone, 2)
        self.screen.blit(text,self.field_spell_zone)

        if self.game.fs_zone[0]:
            self.draw_card(self.field_spell_zone, self.game.fs_zone[0])

        text = self.font.render('EXTRA  DECK',True,(255,255,255))
        pygame.draw.rect(self.screen, (255, 255, 100), self.e_deck_zone, 2)
        self.screen.blit(text,self.e_deck_zone)

        text = self.font.render('GY',True,(255,255,255))
        pygame.draw.rect(self.screen, (255, 255, 100), self.grave_zone, 2)
        self.screen.blit(text,self.grave_zone)

        text = self.font.render('MAIN  DECK',True,(255,255,255))
        pygame.draw.rect(self.screen, (255, 255, 100), self.deck_zone, 2)
        self.screen.blit(text,self.deck_zone)

        # --- Hand ---
        text = self.font.render('Hand',True,(255,255,255))
        pygame.draw.rect(self.screen, (255,255,100), self.hand_y, 2)
        self.draw_hand()

        pygame.display.flip()
    
    def draw_card(self, rect, card):
        pygame.draw.rect(self.screen, (245, 245, 245), rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)

        font = pygame.font.SysFont(None, 18)
        text = font.render(card.name, True, (0, 0, 0))
        self.screen.blit(
            text,
            text.get_rect(center=rect.center)
        )

    def draw_hand(self):

        hand = self.game.hand
        if not hand:
            return

        CARD_W, CARD_H = 80, 120
        GAP = 20

        total_width = len(hand) * (CARD_W + GAP) - GAP
        start_x = self.WIDTH // 2 - total_width // 2

        for i, card in enumerate(hand):
            rect = pygame.Rect(
                start_x + i * (CARD_W + GAP),
                self.HEIGHT - CARD_H - 20,
                CARD_W,
                CARD_H
            )
            self.draw_card(rect, card)


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if not self.start:
                    self.draw_field()
                    self.start = True
                self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    pygame.init()
    ui = GameUI()
    ui.run()
