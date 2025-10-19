import pygame, sys
import time
from random import choice, randint, sample
from os.path import join
from json import load, dump
from support import resource_path, save_path

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
ANIMATION_SPEED = 6

BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_GRAY = (41, 49, 51)
WHITE = (255, 255, 255)
GRAY = (104, 104, 104)

score_font = pygame.font.Font(resource_path('font','Pixeltype.ttf'), 40)
score_font_2 = pygame.font.Font(resource_path('font','Pixeltype.ttf'), 50)
mini_title_font = pygame.font.Font(resource_path('font','Pixeltype.ttf'), 70)
title_font = pygame.font.Font(resource_path('font','Pixeltype.ttf'), 90)
nickname_font = pygame.font.Font(resource_path('font','Pixeltype.ttf'), 130)
menu_score_font = pygame.font.Font(resource_path('font','Pixeltype.ttf'), 60)
progress_font = pygame.font.Font(resource_path('font', 'Pixeltype.ttf'), 35)

# menu
game_titles = ['Basket Eco', 'Pioggia di Rifiuti!', 'Infestazione di \n            Rifiuti', 'Giustizia Eco', 'Quiz Eco']
titles_pos = [(40, 270), (540, 270), (290, 370), (40, 470), (540, 470)]
menu_icons = [(10, -5), (20, 90), (40, 192)]

# basket rules
trash_map = ['Cestino azzuro: Carta','Cestino grigio: Indifferenziata','Cestino giallo: Plastica','Cestino marrone: Umido','Cestino verde: Vetro']

# quiz
questions = {
    'Qual e\' il principale gas responsabile \ndell\'effetto serra?': 2, 'Qual e\' l\'organo delle piante \nresponsabile della fotosintesi?': 1, 'Qual e\' il processo attraverso cui \ngli organismi decompongono \nla materia organica?': 2, 'Qual e\' una causa dell\'acidificazione \ndegli oceani?': 3, 'Qual e\' una fonte rinnovabile \ndi energia?': 2,
    'Qual e\' un esempio di \necosistema marino?': 2, 'Qual e\' un effetto \ndell\'inquinamento luminoso?': 1, 'Qual e\' un metodo per \nconservare la biodiversita\'?': 2, 'Qual e\' un esempio di energia \nnon rinnovabile?': 2, 'Qual e\' un esempio di inquinamento \ndell\'aria?': 0,
    'Qual e\' un fattore che contribuisce \nalla perdita di habitat?': 1, 'Qual e\' un effetto del surriscaldamento \nglobale sugli oceani?': 1, 'Qual e\' un metodo per ridurre \nl\'impronta ecologica?': 1, 'Qual e\' un esempio di \nspecie invasive?': 3, 'Qual e\' un beneficio \ndell\'agricoltura biologica?': 1,
    'Qual e\' una causa dell\'erosione \ndel suolo?': 0, 'Qual e\' un effetto dell\'inquinamento \ndei fiumi?': 2, 'Qual e\' un vantaggio dell\'energia \nsolare?': 2, 'Qual e\' un modo per ridurre \nla produzione di rifiuti?': 1, 'Qual e\' un impatto dell\'inquinamento \nidrico?': 2,
}

