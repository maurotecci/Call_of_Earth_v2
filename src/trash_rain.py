from settings import *
from minigame import Minigame
from objects import Obstacle
from player import AnimatedPlayer

class TrashRain(Minigame):
    def __init__(self, assets: dict, audio_files: dict, change_stage: callable, save_data: callable, saved_data: dict):
        super().__init__(assets, audio_files, change_stage, self.reset_local_vars, save_data, saved_data, 'minigame_3')
        self.display_surface = pygame.display.get_surface()
        self.title = 'Elimina la spazzatura!'
        
        self.skin = saved_data['skin']
        self.player = AnimatedPlayer(self.all_sprites, (400, 440), assets['player'][self.skin])
        
        # game vars
        self.obstacle_prob = [1, 1, 1, 1, 1, 2]
        self.speed = 600
        
        # game graphics
        screen_shrink = pygame.surface.Surface((150, 700))
        self.game_assets.append((screen_shrink, (650, 0)))
        
        # game timers
        self.obstacle_timer = pygame.USEREVENT + 1
        self.obstacle_speed = pygame.USEREVENT + 2
        
    def reset_local_vars(self):
        pygame.time.set_timer(self.obstacle_timer, 750)
        pygame.time.set_timer(self.obstacle_speed, 10000)
        self.obstacle_prob = [1, 1, 1, 1, 1, 2]
        self.speed = 600
        
    def handle_timers(self, event):
        if event.type == self.obstacle_timer and self.passed_time > 1.5:
            obstacle_type = choice(self.obstacle_prob)
            pos_x = randint(180, 605)
            if obstacle_type == 1: 
                obstacle_image = choice(self.assets['bad_trash'])
                self.trash.append(Obstacle((self.all_sprites, self.good_trash), obstacle_image, (pos_x, 10), 'vertical', self.speed))
            else:
                obstacle_image = choice(self.assets['good_trash'])
                self.trash.append(Obstacle((self.all_sprites, self.bad_trash), obstacle_image, (pos_x, 10), 'vertical', self.speed))
            
        if event.type == self.obstacle_speed:
            if self.obstacle_prob.count(2) < 5:
                self.obstacle_prob.append(2)
            
            if self.trash[0].speed < 700:
                for sprite in self.trash:
                    sprite.speed += 100
    
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if not self.has_started: self.save_data()
                
                pygame.quit()
                sys.exit()
                
            if self.has_started: self.handle_timers(event)
        
    def run(self, dt: float):
        self.event_loop()
        if self.has_started: 
            self.draw(dt) 
            self.calculate_time()
            self.check_bad_collision()
            self.check_good_collision(save_data='trash_collected')
            self.score_eq = self.score // 2
            self.check_game_over(self.strikes, 2)
        else: self.menu_stage(self.title)
        