from settings import *
from objects import Button

class Menu:
    def __init__(self, assets: dict, audio_files: dict, choose_game: callable, save_data: callable, saved_data: dict):
        self.display_surface = pygame.display.get_surface()
        self.choose_game = choose_game
        self.audio_files = audio_files
        self.game_buttons = []
        self.icon_rects = []
        self.scores = [score for i, score in enumerate(saved_data.values()) if i < 5]
        self.save_data = save_data
        self.audio_files['menu'][0].play(loops=-1)
        
        self.games = {
            0: 'shop',
            1: 'stats',
            2: 'achievements',
            3: 'eco_basket',
            4: 'trash_invasion',
            5: 'trash_rain',
            6: 'eco_justice',
            7: 'quiz'
        }
        
        # graphics
        self.assets = assets
        coin_surf = assets['menu_icons'][3]
        coin_rect = coin_surf.get_frect(topleft=(730, 10))
        coin_text = score_font.render(str(saved_data['coins']), False, BLACK)
        self.coin_bg = pygame.FRect((coin_rect.left - coin_text.get_width() - 20, coin_rect.top + 5), 
                                    (coin_text.get_width() + 10, coin_text.get_height() + 10))
        
        self.game_surfs = [(assets['title'], (110, -100)), (coin_surf, coin_rect), 
                           (coin_text, (coin_rect.left - coin_text.get_width() - 15, coin_rect.top + 15))]
        self.create_surfs()
        
    def create_surfs(self):
        # buttons
        for index, title in enumerate(game_titles):
            button = Button(title, 220, 100, titles_pos[index], 5, score=self.scores[index])
            self.game_buttons.append(button)
            
        # icon rects
        for index, pos in enumerate(menu_icons):
            self.game_surfs.append((self.assets['menu_icons'][index], pos))
            self.icon_rects.append(self.assets['menu_icons'][index].get_frect(topleft=pos))
            
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_data()
                pygame.quit()
                sys.exit()
            
    def check_mouse_input(self):
        mouse_pos = pygame.mouse.get_pos()
        
        if pygame.mouse.get_pressed()[0]:
            for index, rect in enumerate(self.icon_rects):
                if rect.collidepoint(mouse_pos):
                    self.audio_files['menu'][0].fadeout(750)
                    self.choose_game(self.games[index])
                    
            for index, button in enumerate(self.game_buttons):
                if button.check_click():
                    self.audio_files['menu'][0].fadeout(750)
                    self.choose_game(self.games[index + 3])
            
    def draw(self):
        self.display_surface.blit(self.assets['background'], (0, 0))
        
        for i in range(3):
            pygame.draw.circle(self.display_surface, LIGHT_BLUE, self.icon_rects[i].center, self.icon_rects[1].width / 2)
            pygame.draw.circle(self.display_surface, (0, 0, 0), self.icon_rects[i].center, self.icon_rects[1].width / 2, 5)
        
        pygame.draw.rect(self.display_surface, LIGHT_BLUE, self.coin_bg, border_radius=12)
        
        for surf, pos in self.game_surfs:
            self.display_surface.blit(surf, pos)
            
        for button in self.game_buttons:
            button.draw()
        
    def run(self, _dt: float):
        self.event_loop()
        self.draw()
        self.check_mouse_input()