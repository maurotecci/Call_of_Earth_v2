from settings import *
from math import sqrt
from minigame import Minigame
from player import BasketPlayer
from objects import Obstacle, Trash

class EcoBasket(Minigame):
    def __init__(self, assets: dict, audio_files: dict, change_stage: callable, save_data: callable, saved_data: dict):
        super().__init__(assets, audio_files, change_stage, self.reset_local_vars, save_data, saved_data, 'minigame_1')
        self.title = "Score baskets!!"
        self.skin = saved_data['skin']
        self.player = BasketPlayer(self.all_sprites, (120, 450), audio_files, assets['player'][self.skin])
        self.old_score = self.score
        
        # game vars
        self.size_increase = 600
        self.starting_size = 100
        self.arc_rect_height = 500
        self.throw_speed = 600
        self.throwing = False
        self.arc_rect = pygame.FRect((self.player.rect.centerx + 20, self.player.rect.centery - self.arc_rect_height), (self.starting_size, self.arc_rect_height))
        self.start_throw_pos = self.arc_rect.left
        self.end_throw_pos = self.arc_rect.bottom / 2 - 30
        self.arc_bottom = self.arc_rect.right
        
        # timer surf
        self.timer_surf = score_font_2.render('0', False, BLACK)
        self.timer_rect = self.timer_surf.get_frect()
        self.timer_bg_rect = pygame.FRect((135, 35), (self.timer_rect.width + 25, self.timer_rect.height + 25))
        self.rect_surfs.append((self.timer_bg_rect, self.timer_surf, self.timer_rect))
                
        # graphics
        self.trash_map = self.assets['level_icons'][2]
        self.map_rect = self.trash_map.get_frect(topleft=(20, 25))
        self.game_assets.clear()
        self.game_assets = [(self.assets['sky'], (0, 0)), (self.assets['ground'], (0, 500))]
        
        # info graphics
        self.rules_rect = pygame.FRect((100,50), (600,500))
        self.tint_surf = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_surf.set_alpha(200)
        info_title = mini_title_font.render('Baskets', False, BLACK)
        info_title_rect = info_title.get_frect(center=(400, 100))
        self.info_surfs = [(self.trash_map, self.map_rect), (info_title, info_title_rect)]
        
        # trash_cans
        for i in range(5):
            Trash((self.all_sprites, self.trash_cans), assets['trash_cans'][i], (350 + 80 * i, 410), i)
        
    def menu_stage(self):
        mouse_pos = pygame.mouse.get_pos()
        
        super().menu_stage(self.title)
        self.display_surface.blit(self.trash_map, self.map_rect)
        
        if pygame.mouse.get_pressed()[0]:
            if self.map_rect.collidepoint(mouse_pos):
                self.checking_rules = True
                
        if self.checking_rules:      
            self.display_rules()
                
    def display_rules(self):
        self.display_surface.blit(self.tint_surf, (0, 0))
        pygame.draw.rect(self.display_surface, (173, 216, 230), self.rules_rect, border_radius=12)
        
        for index, rule in enumerate(trash_map):
            rule_text = score_font.render(rule, False, BLACK)
            self.info_surfs.append((rule_text, (150, ((self.rules_rect.width / 5 - 40) * index + 160))))
            pygame.draw.circle(self.display_surface, BLACK, (125,((self.rules_rect.width / 5 - 40) * index + 170)),5)
            
        for surf, pos in self.info_surfs:
            self.display_surface.blit(surf, pos)
                
    def handle_ball_trajectory(self, dt: float):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE] and not self.throwing:
            self.arc_rect.width += self.size_increase * dt
            self.arc_bottom_x = self.arc_rect.right - 30
            
            # draw throw trajectory arcs
            pygame.draw.arc(self.display_surface, (0, 128, 0), ((self.arc_rect.left, self.arc_rect.bottom / 2 - 30), 
                                                                (self.arc_rect.width - self.trash.rect.width / 2, self.arc_rect_height)), 0, 3.14 / 2, 3)
            pygame.draw.arc(self.display_surface, (0, 128, 0), ((self.arc_rect.left, self.arc_rect.bottom / 2 - 30), 
                                                                (self.arc_rect.width - self.trash.rect.width / 2, self.arc_rect_height)), 3.14 / 2, 3.14 * 7 / 8, 3)
            
            if self.arc_rect.width >= 650 or self.arc_rect.width < 100: self.size_increase *= -1
        
        if keys[pygame.K_UP] and keys[pygame.K_SPACE]:
            self.get_arc_equation()
            self.throwing = True
            
        self.arc_rect.width = self.starting_size if not keys[pygame.K_SPACE] else self.arc_rect.width
            
    def get_arc_equation(self):
        self.arc_x = (self.arc_rect.left + self.arc_rect.right) / 2
        self.arc_y = (self.arc_rect.bottom + self.arc_rect.bottom) / 2
        
        self.radius = sqrt((self.arc_rect.right - self.arc_rect.left)**2 + (self.arc_rect.bottom - self.arc_rect.bottom)**2) / 2
        
    def check_good_collision(self):
        for sprite in self.trash_cans:
            if sprite.rect.left + 10 <= self.arc_bottom_x <= sprite.rect.right - 10:
                if sprite.type == self.trash.type:
                    self.score += 1
                    self.audio_files['score'][1].play()
                    self.score_eq = self.score
                    self.saved_data['baskets_made'] += 1
                    self.rect_surfs[0] = (self.score_bg, score_font_2.render(f'Score: {self.score}', False, BLACK), self.score_rect)
                    self.score_rect = self.rect_surfs[0][1].get_frect(topleft=(425, 50))
                    self.score_bg.width = self.score_rect.width + 25
                
                
        if self.old_score == self.score: self.audio_files['score'][5].play()
        self.old_score = self.score
              
        self.bad_trash.empty()
        self.trash.kill()
        self.reset_local_vars()  
        
    def throw_trash(self, dt: float):
        try:
            self.trash.rect.center = self.trash.bg_rect.center =\
            (self.start_throw_pos - self.trash.rect.width, self.arc_y - sqrt(self.radius**2 - (self.start_throw_pos - self.arc_x)**2))
        except:
            self.check_good_collision()
        
        self.start_throw_pos += self.throw_speed * dt
        
    def update_timer_rect(self):
        color = BLACK
        
        if self.passed_time >= 20: color = (255, 255, 0)
        if self.passed_time >= 25: color = (255, 0, 0)
        
        self.timer_surf = score_font_2.render(str(self.passed_time), False, color)    
        self.timer_rect = self.timer_surf.get_frect(topleft=(150, 50))
        self.timer_bg_rect.width = self.timer_rect.width + 25
        
        self.rect_surfs[1] = (self.timer_bg_rect, self.timer_surf, self.timer_rect)
        
    def reset_local_vars(self):
        self.throwing = False
        self.start_throw_pos = self.arc_rect.left
        self.arc_rect.width = self.starting_size
        image = choice(self.assets['bad_trash'])
        self.trash = Obstacle((self.all_sprites, self.bad_trash), image, (self.start_throw_pos, 450), 'horizontal', 0, type=self.assets['bad_trash'].index(image))
    
    def run(self, dt: float):
        self.event_loop()
        if self.has_started:
            self.calculate_time() 
            self.update_timer_rect()
            self.draw(dt)
            self.handle_ball_trajectory(dt)
            self.check_game_over(self.passed_time, 29)
            if self.throwing: self.throw_trash(dt)
        else: self.menu_stage()
        