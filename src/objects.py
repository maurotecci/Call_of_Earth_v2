from pygame import image as image
from settings import *

class Button:
    def __init__(self, text: str, width: int, height: int, pos: tuple[int, int], elevation: int, clickable: bool=True, score: int=None, type: int=None):
        # core attributes
        self.screen = pygame.display.get_surface()
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]
        self.text = text
        self.text_lines = 1
        self.score = score
        self.type = type
        self.clickable = clickable
        
        # top rect
        self.top_rect = pygame.FRect(pos, (width, height))
        self.top_color = '#475F77' 
        
        # bottom rect
        self.bottom_rect = pygame.FRect(pos, (width, elevation))
        self.bottom_color = '#354B5E'
        
        # outline rect
        self.outline_rect = pygame.FRect(pos, (width, elevation))
        self.outline_color = BLACK
        
        # text
        self.text_surf = score_font.render(text, False, BLACK)
        self.text_rect = self.text_surf.get_frect()
        self.score_surf = score_font.render(f'Best score: {score}', True, BLACK)
        self.score_rect = self.score_surf.get_frect()
        
        if '\n' in self.text:
            self.text_lines += 0.4
        
    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_surf = score_font.render(self.text, False, BLACK)
        
        if self.score != None:
            pygame.draw.rect(self.screen, self.outline_color, self.bottom_rect, width=3, border_radius=12)
            self.score_surf = score_font.render(f'Best score: {self.score}', True, BLACK)
            self.text_rect.center = (self.top_rect.centerx, self.top_rect.top + 30 * self.text_lines)
            self.score_rect.center = (self.top_rect.centerx, self.top_rect.top + 80)
        else:
            self.text_rect = self.text_surf.get_frect()
            self.text_rect.center = self.top_rect.center
            pygame.draw.rect(self.screen, self.bottom_color, self.bottom_rect, border_radius=12)
            pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=12)
        
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
        
        self.check_click()
        self.screen.blit(self.text_surf,self.text_rect)
        if self.score != None:
            self.screen.blit(self.score_surf, self.score_rect)
        
    def check_click(self):
        pressed = False
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos) and self.clickable:
            
            self.text_surf = score_font.render(self.text, False, '#FFFFFF')
            if self.score != None:
                self.score_surf = score_font.render(f'Best score: {self.score}', False, '#FFFFFF')
                pygame.draw.rect(self.screen, self.bottom_color, self.bottom_rect, border_radius=12)
                pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=12)
            
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
                pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed:
                    self.pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#475F77' 
            
        return pressed
    
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group, image: pygame.image, pos: tuple[int, int], dir: str, speed: int, type: int=None):
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.image = image
        self.rect = self.image.get_frect(center=pos)
        
        # bg surf
        self.bg_surf = pygame.surface.Surface((self.rect.width + 5, self.rect.height + 5))
        self.bg_surf.set_alpha(180)
        self.bg_surf.fill(BLACK)
        self.bg_rect = self.bg_surf.get_frect(center=(self.rect.centerx - 2, self.rect.centery - 2))
        
        # move attr
        self.speed = speed
        self.dir = dir
        self.type = type
        self.posx_interval = (self.rect.left, self.rect.right)
        
    def move(self, dt: float):
        if self.dir == 'vertical': 
            self.rect.y += self.speed * 1 * dt
            self.bg_rect.y += self.speed * 1 * dt
            
            if self.rect.y >= 525: self.kill()
        else:
            self.rect.x += self.speed * -1 * dt
            self.bg_rect.x += self.speed * -1 * dt
                
    def update(self, dt: float):
        self.move(dt)
        self.display_surface.blit(self.bg_surf, self.bg_rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group, image: pygame.image, pos: tuple[int, int]):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(center=pos)
        self.speed = 400
        self.dir = -1
        
    def update(self, dt: float):
        if self.rect.centery <= -40:
            self.kill()
        
        self.rect.y += self.speed * self.dir * dt
        
class Trash(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group, image: pygame.image, pos: tuple[int, int], type: int):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(topleft=pos)
        self.type = type
        
class Road(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group, pos: tuple[int, int]):
        super().__init__(groups)
        self.image = pygame.surface.Surface((80, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_frect(topleft=pos)
        self.speed  = 400
        self.dir = -1
        
    def update(self, dt: float):
        self.rect.x += self.speed * self.dir * dt
        
        if self.rect.right <= 0:
            self.rect.left = 800 
    