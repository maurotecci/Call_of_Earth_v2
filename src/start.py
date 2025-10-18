from settings import *

class Introduction:
    def __init__(self, _assets: dict, audio_files: dict, change_stage: callable, _save_data: callable, saved_data: dict):
        self.display_surface = pygame.display.get_surface()
        self.change_stage = change_stage
        self.saved_data = saved_data
        self.audio_files = audio_files
        self.surfs = []
        self.audio_files['menu'][0].play(loops=-1)
        
        title = title_font.render("Qual e' il tuo nickname?", False, BLACK)
        title_rect =  title.get_frect(center=(400,150))
        self.surfs = [(title, title_rect), (None, None), (None, None)]
        
        self.cursor_x = 110
        self.active = False
        self.cursor_visible = True
        self.cursor_last_blink = pygame.time.get_ticks()
        self.cursor_blink_rate = 500
        
        self.input_rect = pygame.FRect((100, 300), (600, 100))
        
    def draw(self):
        for surf, pos in self.surfs:
            if surf: self.display_surface.blit(surf, pos)
        
        if self.active:
            if self.cursor_visible: pygame.draw.line(self.display_surface, BLACK, (self.cursor_x, 310),(self.cursor_x, 390), 5)
            self.current_time = pygame.time.get_ticks()
            if self.current_time - self.cursor_last_blink >= self.cursor_blink_rate:
                self.cursor_visible = not self.cursor_visible
                self.cursor_last_blink = self.current_time
                
        pygame.draw.rect(self.display_surface, BLACK, self.input_rect, 5)
        
    def adjust_texts(self):
        user_text = nickname_font.render(self.saved_data['name'], False, BLACK)
        user_rect = user_text.get_frect(topleft=(self.input_rect.x + 10, self.input_rect.y + 15))
        self.cursor_x = user_rect.right + 10
        
        max_char_text = score_font.render(f'Caratteri utilizzati: {len(self.saved_data['name'])}', False, BLACK)
        max_char_rect = max_char_text.get_frect(center=(400, 500))
        
        self.surfs[1] = (user_text, user_rect)
        self.surfs[2] = (max_char_text, max_char_rect)
        
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos): self.active = True
                else: self.active = False
                
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.saved_data['name'] = self.saved_data['name'][:-1]
                    else: 
                        if len(self.saved_data['name']) < 10:
                            self.saved_data['name'] += event.unicode
                            
                    self.adjust_texts()
                            
                    if event.key == pygame.K_RETURN: 
                        self.saved_data['name'] = self.saved_data['name'][:-1]
                        self.audio_files['menu'][0].fadeout(750)
                        self.change_stage('menu')
        
    def run(self, _dt: float):
        self.display_surface.fill(LIGHT_BLUE)
        self.event_loop()
        self.draw()