from settings import *
from support import *
from menu import Menu
from trash_rain import TrashRain
from trash_invasion import TrashInvasion
from basket_eco import EcoBasket
from eco_quiz import Quiz
from eco_justice import EcoJustice
from achievements import Achievements
from shop import Shop
from stats import Stats
from start import Introduction

class Game:
    def __init__(self):
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Call of Earth')
        self.clock = pygame.time.Clock()
        self.import_assets()
        self.import_data()
        
        self.stages = {
            'trash_rain': TrashRain,
            'trash_invasion': TrashInvasion,
            'eco_basket': EcoBasket,
            'eco_justice': EcoJustice,
            'menu': Menu,
            'quiz': Quiz,
            'achievements': Achievements,
            'shop': Shop,
            'stats': Stats,  
            'start': Introduction          
        }
    
        if not self.saved_data['name']: self.change_stage('start')
        else: self.change_stage('menu')
    
    def import_data(self):
        try:
            with open(os.path.join('saves', 'games_data.txt')) as save_file:
                self.saved_data = load(save_file)
        except:
            self.saved_data = {
            'minigame_1': 0,
            'minigame_2': 0,
            'minigame_3': 0,
            'minigame_4': 0,
            'minigame_5': 0,
            'baskets_made': 0,
            'hit_streak': 0,
            'trash_eliminated': 0,
            'trash_collected': 0,
            'victories': 0,
            'correct_answers': 0,
            'already_answered': [],
            'tests_done': 0,
            'coins': 0,
            'skin': 'julius',
            'name': '',
            'car_skin': 0,
            'time_played': 0
        }  
        
    def save_data(self):
        with open(os.path.join('saves', 'games_data.txt'), 'w') as save_file:
            dump(self.saved_data, save_file)
    
    def import_assets(self):
        self.assets = {
            'sky': import_image(os.path.join('images', 'livello', 'background', 'sky')),
            'ground': import_image(os.path.join('images', 'livello', 'background', 'ground')),
            'level_icons': import_folder(os.path.join('images', 'livello', 'icone')),
            'menu_icons': import_folder(os.path.join('images', 'menu', 'icone')),
            'player': import_sub_folders(os.path.join('images', 'livello', 'player', 'omini')),
            'cars': import_folder(os.path.join('images', 'livello', 'player', 'macchine')),
            'garbage_bag': import_image(os.path.join('images', 'livello', 'player', 'cestini', '0')),
            'background': import_image(os.path.join('images', 'menu', 'background')),
            'title': import_image(os.path.join('images', 'menu', 'titolo_menu')),
            'good_trash': import_folder(os.path.join('images', 'livello', 'rifiuti', 'buoni')),
            'bad_trash': import_folder(os.path.join('images', 'livello', 'rifiuti', 'cattivi')),
            'super_trash': import_image(os.path.join('images', 'livello', 'rifiuti', 'super', '0')),
            'trash_can': import_image(os.path.join('images', 'livello', 'player', 'cestino')),
            'trash_cans': import_folder(os.path.join('images', 'livello', 'cestini')),
            'stone': import_image(os.path.join('images', 'livello', 'ostacoli', '0')),
        }
        
        self.assets['sky'] = pygame.transform.rotozoom(self.assets['sky'], 0, 1.3)
        
        self.audio_files = {
            'completion': import_audio_folder(os.path.join('audio', 'completamento')),
            'shop': import_audio_folder(os.path.join('audio', 'negozio')),
            'player': import_audio_folder(os.path.join('audio', 'player')),
            'score': import_audio_folder(os.path.join('audio', 'punteggio')),
            'background': import_audio_folder(os.path.join('audio', 'sottofondo')),
            'menu': import_audio_folder(os.path.join('audio', 'menu'))
        }
        
        self.audio_files['score'][5].set_volume(0.2)
        self.audio_files['player'][0].set_volume(0.3)
        for audio in self.audio_files['background']: audio.set_volume(0.5)
        for audio in self.audio_files['shop']: audio.set_volume(0.2)
        
    def change_stage(self, target: str):
        self.current_stage = self.stages[target](self.assets, self.audio_files, self.change_stage, self.save_data, self.saved_data)
    
    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            
            self.display_surface.fill(BLACK)
            self.current_stage.run(dt)
            
            pygame.display.update()
    
    
if __name__ == '__main__':
    game = Game()
    game.run()    
