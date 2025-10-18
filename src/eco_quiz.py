from settings import *
from objects import Button
from minigame import Minigame

class Quiz(Minigame):
    def __init__(self, assets: dict, audio_files: dict, change_stage: callable, save_data: callable, saved_data: dict):
        super().__init__(assets, audio_files, change_stage, self.reset_local_vars, save_data, saved_data, 'minigame_5')
        self.title = 'Quante ne sai?'
        
        # game vars
        self.curr_question = 0
        self.curr_index = 0
        self.question_surf = None
        self.question_rect = None
        self.songs = [4]
        
        # lists
        self.buttons = []
        self.questions_indexes = []
        self.questions = []
        self.game_assets.clear()
        
        # options buttons
        for i in range(4):
            pos = (50 + i * 400, 180) if i < 2 else (50 + (i - 2) * 400, 370)
            self.buttons.append(Button('', 300, 150, pos, 5, type=i))
            
    def change_question(self):
        self.rect_surfs.clear()
        self.check_game_over(self.curr_index, 4)
        
        if self.has_started:
            self.curr_question = self.questions[self.curr_index]
            self.curr_question_answer = questions[self.curr_question]
            
            for i, button in enumerate(self.buttons):
                button.text = options[self.questions_indexes[self.curr_index]][i]
            
            self.question_surf = score_font.render(self.curr_question, False, BLACK)
            self.question_rect = self.question_surf.get_frect(center=(400, 100))
            self.bg_rect = pygame.FRect((self.question_rect.left - 15, self.question_rect.top - 15), (self.question_rect.width + 25, self.question_rect.height + 25))
            self.rect_surfs = [(self.bg_rect, self.question_surf, self.question_rect)]
        
        
    def reset_local_vars(self):
        self.curr_index = 0
        self.questions_indexes.clear()
        self.questions_indexes = sample(range(20), 5)
        self.questions = [list(questions.keys())[index] for index in self.questions_indexes]
        self.saved_data['tests_done'] += 1

        self.change_question()
            
    def check_right_answer(self):
        mouse_pos = pygame.mouse.get_pos()
        curr_time_press = float((pygame.time.get_ticks() - self.press_timer) / 1000) if self.press_timer else 1 
            
        if pygame.mouse.get_pressed()[0] and curr_time_press >= 0.1:
            self.press_timer = pygame.time.get_ticks()
            for button in self.buttons:
                if button.check_click():
                    if button.type == self.curr_question_answer:
                        self.score += 1
                        self.audio_files['score'][0].play()
                        self.score_eq = self.score * 3
                        if self.curr_question not in self.saved_data['already_answered']:
                            self.saved_data['already_answered'].append(self.curr_question)
                            self.saved_data['correct_answers'] += len(self.saved_data['already_answered'])
                    else: self.audio_files['score'][5].play()
         
                    self.curr_index += 1
                        
                    self.change_question()
        
    def run(self, dt: float):
        self.event_loop()
        self.display_surface.fill(LIGHT_BLUE)
        if self.has_started:
            self.draw(dt)
            self.calculate_time()
            for button in self.buttons: button.draw()
            self.check_right_answer()
        else: self.menu_stage(self.title)
        