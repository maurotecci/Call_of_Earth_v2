from settings import *
from objects import Button

class Shop:
    def __init__(self, assets: dict, audio_files: dict, change_stage: callable, save_data: callable, saved_data: dict):
        self.assets = assets 
        self.change_stage = change_stage
        self.audio_files = audio_files
        self.save_data = save_data
        self.saved_data = saved_data
        self.display_surface = pygame.display.get_surface()
        self.import_data()
        self.audio_files['background'][5].play(loops=-1)
        self.press_timer = None
        
        # shop vars
        self.confirming = False
        self.chosen_skin = None
        self.not_enough = False
        
        # lists
        self.player_rects, self.skin_surfs, self.names_surfs = [], [], []     
        self.other_surfs = []
        self.buttons, self.buy_buttons = [], {}
        self.title = title_font.render('Negozio', False, BLACK)
        self.other_surfs.append((self.title, (300, 40)))
        
        # graphics
        self.tint_surf = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_surf.set_alpha(180)
        self.buttons.append(Button('Si', 225, 100, (150, 220), 6))
        self.buttons.append(Button('No', 225, 100, (425, 220), 6))
        self.confirm_text = title_font.render('Confermi?', False, BLACK)
        self.not_enough_text = menu_score_font.render('Non hai abbastanza monete!', False, BLACK)
        
        exit_surf = assets['level_icons'][0]
        self.exit_rect = exit_surf.get_frect(center=(750, 60))
        coin_surf = assets['menu_icons'][3]
        self.coin_rect = coin_surf.get_frect(topleft=((50, 40)))
        coin_text = score_font_2.render(str(saved_data['coins']), False, BLACK)
        self.other_surfs.append((coin_text, (self.coin_rect.right + 10, 55)))
        self.other_surfs.append((coin_surf, self.coin_rect))
        self.other_surfs.append((exit_surf, self.exit_rect))
        
        self.skins = [skin[0] for skin in assets['player'].values()]
        self.skins[1], self.skins[0] = self.skins[0], self.skins[1]
        self.cars = assets['cars']
        self.big_lock = assets['menu_icons'][4]
        self.small_lock = pygame.transform.scale(self.big_lock, (90, 100))
        
        rects_spacing = (WINDOW_WIDTH - (140 * 4)) // (4 + 1)
        for i in range(4):
            x_pos = rects_spacing + i * (140 + rects_spacing)
            self.player_rects.append(pygame.FRect((x_pos, 190), (140, 140)))
            self.skin_surfs.append((self.skins[i], (x_pos + 10, 190 + 10)))
            
            name_surf = score_font.render(skin_names[i], False, BLACK)
            name_rect = name_surf.get_frect(center=(self.player_rects[i].centerx, 170))
            self.names_surfs.append((name_surf, name_rect))
            
            if not self.shop_data[str(i)]:
                self.buy_buttons[str(i)] = pygame.FRect((x_pos, 340), (self.player_rects[i].width, 30))
        
        rects_spacing = (WINDOW_WIDTH - (100 * 4)) // (4 + 1)
        for i in range(4):
            x_pos = rects_spacing + i * (100 + rects_spacing)
            self.player_rects.append(pygame.FRect((x_pos, 450), (100, 100)))
            self.skin_surfs.append((self.cars[i], (x_pos + 10, 450 + 10)))
            
            name_surf = score_font.render(skin_names[i + 4], False, BLACK)
            name_rect = name_surf.get_frect(center=(self.player_rects[i  + 4].centerx, 430))
            self.names_surfs.append((name_surf, name_rect))
            
            if not self.shop_data[str(i + 4)]:
                self.buy_buttons[str(i + 4)] = pygame.FRect((x_pos, 555), (self.player_rects[i  + 4].width, 30))
        
    def import_data(self):
        try:
            with open(save_path('shop_data.txt')) as shop_file:
                self.shop_data = load(shop_file)
        except:
            self.shop_data = {
                '0': True,
                '1': False,
                '2': False,
                '3': False,
                '4': True,
                '5': False,
                '6': False,
                '7': False,
                'current_skin': '0',
                'current_car': '4'
            }
            
    def save_shop_data(self):
        with open(save_path('shop_data.txt'), 'w') as shop_file:
            dump(self.shop_data, shop_file)
               
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_shop_data()
                self.save_data()
                pygame.quit()
                sys.exit()
                
    def mouse_pressed(self):
        for index, button in enumerate(self.buttons):
            if button.check_click():
                if index == 0:
                    if int(self.chosen_skin) < 4: curr_skin = int(self.chosen_skin) - 1
                    else: curr_skin = int(self.chosen_skin) - 2
                    if self.saved_data['coins'] >= prices[curr_skin]:
                        self.saved_data['coins'] -= prices[curr_skin]
                        self.shop_data[self.chosen_skin] = True
                        self.skin_surfs[int(self.chosen_skin)][0].set_alpha(255)
                        self.confirming = False
                        self.audio_files['shop'][0].play()
                        coin_text = score_font_2.render(str(self.saved_data['coins']), False, BLACK)
                        self.other_surfs[1] = (coin_text, (self.coin_rect.right + 10, 55))
                    else:
                        self.not_enough = True
                        self.audio_files['shop'][1].play()
                else: 
                    self.confirming = self.not_enough = False
            
    def mouse_input(self):
        mouse_pos = pygame.mouse.get_pos()
        curr_time_press = float((pygame.time.get_ticks() - self.press_timer) / 1000) if self.press_timer else 1 
        
        if pygame.mouse.get_pressed()[0] and curr_time_press >= 0.1:
            self.press_timer = pygame.time.get_ticks()
            if self.confirming:
                self.mouse_pressed()
            else:
                for button in self.buy_buttons.values():
                    if button.collidepoint(mouse_pos):
                        self.chosen_skin = next((k for k, v in self.buy_buttons.items() if v == button), None)
                        self.confirming = True
                        
            for index, rect in enumerate(self.player_rects):
                if rect.collidepoint(mouse_pos) and self.shop_data[str(index)]:
                    if index < 4: 
                        self.shop_data['current_skin'] = str(index)
                        self.saved_data['skin'] = index_skin_conversion[index]
                    else: 
                        self.shop_data['current_car'] = str(index)
                        self.saved_data['car_skin'] = index - 4
                    
            if self.exit_rect.collidepoint(mouse_pos) and not self.confirming:
                self.audio_files['background'][5].fadeout(750)
                self.save_shop_data()
                self.change_stage('menu')
      
    def draw_confirm_screen(self):
        self.display_surface.blit(self.tint_surf, (0, 0))
        if int(self.chosen_skin) < 4: curr_skin = int(self.chosen_skin) - 1
        else: curr_skin = int(self.chosen_skin) - 2
        
        bg_rect = pygame.FRect((100, 100), (600, 320))
        pygame.draw.rect(self.display_surface, LIGHT_BLUE, bg_rect, border_radius=12)
        self.display_surface.blit(self.confirm_text, (270, 120))
        
        if self.not_enough: self.display_surface.blit(self.not_enough_text, (150, 350))
        else: 
            skin_cost = menu_score_font.render(f'Costo: {prices[curr_skin]}', False, BLACK)
            self.display_surface.blit(skin_cost, (300, 350))
        
        for button in self.buttons:
            button.draw()
                
    def draw(self):  
        pygame.draw.rect(self.display_surface, (182, 209, 212), (0, 120, WINDOW_WIDTH, 480))
              
        for index, (surf, pos) in enumerate(self.skin_surfs):
            name_rect = pygame.FRect((self.names_surfs[index][1].left - 5, self.names_surfs[index][1].top - 5), (self.names_surfs[index][1].width + 5, 30))
            pygame.draw.rect(self.display_surface, GRAY, name_rect, border_radius=12)
            pygame.draw.rect(self.display_surface, (57, 69, 110), self.player_rects[index], border_radius=12) 
            
            if str(index) == self.shop_data['current_skin'] or\
               str(index) == self.shop_data['current_car']:
                pygame.draw.rect(self.display_surface, (255, 255, 255), self.player_rects[index], 5, border_radius=12) 
            
            self.display_surface.blit(surf, pos) 
            self.display_surface.blit(self.names_surfs[index][0], self.names_surfs[index][1])
              
            if not self.shop_data[str(index)]:
                lock_graphic = self.big_lock if index < 4 else self.small_lock
                offset = 15 if index < 4 else 5
                surf.set_alpha(100)
                self.display_surface.blit(lock_graphic, (self.player_rects[index].left + offset, self.player_rects[index].top))
                
                pygame.draw.rect(self.display_surface, GRAY, self.buy_buttons[str(index)], border_radius=12)
                buy_text = score_font.render('Compra', False, BLACK)
                offset = 25 if index < 4 else 7
                self.display_surface.blit(buy_text, (self.buy_buttons[str(index)].left + offset, self.buy_buttons[str(index)].top + 5))
                
        pygame.draw.line(self.display_surface, WHITE, (0, 390), (WINDOW_WIDTH, 390), 5)
                
        for surf, pos in self.other_surfs:
            self.display_surface.blit(surf, pos)
            
        if self.confirming:
            self.draw_confirm_screen()        
        
    def run(self, _dt: float):
        self.display_surface.fill((19, 87, 94))
        self.event_loop()
        self.mouse_input()
        self.draw()
       