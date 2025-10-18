from pygame import image as image
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group, pos: tuple[int, int], image: pygame.image):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(center=(pos))
        self.pos = pos
        
        # movement attributes
        self.speed = 600
        self.dir = 1
            
    def move(self, dt: float):
        keys = pygame.key.get_pressed()
        
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left > 150:
            self.dir = -1
            
        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right <= WINDOW_WIDTH - 150:
            self.dir = 1
            
        else: self.dir = 0
            
        self.rect.x += self.dir * self.speed * dt
            
        return self.rect.center
    
    def update(self, dt: float):
        self.move(dt)
        
class AnimatedPlayer(Player):
    def __init__(self, groups: pygame.sprite.Group, pos: tuple[int, int], frames: list = None):
        super().__init__(groups, pos, frames[0])
        
        # animation attributes
        self.frames = [frames[1], frames[2]]
        self.idle = frames[0]
        self.jump = frames[3]
        self.player_index = 0
        
    def animate(self, dt: float):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.player_index += ANIMATION_SPEED * dt
            
            if self.player_index >= len(self.frames): self.player_index = 0
            self.image = self.frames[int(self.player_index)]
            
            if keys[pygame.K_a] or keys[pygame.K_LEFT]: self.image = pygame.transform.flip(self.image,True,False)
        else:
            self.image = self.idle
            
    def update(self, dt: float):
        self.animate(dt)
        self.move(dt)
        

class BasketPlayer(AnimatedPlayer):
    def __init__(self, groups: pygame.sprite.Group, pos: tuple[int, int], audio_files: dict, frames: list = None):
        super().__init__(groups, pos, frames)
        self.player_gravity = 0
        self.jump_height = -1000
        self.ground_x = 500
        self.audio_files = audio_files
        
    def move(self, keys: pygame.key):        
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.bottom == self.ground_x:
            self.player_gravity = self.jump_height
            self.audio_files['player'][0].play()
            
    def animate(self, keys: pygame.key):        
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.bottom <= self.ground_x:
            self.image = self.jump
            
        if self.rect.bottom and self.rect.bottom >= self.ground_x:
            self.image = self.idle
        
    def apply_gravity(self, dt):
        self.player_gravity += 7
        self.rect.y += self.player_gravity * dt
        
        if self.rect.bottom >= self.ground_x:
            self.rect.bottom = self.ground_x

    def update(self, dt: float):
        keys = pygame.key.get_pressed()
        self.move(keys)
        self.apply_gravity(dt)
        self.animate(keys)

    
class Car(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group, image: pygame.image, pos: tuple[int, int], type: str='player'):
        super().__init__(groups)    
        self.image = image
        self.rect = self.image.get_frect(center=pos)
        self.pos = pos
        self.lane_x_increase = 133
        self.lane = None
        self.max_pos = 150
        self.type = type
        
    def move(self, dt: float):
        keys = pygame.key.get_just_pressed()
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.rect.centery != 166:
                self.rect.centery -= self.lane_x_increase
            
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.rect.centery != 432:
                self.rect.centery += self.lane_x_increase
                
        self.rect.x += 200 * dt
        if self.rect.centerx > self.max_pos:
            self.rect.centerx = self.max_pos
                
    def change_random_lane(self):
        self.lane = choice([166, 299, 432])
        
        self.rect.centery = self.lane
            
    def update(self, dt: float):
        if self.type == 'player':
            self.move(dt)