options = [
    ['Ossigeno', 'Azoto', 'Anidride Carbonica', 'Idrogeno'], ['Radici', 'Foglie', 'Fiori', 'Steli'], ['Fotosintesi', 'Fermentazione', 'Decomposizione', 'Respirazione'], ['Aumento del pH', 'Diminuzione \nemissioni CO2', 'Assorbimento \ndi CO2', 'Scarichi industriali'], ['Petrolio', 'Carbone', 'Vento', 'Gas naturale'],
    ['Deserto', 'Prateria', 'Barriera \ncorallina', 'Foresta \npluviale'], ['Riduzione dell\' \ninquinamento \ndell\'aria', 'Disturbo degli \nanimali notturni', 'Aumento della \nbiodiversita\'', 'Miglioramento della \nvista notturna umana'], ['Deforestazione', 'Urbanizzazione', 'Creazione \ndi aree protette', 'Estrazione \nmineraria intensiva'], ['Energia solare', ' Energia eolica', 'Petrolio', 'Biomassa'], ['Smog', 'Acidificazione \ndegli oceani', 'Inquinamento luminoso', 'Inquinamento acustico'],
    ['Conservazione \ndelle risorse', 'Urbanizzazione', 'Rimboschimento', 'Riduzione \ndell\'inquinamento'], ['Aumento della salinita\'', 'Aumento della T \ndell\'acqua', 'Diminuzione dell\'acidita\'', 'Riduzione del livello \ndegli oceani'], ['Aumentare il consumo \ndi risorse', 'Ridurre il consumo \ndi energia', 'Aumentare lo spreco \nalimentare', 'Aumentare l\'uso \ndi plastica monouso'], ['Piante locali', 'Animali migratori', 'Specie native', 'Cane di prateria'], ['Utilizzo intensivo \ndi pesticidi', 'Minore impatto \nambientale', 'Aumento dell\' \ninquinamento \ndel suolo', 'Riduzione della \nbiodiversita\''],
    ['Deforestazione', 'Afforestation', 'Ricerca di nuove specie', 'Riciclaggio'], ['Aumento della \nbiodiversita\' acquatica', 'Riduzione della \ntossicita\' dell\'acqua', 'Moria di pesci', 'Miglioramento della \nqualita\' dell\'acqua'], ['Produzione di emissioni \nnocive', 'Costi elevati \ndi installazione', 'Riduzione dell\' \ninquinamento \natmosferico', 'Dipendenza da \ncombustibili fossili'], ['Utilizzare piu\' imballaggi \nmonouso', 'Praticare il \ncompostaggio', 'Aumentare l\'uso \ndi plastica', 'Sprecare cibo'], ['Aumento della \nbiodiversita\' acquatica', 'Riduzione della \ntossicita\' dell\'acqua', 'Morte di organismi \nacquatici', 'Aumento della qualita\' \ndell\'acqua']
]

# achievements
objectives = ['Fai 75 canestri IN TUTTO!',
             'Raccogli 200 rifiuti IN TUTTO!',
             'Distruggi 15 rifiuti SENZA ERRRORI!',
             'Abbatti il nemico 5 VOLTE!',
             'Rispondi a TUTTE le domande correttamente!'
            ]

achievements_titles = ['Superstar del Basket ', 'Occhio di Falco ', 'Raccoglitore Folle ','Guidatore Provetto ', 'Ecologista Sapiente ']
achv_progress = ['Canestri fatti: ', 'Sapazzatura distrutta: ', 'Spazzatura raccolta: ', 'Vittorie: ', 'Risposte corrette: ']
game_reward = ['175', '150', '150', '200', '150']
achv_keys = ['baskets_made', 'hit_streak', 'trash_collected', 'victories', 'correct_answers']
achv_tresholds = {'baskets_made': [0, 30, 50], 'hit_streak': [0, 15, 20], 'trash_collected': [0, 75, 100], 'victories': [0, 2, 3], 'correct_answers': [0, 10, 20]}

# shop
skin_names = ['Julius', 'Kobe Bryant', 'Lebron James', 'Micheal Jordan', 'green car', 'red car', 'black car', 'blue car']
index_skin_conversion = {0: 'julius', 1: 'jordan', 2: 'kobe', 3: 'lebron'}
prices = [750, 750, 750, 350, 350, 350]

# stats
used_stats = {'Canestri fatti: ': 'baskets_made', 'Spazzatura raccolta: ': 'trash_collected', 
              'Spazzatura distrutta: ': 'trash_eliminated', 'Nemici sconfitti: ': 'victories', 
              'Test fatti: ': 'tests_done', 'Skin attuale: ': 'skin', 'Tempo giocato (s): ': 'time_played'}
