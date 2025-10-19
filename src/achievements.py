from settings import *
from objects import Button

class Achievements:
    def __init__(self, assets: dict, audio_files: dict, change_stage: callable, save_data: callable, saved_data: dict):
        self.change_stage = change_stage
        self.saved_data = saved_data
        self.save_data = save_data
        self.audio_files = audio_files
        self.display_surface = pygame.display.get_surface()
        self.surfs = []
        self.achv_surfs, self.progress_surfs, self.buttons = [], [], []
        self.checking_objectives = False
        self.import_achv_data()
        self.audio_files['background'][5].play(loops=-1)
        self.press_timer = None
        
        # get achv tresholds
        self.curr_tresholds, self.curr_achv_level = [], []
        for achv in achv_tresholds:
            for index, treshold in enumerate(achv_tresholds[achv]):
                if treshold >= self.saved_data[achv]:
                    self.curr_tresholds.append(treshold)
                    self.curr_achv_level.append(index + 1)
                    break
                if index == 2: 
                    self.curr_achv_level.append(3)
                    self.curr_tresholds.append(treshold)
        
        # create surfs
        info_surf = assets['level_icons'][2]
        self.info_rect = info_surf.get_frect(topleft=(10, 25))
        self.exit_surf = assets['level_icons'][0]
        self.exit_rect = self.exit_surf.get_frect(center=(750, 50))
        
        title = title_font.render('Obietivi', False, BLACK)
        title_rect = title.get_frect(center=(400, 50))
        
        self.goal_title = title_font.render('Obiettivi', False, BLACK)
        self.goal_rect = self.goal_title.get_frect(center=(400, 100))
        self.tint_surf = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_surf.set_alpha(180)
        
        bg_achv_surf = pygame.surface.Surface((WINDOW_WIDTH, 500))
        bg_achv_surf.fill(DARK_GRAY)
        bg_achv_surf.set_alpha(100)
        bg_achv_rect = bg_achv_surf.get_frect(topleft=(0, 100))
        
        # rects
        self.bg_achv_border = pygame.FRect((0, 100), (WINDOW_WIDTH, 500))
        self.goals_rect = pygame.FRect((100, 50), (600, 500))
        
        self.surfs = [(bg_achv_surf, bg_achv_rect), (title, title_rect), (info_surf, self.info_rect)]
        
        bg_achv_divided = bg_achv_rect.height / 5
        for i in range(5):
            achv_title_text = achievements_titles[i] + 'I ' * self.curr_achv_level[i]
            achv_progress_text = achv_progress[i] + f'{self.saved_data[achv_keys[i]]} / {self.curr_tresholds[i]}'
            
            self.achv_surfs.append(menu_score_font.render(achv_title_text, False, BLACK))
            self.progress_surfs.append(progress_font.render(achv_progress_text, False, BLACK))

            self.surfs.append((self.achv_surfs[i], (20, 120 + bg_achv_divided * i)))
            self.surfs.append((self.progress_surfs[i], (20, 170 + bg_achv_divided * i)))
            
            button = Button(f'Ricompensa: {game_reward[i]}', 200, 80, (550, 115 + (i * 100)), 5)
            self.buttons.append(button)
            
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_data()
                self.save_achv_data()
                pygame.quit()
                sys.exit()
                
    def import_achv_data(self):
        try:
            with open(save_path('achievements_data.txt')) as redeem_file:
                self.redeemed_rewards = load(redeem_file)
        except:
            self.redeemed_rewards = {
                '0': False,
                '1': False,
                '2': False,
                '3': False,
                '4': False,
            }
            
    def save_achv_data(self):
        with open(save_path('achievements_data.txt'), 'w') as redeem_file:
            dump(self.redeemed_rewards, redeem_file)
                
    def draw(self):
        for surf, pos in self.surfs:
            self.display_surface.blit(surf, pos)
            
        pygame.draw.rect(self.display_surface, BLACK, self.bg_achv_border, 5, border_radius=12)
        for i in range(4):
            pygame.draw.line(self.display_surface, BLACK, (0, 200 + (100 * i)), (WINDOW_WIDTH, 200 + (100 * i)), 4)
        
        for button in self.buttons:
            button.draw()
            
        if self.checking_objectives:
            self.draw_achv_goals()
            
        self.display_surface.blit(self.exit_surf, self.exit_rect)
            
    def draw_achv_goals(self):
        self.display_surface.blit(self.tint_surf, (0, 0))
        pygame.draw.rect(self.display_surface, LIGHT_BLUE, self.goals_rect, border_radius=12)
        self.display_surface.blit(self.goal_title, self.goal_rect)
        
        for index, objective in enumerate(objectives):
                objective_text = score_font.render(objective,False,'black')
                self.display_surface.blit(objective_text,(150,((self.goals_rect.width / 5 - 40) * index + 160)))
                pygame.draw.circle(self.display_surface,'black',(125,((self.goals_rect.width / 5 - 40) * index + 170)),5)
            
    def mouse_input(self):
        mouse_pos = pygame.mouse.get_pos()
        curr_time_press = float((pygame.time.get_ticks() - self.press_timer) / 1000) if self.press_timer else 1 
        
        if pygame.mouse.get_pressed()[0] and curr_time_press >= 0.1:
            self.press_timer = pygame.time.get_ticks()
            if self.exit_rect.collidepoint(mouse_pos):
                if self.checking_objectives: self.checking_objectives = False
                else: 
                    self.audio_files['background'][5].fadeout(750)
                    self.change_stage('menu')
                    self.save_achv_data()
                
            if self.info_rect.collidepoint(mouse_pos): self.checking_objectives = True
            
            for index, button in enumerate(self.buttons):
                if button.check_click():
                    if self.saved_data[achv_keys[index]] >= achv_tresholds[achv_keys[index]][2]:
                        if not self.redeemed_rewards[str(index)]:
                            self.redeemed_rewards[str(index)] = True
                            self.saved_data['coins'] += int(game_reward[index])    
                            self.audio_files['completion'][0].play()        
    
    def run(self, _dt: float):
        self.display_surface.fill(LIGHT_BLUE)
        self.event_loop()
        self.mouse_input()
        self.draw()