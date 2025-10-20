from settings import *
from minigame import Minigame
from player import Player
from objects import Obstacle, Bullet

class TrashInvasion(Minigame):
    def __init__(self, assets: dict, audio_files: dict, change_stage: callable, save_data: callable, saved_data: dict):
        super().__init__(assets, audio_files, change_stage, self.reset_local_vars, save_data, saved_data, 'minigame_2')
        self.player = Player(self.all_sprites, (400, 525), assets['garbage_bag'])
        self.title = 'Eliminate the trash!'
        
        # game vars
        self.speed = 500
        self.counter, self.max_counter = 0, 0
        
        # graphics
        screen_shrink = pygame.surface.Surface((150, 700))
        background = pygame.surface.Surface((500, 700))
        player_path = pygame.surface.Surface((500, 10))
        player_path.fill((254, 138, 24))
        background.fill((173, 216, 230))
        
        self.game_assets = [(screen_shrink, (650, 0)), (background, (150, 0)), 
                            (player_path, (150, 525))]
        
        # timers
        self.obstacle_timer = pygame.USEREVENT + 1
        
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if not self.has_started: self.save_data()
               
                pygame.quit()
                sys.exit()
                
            if self.has_started:
                if event.type == self.obstacle_timer:
                    image = choice(self.assets['bad_trash'])
                    pos_x = randint(180, 605)
                    obstacle = Obstacle((self.all_sprites, self.bad_trash), image, (pos_x, 10), 'vertical', self.speed)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and len(self.bullets.sprites()) <= 2:
                        Bullet((self.all_sprites, self.bullets), self.assets['trash_can'], (self.player.rect.center))
    
    def reset_local_vars(self):
        pygame.time.set_timer(self.obstacle_timer, 500)
        self.speed = 500
        self.counter, self.max_counter = 0, 0
        
    def check_good_collision(self):
        if pygame.sprite.groupcollide(self.bullets, self.bad_trash, True, True):
            self.score += 1
            self.score_eq = self.score
            self.counter += 1
            self.audio_files['score'][1].play()
            self.saved_data['trash_eliminated'] += 1
            self.rect_surfs[0] = (self.score_bg, score_font_2.render(f'Score: {self.score}', False, BLACK), self.score_rect)
            self.score_rect = self.rect_surfs[0][1].get_frect(topleft=(425, 50))
            self.score_bg.width = self.score_rect.width + 25
            
    def check_bad_collision(self):
        if super().check_bad_collision():
            self.max_counter = self.counter if self.counter > self.max_counter else self.max_counter
            self.saved_data['hit_streak'] = self.max_counter if self.max_counter > self.saved_data['hit_streak'] else self.saved_data['hit_streak']
            self.counter = 0
            
    def check_trash_over_line(self):
        for trash in self.bad_trash:
            if trash.rect.y >= 480:
                trash.kill()
                self.strikes += 1
                self.audio_files['score'][5].play()
                self.adjust_cross_graphic()
                self.max_counter = self.counter if self.counter > self.max_counter else self.max_counter
                self.saved_data['hit_streak'] = self.max_counter if self.max_counter > self.saved_data['hit_streak'] else self.saved_data['hit_streak']
                self.counter = 0
        
    def run(self, dt: float):
        self.event_loop()
        if self.has_started:
            self.draw(dt)
            self.calculate_time()
            self.check_good_collision()
            self.check_bad_collision()
            self.check_trash_over_line()
            self.check_game_over(self.strikes, 2)
        else: self.menu_stage(self.title)
        
    