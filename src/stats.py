from settings import *
from objects import Button
from pathlib import Path

class Stats:
    def __init__(self, assets: dict, audio_files: dict, change_stage: callable, save_data: callable, saved_data: dict):
        self.assets = assets
        self.change_stage = change_stage
        self.saved_data = saved_data
        self.save_data = save_data
        self.display_surface = pygame.display.get_surface()
        self.surfs = []
        self.buttons = []
        self.stats_rect = pygame.FRect((200, 150), (400, 400))
        self.audio_files = audio_files
        self.audio_files['background'][5].play(loops=-1)   
        self.press_timer = None
        self.deleting = False
        self.deletion_step = 1     
        
        cross_surf = assets['level_icons'][0]
        self.cross_rect = cross_surf.get_frect(center=(750, 50))
        info_surf = assets['level_icons'][2]
        self.info_rect = info_surf.get_frect(center=(50, 50))
        title = title_font.render(f'{saved_data['name']}\'s statistics', False, BLACK)
        title_rect = title.get_frect(center=(400, 80))
        self.surfs = [(title, title_rect), (cross_surf, self.cross_rect), (info_surf, self.info_rect)]
        
        self.tint_surf = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_surf.set_alpha(180)
        self.info_text = menu_score_font.render("This is irreversible!", False, BLACK)
        self.delete_text = title_font.render('Delete account?', False, BLACK)
        self.delete_surfs = [(self.info_text, (220, 350)), (self.delete_text, (200, 120))]
        self.buttons.append(Button('Yes', 225, 100, (150, 220), 6))
        self.buttons.append(Button('No', 225, 100, (425, 220), 6))
        
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
        curr_time_press = float((pygame.time.get_ticks() - self.press_timer) / 1000) if self.press_timer else 1
        
        if pygame.mouse.get_pressed()[0] and curr_time_press >= WAIT_TIME:
            self.press_timer = pygame.time.get_ticks()
            if self.cross_rect.collidepoint(mouse_pos):
                if self.deleting: self.deleting = False
                else:
                    self.audio_files['background'][5].fadeout(750)
                    self.change_stage('menu')
            elif self.info_rect.collidepoint(mouse_pos):
                self.deleting = True
            
            if self.deleting:    
                for index, button in enumerate(self.buttons):
                    if button.check_click() :
                        if index == 0:
                            if self.deletion_step == 1:
                                self.info_text = menu_score_font.render("Are you sure?", False, BLACK)
                                self.delete_surfs[0] = (self.info_text, (270, 350))
                                self.deletion_step += 1
                            else:
                                folder = Path("saves")
                                for file in folder.glob("*.txt"):
                                    file.unlink()
                                pygame.quit()
                                sys.exit()
                        else:
                            self.deleting = False
                            self.deletion_step = 1    
                            self.info_text = menu_score_font.render("This is irreversible!", False, BLACK)
                            self.delete_surfs[0] = (self.info_text, (220, 350))                  
                            
    def draw_delete_win(self):
        self.display_surface.blit(self.tint_surf, (0, 0))
        bg_rect = pygame.FRect((100, 100), (600, 320))
        pygame.draw.rect(self.display_surface, LIGHT_BLUE, bg_rect, border_radius=12)
        
        for surf, rect in self.delete_surfs:
            self.display_surface.blit(surf, rect)
            
        for button in self.buttons:
            button.draw()
    
        
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
        if self.deleting: self.draw_delete_win()