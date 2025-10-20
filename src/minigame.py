from settings import *

class Minigame:
    def __init__(self, assets: dict, audio_files: dict, change_stage: callable, reset_local_vars: callable, save_data: callable, saved_data: dict, game: str):
        self.display_surface = pygame.display.get_surface()
        self.saved_data = saved_data
        self.game = game
        self.audio_files = audio_files
        self.song = ''
        
        # global vars
        self.score = 0
        self.trash = []
        self.strikes = 0
        self.has_started = False
        self.checking_rules = False
        self.press_timer = None
        self.game_timer = None
        self.reset_local_vars = reset_local_vars
        self.change_stage = change_stage
        self.player = None
        self.save_data = save_data
        self.score_eq = 0
        self.songs = [0, 1, 2, 3]
        self.game_finished = False
        self.space_pressed_before = False 
        
        # graphics
        self.assets = assets
        self.cross = assets['level_icons'][0]
        self.game_assets = [(assets['sky'], (150, 0)), (assets['ground'], (150, 500))]
        
        # score graphic
        self.score_surf = score_font_2.render(f'Punteggio: {self.score}', False, (0, 0, 0))
        self.score_rect = self.score_surf.get_frect(topleft=(425, 50))
        self.score_bg = pygame.FRect((410, 35), (self.score_rect.width + 25, self.score_rect.height + 25))
        self.rect_surfs = [(self.score_bg, self.score_surf, self.score_rect)]
        
        # strike graphic
        self.small_cross = pygame.transform.scale(self.cross, (self.cross.get_width(), self.score_rect.height))
        self.strike_rect = self.small_cross.get_frect()
        self.strike_bg = pygame.FRect((160, 35), (self.strike_rect.width + 25, self.strike_rect.height + 25))
        self.strikes_surfs = []
        
        # base groups
        self.all_sprites = pygame.sprite.Group()
        self.good_trash = pygame.sprite.Group()
        self.bad_trash = pygame.sprite.Group()
        self.amazing_trash = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.trash_cans = pygame.sprite.Group()
        
        self.groups = [self.all_sprites, self.good_trash, self.bad_trash, self.amazing_trash, self.bullets, self.trash_cans]
        
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if not self.has_started: self.save_data()
        
                pygame.quit()
                sys.exit()
        
    def reset_global_vars(self):
        self.score = 0
        self.strikes = 0
        self.strikes_surfs.clear()
        
        if self.rect_surfs:
            self.rect_surfs[0] = (self.score_bg, score_font_2.render(f'Score: {self.score}', False, (0, 0, 0)), self.score_rect)
            self.score_rect = self.rect_surfs[0][1].get_frect(topleft=(425, 50))
            self.score_bg.width = self.score_rect.width + 25
            
        if self.player:
            self.player.rect.center = self.player.pos
        
        self.reset_local_vars()  
        
    def check_game_over(self, condition: int, max: int):
        if condition > max:
            for sprite in self.all_sprites:
                if sprite in self.bad_trash or\
                    sprite in self.good_trash:
                    self.all_sprites.remove(sprite)
                    sprite.kill()
                
            self.audio_files['background'][self.song].fadeout(750)
            if self.score > self.saved_data[self.game]:
                self.saved_data[self.game] = self.score 
                self.audio_files['score'][2].play()
                
            self.saved_data['coins'] += self.score_eq
            self.saved_data['time_played'] += self.passed_time
            self.has_started = False
            self.game_timer = None
            self.game_finished = True
            
    def check_bad_collision(self):
        if pygame.sprite.spritecollide(self.player, self.bad_trash, True):
            self.strikes_surfs.clear()
            self.audio_files['score'][5].play()
            self.strikes += 1
            self.adjust_cross_graphic()
            return True
            
    def adjust_cross_graphic(self):
        cross_space, border_space = 60, 25
        
        for i in range(self.strikes):
            self.strikes_surfs.append((self.small_cross, (175 + i * cross_space, 50)))
            border_space = 40 if i >= 1 else 25
            
        self.strike_bg.width = self.strike_rect.width * self.strikes + border_space
                
    def check_good_collision(self, save_data: str=None):
        if pygame.sprite.spritecollide(self.player, self.good_trash, True):
            self.score += 1
            self.audio_files['score'][0].play()
            self.rect_surfs[0] = (self.score_bg, score_font_2.render(f'Score: {self.score}', False, (0, 0, 0)), self.score_rect)
            self.score_rect = self.rect_surfs[0][1].get_frect(topleft=(425, 50))
            self.score_bg.width = self.score_rect.width + 25
            
            if save_data:
                self.saved_data[save_data] += 1
            
    def check_start_input(self, exit_rect):
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        curr_time_press = float((pygame.time.get_ticks() - self.press_timer) / 1000) if self.press_timer else 1 
        space_pressed_now = keys[pygame.K_SPACE]
        
        if keys[pygame.K_SPACE] and not self.game_finished:
            self.song = choice(self.songs)
            self.audio_files['background'][self.song].play(loops=-1)
            self.has_started = True
            self.game_timer = pygame.time.get_ticks()
            self.reset_global_vars()
            
        if self.space_pressed_before and not space_pressed_now:
            self.game_finished = False
            
        self.space_pressed_before = space_pressed_now
            
        if pygame.mouse.get_pressed()[0] and curr_time_press >= WAIT_TIME:
            if exit_rect.collidepoint(mouse_pos):
                if not self.checking_rules: 
                    for group in self.groups:
                        group.empty()
                        
                    self.save_data()
                    self.change_stage('menu')
                else: 
                    self.checking_rules = False
                    self.press_timer = pygame.time.get_ticks()
            
    def calculate_time(self):
        self.passed_time = int((pygame.time.get_ticks() - self.game_timer) / 1000)
            
    def menu_stage(self, title: str):
        self.display_surface.fill((173, 216, 230))
        
        # title graphic
        title_surf = title_font.render(title, False, (0, 0, 0))
        title_rect = title_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        
        exit_surf = self.cross
        exit_rect = exit_surf.get_frect(center=(750, 50))
        
        instruction_surf = score_font.render('Press space to start!', False, (0, 0, 0))
        instruction_rect = instruction_surf.get_frect(center=(400, 500))
        
        self.display_surface.blit(title_surf, title_rect)
        self.display_surface.blit(exit_surf, exit_rect)
        self.display_surface.blit(instruction_surf, instruction_rect)
        
        if self.score > 0:
            score_text = menu_score_font.render(f'Score: {self.score}', False, (0, 0, 0))
            score_rect = score_text.get_frect(center=(400, 100))
            self.display_surface.blit(score_text, score_rect)
            
        self.check_start_input(exit_rect)
    
    def draw(self, dt: float):
        for surf, pos in self.game_assets:
            self.display_surface.blit(surf, pos)
            
        for rect, surf, pos in self.rect_surfs:
            pygame.draw.rect(self.display_surface, (211, 211, 211), rect, border_radius=12)
            self.display_surface.blit(surf, pos)
            
        if self.strikes > 0:
            pygame.draw.rect(self.display_surface, (211, 211, 211), self.strike_bg, border_radius=12)
            for surf, pos in self.strikes_surfs:
                self.display_surface.blit(surf, pos)
            
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.display_surface)
        