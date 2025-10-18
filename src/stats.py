from settings import *

class Stats:
    def __init__(self, assets: dict, audio_files: dict, change_stage: callable, save_data: callable, saved_data: dict):
        self.assets = assets
        self.change_stage = change_stage
        self.saved_data = saved_data
        self.save_data = save_data
        self.display_surface = pygame.display.get_surface()
        self.surfs = []
        self.stats_rect = pygame.FRect((200, 150), (400, 400))
        self.audio_files = audio_files
        self.audio_files['background'][5].play(loops=-1)        
        
        cross_surf = assets['level_icons'][0]
        self.cross_rect = cross_surf.get_frect(center=(750, 50))
        title = title_font.render(f'Statistiche di {saved_data['name']}', False, BLACK)
        title_rect = title.get_frect(center=(400, 80))
        self.surfs = [(title, title_rect), (cross_surf, self.cross_rect)]
        
        for index, (desc, stat) in enumerate(used_stats.items()):
            text = score_font.render(desc + str(self.saved_data[stat]), False, BLACK)
            pos = (220, (self.stats_rect.height / 7) * index + 170)
            self.surfs.append((text, pos))
        
    def draw(self):
        for surf, pos in self.surfs:
            self.display_surface.blit(surf, pos)
            
        pygame.draw.rect(self.display_surface, BLACK, self.stats_rect, 5, border_radius=12)
        
    def mouse_input(self):
        mouse_pos = pygame.mouse.get_pos()
        
        if pygame.mouse.get_pressed()[0]:
            if self.cross_rect.collidepoint(mouse_pos):
                self.audio_files['background'][5].fadeout(750)
                self.change_stage('menu')
        
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_data()
                pygame.quit()
                sys.exit()
        
    def run(self, _dt: float):
        self.display_surface.fill(LIGHT_BLUE)
        self.event_loop()
        self.mouse_input()
        self.draw()