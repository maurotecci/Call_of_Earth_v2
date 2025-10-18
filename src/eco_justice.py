from settings import *
from minigame import Minigame
from player import Car
from objects import Obstacle, Road

class EcoJustice(Minigame):
    def __init__(self, assets: dict, audio_files: dict, change_stage: callable, save_data: callable, saved_data: dict):
        super().__init__(assets, audio_files, change_stage, self.reset_local_vars, save_data, saved_data, 'minigame_4')
        self.title = 'Elimina il nemico'
        
        game_surf = pygame.surface.Surface((800, 400))
        game_surf.fill(DARK_GRAY)
        self.tint_surf = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.alpha_value = 0
        self.tint_surf.set_alpha(self.alpha_value)
        self.game_assets = [(game_surf, (0, 100))]
        
        # game vars
        self.curr_max_pos = 150
        self.victory = False
        
        # road lines
        x, y = 0, 156
        for lane in range(3):
            for line in range(5):
                Road(self.all_sprites, (x, y))
                x += 180
            y += 133.5
            x = 0
            
        lane_divider = pygame.surface.Surface((800, 10))
        lane_divider.fill(WHITE)
        for i in range(4):
            self.game_assets.append((lane_divider, (0, 100 + (133 * i))))
            
        self.skin = saved_data['car_skin']
        self.player = Car(self.all_sprites, assets['cars'][self.skin], (150, 299))
        self.enemey = Car(self.all_sprites, assets['cars'][2], (700 ,299), type='enemy')
        
        # timers
        self.obstacle_frequency = 800
        self.obstacle_freq_timer = pygame.USEREVENT + 1
        self.obstacle_freq_difficulty = pygame.USEREVENT + 2
        
    def generate_trash(self):
        self.enemey.change_random_lane()
        
        if self.super_obs_timer >= self.super_obs_duration:
            self.super_obs_duration = randint(8, 12)
            self.super_obs_timer_start = pygame.time.get_ticks()
            group = self.amazing_trash
            asset = self.assets['super_trash']
        else: 
            if choice([1, 1, 1, 2]) == 1:
                asset = choice(self.assets['bad_trash'])
                group = self.good_trash
            else: 
                asset = self.assets['stone']
                group = self.bad_trash
            
        Obstacle((self.all_sprites, group), asset, (700, self.enemey.lane), 'horizontal', 400)
        
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if not self.has_started: self.save_data()
        
                pygame.quit()
                sys.exit()
                
            if self.has_started:
                if event.type == self.obstacle_freq_timer and self.passed_time > 0.75:
                    self.generate_trash()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.rect.x = -5
        
    def reset_local_vars(self):
        pygame.time.set_timer(self.obstacle_freq_timer, self.obstacle_frequency)
        pygame.time.set_timer(self.obstacle_freq_difficulty, 8000)
        self.super_obs_duration = randint(8, 12)
        self.super_obs_timer_start = pygame.time.get_ticks()
        self.curr_max_pos = 150
        self.player.max_pos = self.curr_max_pos
        
    def calculate_time(self):
        super().calculate_time()
        self.super_obs_timer = int((pygame.time.get_ticks() - self.super_obs_timer_start) / 1000) 
        
    def check_amazing_collision(self):
        if pygame.sprite.spritecollide(self.player, self.amazing_trash, True):
            self.curr_max_pos += 75
            self.audio_files['score'][3].play()
            self.player.max_pos = self.curr_max_pos
            
    def check_trash_out(self):
        for trash in self.good_trash:
            if trash.rect.centerx <= -140:
                self.strikes += 1
                trash.kill()
                self.adjust_cross_graphic()
                
    def check_game_over(self, dt: float):
        super().check_game_over(self.strikes, 2)
        
        if self.player.rect.right >= 540:
            self.audio_files['completion'][1].play()
            self.victory = True
        
        if self.victory:
            self.alpha_value += 200 * dt
            self.tint_surf.set_alpha(self.alpha_value)
            
            if self.alpha_value >= 255:
                self.saved_data['victories'] += 1
                self.saved_data['coins'] += 50
                self.has_started = False
        
    def run(self, dt: float):
        self.display_surface.fill(LIGHT_BLUE)
        self.event_loop()
        if self.has_started:
            self.calculate_time()
            self.draw(dt)
            self.display_surface.blit(self.tint_surf, (0, 0))
            self.check_game_over(dt)
            if not self.victory:
                self.check_good_collision()
                self.score_eq = self.score // 2
                self.check_bad_collision()
                self.check_amazing_collision()
                self.check_trash_out()
        else: self.menu_stage(self.title)