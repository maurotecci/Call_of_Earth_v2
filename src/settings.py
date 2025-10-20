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

WAIT_TIME = 0.3

score_font = pygame.font.Font(resource_path('font','Pixeltype.ttf'), 40)
score_font_2 = pygame.font.Font(resource_path('font','Pixeltype.ttf'), 50)
mini_title_font = pygame.font.Font(resource_path('font','Pixeltype.ttf'), 70)
title_font = pygame.font.Font(resource_path('font','Pixeltype.ttf'), 90)
nickname_font = pygame.font.Font(resource_path('font','Pixeltype.ttf'), 130)
menu_score_font = pygame.font.Font(resource_path('font','Pixeltype.ttf'), 60)
progress_font = pygame.font.Font(resource_path('font', 'Pixeltype.ttf'), 35)

# menu
game_titles = ['Eco Basket', 'Trash Rain', '      Trash \nInfestation', 'Eco Justice', 'Eco Quiz']
titles_pos = [(40, 270), (540, 270), (290, 370), (40, 470), (540, 470)]
menu_icons = [(10, -5), (20, 90), (40, 192)]

# basket rules
trash_map = ['Blue bin: Paper','Gray bin: General waste','Yellow bin: Plastic','Brown bin: Organic waste','Green bin: Glass']

# quiz
questions = {
    'What is the main gas responsible \nfor the greenhouse effect?': 2, 'What is the plant organ \nresponsible for photosynthesis?': 1, 'What is the process through which \norganisms break down \norganic matter?': 2, 'What is a cause of the \nacidification of the oceans?': 3, 'Which of the following is a \nrenewable energy source?': 2,
    'Which of the following is an example \nof a marine ecosystem?': 2, 'What is one effect \nof light pollution?': 1, 'What is a method to \nconserve biodiversity?': 2, 'Which of the following is an example \nof non-renewable energy?': 2, 'Which of the following is an example \nof air pollution?': 0,
    'What is a factor contributing \nto habitat loss?': 1, 'What is one effect of global warming \non the oceans?': 1, 'What is one way to reduce \nthe ecological footprint?': 1, 'Which of the following is an example \nof invasive species?': 3, 'What is a benefit \nof organic farming?': 1,
    'What is a cause of soil erosion?': 0, 'What is an effect of \nriver pollution?': 2, 'What is an advantage of \nsolar energy?': 2, 'What is one way to reduce \nwaste production?': 1, 'What is an impact of \nwater pollution?': 2,
}

options = [
    ['Oxygen', 'Nitrogen', 'Carbon Dioxide', 'Hydrogen'], ['Roots', 'Leaves', 'Flowers', 'Stems'], ['Photosynthesis', 'Fermentation', 'Decomposition', 'Respiration'], ['Increase in pH', 'Decrease in \nCO2 emissions', 'Absorption \nof CO2', 'Industrial discharges'], ['Oil', 'Coal', 'Wind', 'Natural Gas'],
    ['Desert', 'Grassland', 'Coral \nreef', 'Rainforest'], ['Reduction of \nair pollution', 'Disturbance of \nnocturnal animals', 'Increase in \nbiodiversity', 'Improvement of \nhuman night vision'], ['Deforestation', 'Urbanization', 'Creation \nof protected areas', 'Intensive \nmining'], ['Solar energy', 'Wind energy', 'Oil', 'Biomass'], ['Smog', 'Ocean \nacidification', 'Light pollution', 'Noise pollution'],
    ['Conservation \nof resources', 'Urbanization', 'Reforestation', 'Reduction \nof pollution'], ['Increase in \nwater salinity', 'Increase in \nwater temperature', 'Decrease in \nacidity', 'Reduction of sea \nlevels'], ['Increase resource \nconsumption', 'Reduce energy \nconsumption', 'Increase food \nwaste', 'Increase use of \nsingle-use plastic'], ['Local plants', 'Migratory animals', 'Native species', 'Prairie dog'], ['Intensive use \nof pesticides', 'Lower \nenvironmental impact', 'Increase in \nsoil pollution', 'Reduction of \nbiodiversity'],
    ['Deforestation', 'Afforestation', 'Search for new species', 'Recycling'], ['Increase in aquatic \nbiodiversity', 'Reduction in water \ntoxicity', 'Fish die-off', 'Improvement in \nwater quality'], ['Production of harmful \nemissions', 'High installation \ncosts', 'Reduction of \natmospheric pollution', 'Dependence on \nfossil fuels'], ['Use more single-use \npackaging', 'Do \ncomposting', 'Increase plastic \nuse', 'Waste food'], ['Increase in aquatic \nbiodiversity', 'Reduction in water \ntoxicity', 'Death of aquatic \norganisms', 'Increase in water \nquality']
]

# achievements
objectives = ['Score 75 baskets IN TOTAL!',
             'Collect 200 pieces of trash IN TOTAL!',
             'Kill 15 pieces of trash WITHOUT MISTAKES!',
             'Defeat the enemy 5 TIMES!',
             'Answer ALL questions correctly!'
            ]

achievements_titles = ['Basket Superstar ', 'Eagle Eye ', 'Crazy Collector ','Expert Driver ', 'Wise Ecologist ']
achv_progress = ['Baskets made: ', 'Trash destroyed: ', 'Trash collected: ', 'Victories: ', 'Correct answers: ']
game_reward = ['175', '150', '150', '200', '150']
achv_keys = ['baskets_made', 'hit_streak', 'trash_collected', 'victories', 'correct_answers']
achv_tresholds = {'baskets_made': [0, 30, 50], 'hit_streak': [0, 15, 20], 'trash_collected': [0, 75, 100], 'victories': [0, 2, 3], 'correct_answers': [0, 10, 20]}

# shop
skin_names = ['Julius', 'Kobe Bryant', 'Lebron James', 'Michael Jordan', 'green car', 'red car', 'black car', 'blue car']
index_skin_conversion = {0: 'julius', 1: 'jordan', 2: 'kobe', 3: 'lebron'}
prices = [750, 750, 750, 350, 350, 350]

# stats
used_stats = {'Baskets made: ': 'baskets_made', 'Trash collected: ': 'trash_collected', 
              'Trash destroyed: ': 'trash_eliminated', 'Enemies defeated: ': 'victories', 
              'Tests completed: ': 'tests_done', 'Current skin: ': 'skin', 'Time played (s): ': 'time_played'}
