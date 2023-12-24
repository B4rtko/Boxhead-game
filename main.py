import os
import sys

import pygame
from pygame.locals import *

sys.path.append(".")

from src.game_elements.Arena import *
from src.game_elements.Bot import *
from src.game_elements.Gameplay import *
from src.game_elements.Shooter import *

from src.game_configs.Config_difficult_level import config_difficult_level_easy, config_difficult_level_medium, config_difficult_level_hard
from src.game_configs.Config_controls import ConfigControls
from src.game_configs.utils import load_yaml, save_yaml


main_clock = pygame.time.Clock()

path_media_elements = os.path.join("src", "media_elements")


class StartScreen:
    """
    Main menu screen instance
    """
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.mouse.set_visible(0)

        self._control_buttons = None
        self._map_layout = None
        self._difficulty_level = None
        self._muted = None
        self.get_last_config()

        self.dict_difficulty_config = dict()

        pygame.mixer.music.load(os.path.join(path_media_elements, "dzwieki", "background.mp3"))
        if not self.muted:
            pygame.mixer.music.play(-1)

        self.sound_select = pygame.mixer.Sound(os.path.join(path_media_elements, "dzwieki", "menu_select.wav"))

        self.myfont = pygame.font.SysFont('Comic Sans MS', 40)

        self.highlight_ind = 0
        self.buttons = ["graj", "opcje", "instrukcja", "wyniki", "o autorze", "zakoncz"]

        self.image_menu = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "menu_glowne.png"))
        self.image_index = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "wskaznik.png"))

        self.ind_position = {"graj": (520, 140), "opcje": (520, 275), "instrukcja": (520, 405),
                             "wyniki": (520, 535), "o autorze": (520, 665), "zakoncz": (520, 795)}

        self.move_pressed = False

        self.set_difficulty_config()

        self.main_menu()
    
    def __export_config_dict(self):
        controls = self.control_buttons
        config_dict = {
            "map": { 
                "layout": self.map_layout
            },
            "controls": {
                "góra": controls["góra"],
                "dół": controls["dół"],
                "lewo": controls["lewo"],
                "prawo": controls["prawo"],
                "strzał": controls["strzał"],
                "następna": controls["następna"],
                "poprzednia": controls["poprzednia"],
            },
            "difficulty_level": self.difficulty_level,
            "music": {
                "is_muted": self.muted
            },
        }
        return config_dict
    
    @property
    def map_layout(self):
        return self._map_layout
    
    @map_layout.setter
    def map_layout(self, value):
        if not value in range(1, 6):
            raise ValueError

        self._map_layout = value
    
    @property
    def control_buttons(self):
        return self._control_buttons
    
    @control_buttons.setter
    def control_buttons(self, value):
        self._control_buttons = value
    
    @property
    def difficulty_level(self):
        return self._difficulty_level
    
    @difficulty_level.setter
    def difficulty_level(self, value):
        if value not in ["łatwy", "średni", "trudny"]:
            raise ValueError
        self._difficulty_level = value
    
    @property
    def muted(self):
        return self._muted
    
    @muted.setter
    def muted(self, value):
        if type(value) != bool:
            raise ValueError
        self._muted = value

    def get_last_config(self):
        """
        function loads previous game configuration if such exists
        """
        try:
            config = load_yaml(os.path.join(path_media_elements, "ostatni_stan.yaml"))

            self.map_layout = config["map"]["layout"]
            self.control_buttons = ConfigControls(**config["controls"])
            self.difficulty_level = config["difficulty_level"]
            self.muted = config["music"]["is_muted"]

        except:
            self.map_layout = 1
            self.control_buttons = ConfigControls()
            self.difficulty_level = "średni"
            self.muted = False

    def set_difficulty_config(self):
        """
        function sets game aspects depending on chosen difficulty level
        """
        if self.difficulty_level == "łatwy":
            self.dict_difficulty_config = config_difficult_level_easy

        elif self.difficulty_level == "średni":
            self.dict_difficulty_config = config_difficult_level_medium

        elif self.difficulty_level == "trudny":
            self.dict_difficulty_config = config_difficult_level_hard

    def main_menu(self):
        """
        function with main loop
        """
        while True:
            click = False
            highlighted = self.buttons[self.highlight_ind]

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key in [K_UP, K_w, K_DOWN, K_s] and (not self.move_pressed) and (not self.muted):
                    self.sound_select.play()
                    self.move_pressed = True
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        save_yaml(os.path.join(path_media_elements, "ostatni_stan.yaml"), self.__export_config_dict())
                        pygame.quit()
                        sys.exit()
                    if event.key == K_m and not self.muted:
                        self.muted = True
                        pygame.mixer.music.stop()
                    elif event.key == K_m and self.muted:
                        self.muted = False
                        pygame.mixer.music.play(-1)
                    if event.key in [K_RETURN, K_SPACE]:
                        click = True
                    if event.key in [K_UP, K_w]:
                        self.move_pressed = False
                        if self.highlight_ind > 0:
                            self.highlight_ind -= 1
                        else:
                            self.highlight_ind = len(self.buttons)-1
                    if event.key in [K_DOWN, K_s]:
                        self.move_pressed = False
                        if self.highlight_ind < len(self.buttons)-1:
                            self.highlight_ind += 1
                        else:
                            self.highlight_ind = 0

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.image_menu, self.image_menu.get_rect())
            self.screen.blit(self.image_index, self.ind_position[self.buttons[self.highlight_ind]])

            if highlighted == "graj" and click:
                Game(self)
            elif highlighted == "opcje" and click:
                OptionScreen(self)
            elif highlighted == "instrukcja" and click:
                HelpScreen(self)
            elif highlighted == "wyniki" and click:
                HighScoreScreen(self)
            elif highlighted == "o autorze" and click:
                CreditsScreen(self)
            elif highlighted == "zakoncz" and click:
                save_yaml(os.path.join(path_media_elements, "ostatni_stan.yaml"), self.__export_config_dict())
                pygame.quit()
                sys.exit()

            pygame.display.flip()
            main_clock.tick(30)


class OptionScreen:
    """
    Option screen instance
    """
    def __init__(self, menu):
        pygame.init()

        self.menu = menu

        self.screen = menu.screen
        pygame.mouse.set_visible(0)

        self.sound_select = pygame.mixer.Sound(os.path.join(path_media_elements, "dzwieki", "menu_select.wav"))

        self.highlight_ind = 0
        self.buttons = ["mapa", "sterowanie", "trudność", "powrót"]

        self.image_menu = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "menu_opcje.png"))
        self.image_index = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "wskaznik.png"))

        self.ind_position = {"mapa": (520, 275), "sterowanie": (520, 405),
                             "trudność": (520, 535), "powrót": (520, 665)}

        self.move_pressed = False
        self.muted = self.menu.muted

        self.loop = True
        self.option_menu()

    def option_menu(self):
        """
        function with main loop
        """
        while self.loop:
            click = False
            highlighted = self.buttons[self.highlight_ind]

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key in [K_UP, K_w, K_DOWN, K_s] and (not self.move_pressed) and (not self.muted):
                    self.sound_select.play()
                    self.move_pressed = True
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        self.loop = False
                    if event.key == K_m and not self.muted:
                        self.muted = True
                        self.menu.muted = True
                        pygame.mixer.music.stop()
                    elif event.key == K_m and self.muted:
                        self.muted = False
                        self.menu.muted = False
                        pygame.mixer.music.play(-1)
                    if event.key in [K_RETURN, K_SPACE]:
                        click = True
                    if event.key in [K_UP, K_w]:
                        self.move_pressed = False
                        if self.highlight_ind > 0:
                            self.highlight_ind -= 1
                        else:
                            self.highlight_ind = len(self.buttons)-1
                    if event.key in [K_DOWN, K_s]:
                        self.move_pressed = False
                        if self.highlight_ind < len(self.buttons)-1:
                            self.highlight_ind += 1
                        else:
                            self.highlight_ind = 0

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.image_menu, self.image_menu.get_rect())
            self.screen.blit(self.image_index, self.ind_position[self.buttons[self.highlight_ind]])

            if highlighted == "mapa" and click:
                OptionMapScreen(self)
            elif highlighted == "sterowanie" and click:
                OptionControlScreen(self)
            elif highlighted == "trudność" and click:
                OptionDifficultyScreen(self)
            elif highlighted == "powrót" and click:
                self.loop = False

            pygame.display.flip()
            main_clock.tick(30)


class OptionMapScreen:
    """
    Map choosing screen instance
    """
    def __init__(self, option):
        pygame.init()

        self.option = option

        self.screen = option.screen
        pygame.mouse.set_visible(0)

        self.sound_select = pygame.mixer.Sound(os.path.join(path_media_elements, "dzwieki", "menu_select.wav"))

        self.image_menu = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "menu_opcje_zblakly.png"))
        self.image_map_1 = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "mapy", "menu_opcje_mapa_1.png"))
        self.image_map_2 = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "mapy", "menu_opcje_mapa_2.png"))
        self.image_map_3 = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "mapy", "menu_opcje_mapa_3.png"))
        self.image_map_4 = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "mapy", "menu_opcje_mapa_4.png"))
        self.image_map_5 = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "mapy", "menu_opcje_mapa_5.png"))

        self.highlight_ind = self.option.menu.map_layout
        self.image_map_list = [None, self.image_map_1, self.image_map_2, self.image_map_3, self.image_map_4, self.image_map_5]

        self.move_pressed = False
        self.muted = self.option.menu.muted

        self.loop = True
        self.option_menu()

    def option_menu(self):
        """
        function with main loop
        """
        while self.loop:
            click = False
            highlighted = self.image_map_list[self.highlight_ind]

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key in [K_UP, K_w, K_DOWN, K_s, K_LEFT, K_a, K_RIGHT, K_d] and (not self.move_pressed) and (not self.muted):
                    self.sound_select.play()
                    self.move_pressed = True
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        self.loop = False
                    if event.key == K_m and not self.muted:
                        self.muted = True
                        self.option.muted = True
                        self.option.menu.muted = True
                        pygame.mixer.music.stop()
                    elif event.key == K_m and self.muted:
                        self.muted = False
                        self.option.muted = False
                        self.option.menu.muted = False
                        pygame.mixer.music.play(-1)
                    if event.key in [K_RETURN, K_SPACE]:
                        click = True
                    if event.key in [K_UP, K_LEFT, K_w, K_a]:
                        self.move_pressed = False
                        if self.highlight_ind > 1:
                            self.highlight_ind -= 1
                        else:
                            self.highlight_ind = len(self.image_map_list)-1
                    if event.key in [K_DOWN, K_RIGHT, K_s, K_d]:
                        self.move_pressed = False
                        if self.highlight_ind < len(self.image_map_list)-1:
                            self.highlight_ind += 1
                        else:
                            self.highlight_ind = 1

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.image_menu, self.image_menu.get_rect())
            self.screen.blit(highlighted, (600, 0))

            if self.highlight_ind == 1 and click:
                self.option.menu.map_layout = 1
                self.loop = False
            if self.highlight_ind == 2 and click:
                self.option.menu.map_layout = 2
                self.loop = False
            if self.highlight_ind == 3 and click:
                self.option.menu.map_layout = 3
                self.loop = False
            if self.highlight_ind == 4 and click:
                self.option.menu.map_layout = 4
                self.loop = False
            if self.highlight_ind == 5 and click:
                self.option.menu.map_layout = 5
                self.loop = False

            pygame.display.flip()
            main_clock.tick(30)


class OptionControlScreen:
    """
    Control setting screen instance
    """
    def __init__(self, option):
        pygame.init()

        self.option = option

        self.screen = option.screen
        pygame.mouse.set_visible(0)

        self.sound_select = pygame.mixer.Sound(os.path.join(path_media_elements, "dzwieki", "menu_select.wav"))

        self.highlight_ind = 0
        self.buttons = ["góra", "dół", "lewo", "prawo", "strzał", "następna", "poprzednia"]

        self.image_menu = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "menu_opcje_zblakly.png"))
        self.image_control = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "menu_opcje_sterowanie.png"))
        self.image_index = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "wskaznik.png"))

        self.ind_position = {"góra": (1303, 79), "dół": (1303, 208), "lewo": (1303, 338), "prawo": (1303, 468),
                             "strzał": (1303, 598), "następna": (1303, 728), "poprzednia": (1303, 858)}

        self.move_pressed = False
        self.muted = self.option.menu.muted

        self.loop = True
        self.option_menu()

    def option_menu(self):
        """
        function with main loop
        """
        while self.loop:
            click = False
            highlighted = self.buttons[self.highlight_ind]

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key in [K_UP, K_w, K_DOWN, K_s] and (not self.move_pressed) and (not self.muted):
                    self.sound_select.play()
                    self.move_pressed = True
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        self.loop = False
                    if event.key == K_m and not self.muted:
                        self.muted = True
                        self.option.muted = True
                        self.option.menu.muted = True
                        pygame.mixer.music.stop()
                    elif event.key == K_m and self.muted:
                        self.muted = False
                        self.option.muted = False
                        self.option.menu.muted = False
                        pygame.mixer.music.play(-1)
                    if event.key in [K_RETURN, K_SPACE]:
                        click = True
                    if event.key in [K_UP, K_w]:
                        self.move_pressed = False
                        if self.highlight_ind > 0:
                            self.highlight_ind -= 1
                        else:
                            self.highlight_ind = len(self.buttons)-1
                    if event.key in [K_DOWN, K_s]:
                        self.move_pressed = False
                        if self.highlight_ind < len(self.buttons)-1:
                            self.highlight_ind += 1
                        else:
                            self.highlight_ind = 0

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.image_menu, self.image_menu.get_rect())
            self.screen.blit(self.image_control, (700,0))
            self.screen.blit(self.image_index, self.ind_position[self.buttons[self.highlight_ind]])

            button_up_surface = self.option.menu.myfont.render(f"{pygame.key.name(self.option.menu.control_buttons['góra'])}", False, (255, 255, 255))
            button_down_surface = self.option.menu.myfont.render(f"{pygame.key.name(self.option.menu.control_buttons['dół'])}", False, (255, 255, 255))
            button_left_surface = self.option.menu.myfont.render(f"{pygame.key.name(self.option.menu.control_buttons['lewo'])}", False, (255, 255, 255))
            button_right_surface = self.option.menu.myfont.render(f"{pygame.key.name(self.option.menu.control_buttons['prawo'])}", False, (255, 255, 255))
            button_shot_surface = self.option.menu.myfont.render(f"{pygame.key.name(self.option.menu.control_buttons['strzał'])}", False, (255, 255, 255))
            button_next_gun_surface = self.option.menu.myfont.render(f"{pygame.key.name(self.option.menu.control_buttons['następna'])}", False, (255, 255, 255))
            button_previous_gun_surface = self.option.menu.myfont.render(f"{pygame.key.name(self.option.menu.control_buttons['poprzednia'])}", False, (255, 255, 255))
            self.screen.blit(button_up_surface, (1600, 115))
            self.screen.blit(button_down_surface, (1600, 245))
            self.screen.blit(button_left_surface, (1600, 375))
            self.screen.blit(button_right_surface, (1600, 505))
            self.screen.blit(button_shot_surface, (1600, 635))
            self.screen.blit(button_next_gun_surface, (1600, 765))
            self.screen.blit(button_previous_gun_surface, (1600, 895))

            if highlighted == "góra" and click:
                    self.wait_loop = True
                    while self.wait_loop:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYUP:
                                if event.key == K_ESCAPE:
                                    self.wait_loop = False
                                elif event.key not in [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0, K_p, K_m]:
                                    self.option.menu.control_buttons["góra"] = event.key
                                    self.wait_loop = False
            elif highlighted == "dół" and click:
                    self.wait_loop = True
                    while self.wait_loop:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYUP:
                                if event.key == K_ESCAPE:
                                    self.wait_loop = False
                                elif event.key not in [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0, K_p, K_m]:
                                    self.option.menu.control_buttons["dół"] = event.key
                                    self.wait_loop = False
            elif highlighted == "lewo" and click:
                self.wait_loop = True
                while self.wait_loop:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYUP:
                            if event.key == K_ESCAPE:
                                self.wait_loop = False
                            elif event.key not in [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0, K_p, K_m]:
                                self.option.menu.control_buttons["lewo"] = event.key
                                self.wait_loop = False
            elif highlighted == "prawo" and click:
                self.wait_loop = True
                while self.wait_loop:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYUP:
                            if event.key == K_ESCAPE:
                                self.wait_loop = False
                            elif event.key not in [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0, K_p, K_m]:
                                self.option.menu.control_buttons["prawo"] = event.key
                                self.wait_loop = False
            elif highlighted == "strzał" and click:
                self.wait_loop = True
                while self.wait_loop:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYUP:
                            if event.key == K_ESCAPE:
                                self.wait_loop = False
                            elif event.key not in [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0, K_p, K_m]:
                                self.option.menu.control_buttons["strzał"] = event.key
                                self.wait_loop = False
            elif highlighted == "następna" and click:
                self.wait_loop = True
                while self.wait_loop:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYUP:
                            if event.key == K_ESCAPE:
                                self.wait_loop = False
                            elif event.key not in [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0, K_p, K_m]:
                                self.option.menu.control_buttons["następna"] = event.key
                                self.wait_loop = False
            elif highlighted == "poprzednia" and click:
                self.wait_loop = True
                while self.wait_loop:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYUP:
                            if event.key == K_ESCAPE:
                                self.wait_loop = False
                            elif event.key not in [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0, K_p, K_m]:
                                self.option.menu.control_buttons["poprzednia"] = event.key
                                self.wait_loop = False

            pygame.display.flip()
            main_clock.tick(30)


class OptionDifficultyScreen:
    """
    Difficulty setting screen instance
    """
    def __init__(self, option):
        pygame.init()

        self.option = option

        self.screen = option.screen
        pygame.mouse.set_visible(0)

        self.sound_select = pygame.mixer.Sound(os.path.join(path_media_elements, "dzwieki", "menu_select.wav"))

        self.buttons = ["łatwy", "średni", "trudny"]
        self.highlight_ind = self.buttons.index(self.option.menu.difficulty_level)

        self.image_menu = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "menu_opcje_zblakly.png"))
        self.image_difficulty = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "menu_opcje_poziom_trudności.png"))
        self.image_index = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "wskaznik.png"))

        self.ind_position = {"łatwy": (1303, 338), "średni": (1303, 468), "trudny": (1303, 598)}

        self.move_pressed = False
        self.muted = self.option.menu.muted

        self.loop = True
        self.option_menu()

    def option_menu(self):
        """
        function with main loop
        """
        while self.loop:
            click = False
            highlighted = self.buttons[self.highlight_ind]

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key in [K_UP, K_w, K_DOWN, K_s] and (not self.move_pressed) and (not self.muted):
                    self.sound_select.play()
                    self.move_pressed = True
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        self.loop = False
                    if event.key == K_m and not self.muted:
                        self.muted = True
                        self.option.muted = True
                        self.option.menu.muted = True
                        pygame.mixer.music.stop()
                    elif event.key == K_m and self.muted:
                        self.muted = False
                        self.option.muted = False
                        self.option.menu.muted = False
                        pygame.mixer.music.play(-1)
                    if event.key in [K_RETURN, K_SPACE]:
                        click = True
                    if event.key in [K_UP, K_w]:
                        self.move_pressed = False
                        if self.highlight_ind > 0:
                            self.highlight_ind -= 1
                        else:
                            self.highlight_ind = len(self.buttons)-1
                    if event.key in [K_DOWN, K_s]:
                        self.move_pressed = False
                        if self.highlight_ind < len(self.buttons)-1:
                            self.highlight_ind += 1
                        else:
                            self.highlight_ind = 0

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.image_menu, self.image_menu.get_rect())
            self.screen.blit(self.image_difficulty, (700,0))
            self.screen.blit(self.image_index, self.ind_position[self.buttons[self.highlight_ind]])

            if highlighted == "łatwy" and click:
                self.option.menu.difficulty_level = "łatwy"
                self.option.menu.set_difficulty_config()
                self.loop = False
            elif highlighted == "średni" and click:
                self.option.menu.difficulty_level = "średni"
                self.option.menu.set_difficulty_config()
                self.loop = False
            elif highlighted == "trudny" and click:
                self.option.menu.difficulty_level = "trudny"
                self.option.menu.set_difficulty_config()
                self.loop = False

            pygame.display.flip()
            main_clock.tick(30)


class HelpScreen:
    """
    Help screen instance
    """
    def __init__(self, menu):
        pygame.init()

        self.menu = menu
        self.screen = menu.screen
        pygame.mouse.set_visible(0)

        self.image_menu = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "menu_instrukcja.png"))

        self.muted = self.menu.muted

        self.loop = True
        self.help_menu()

    def help_menu(self):
        """
        function with main loop
        """
        while self.loop:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP:
                    if event.key in [K_ESCAPE, K_RETURN, K_SPACE]:
                        self.loop = False
                    if event.key == K_m and not self.muted:
                        self.muted = True
                        self.menu.muted = True
                        pygame.mixer.music.stop()
                    elif event.key == K_m and self.muted:
                        self.muted = False
                        self.menu.muted = False
                        pygame.mixer.music.play(-1)


            self.screen.fill((0, 0, 0))
            self.screen.blit(self.image_menu, self.image_menu.get_rect())

            pygame.display.flip()
            main_clock.tick(30)


class HighScoreScreen:
    """
    High score screen instance
    """
    def __init__(self, menu):
        pygame.init()

        self.menu = menu
        self.myfont = pygame.font.SysFont('Comic Sans MS', 40)

        self.screen = menu.screen
        pygame.mouse.set_visible(0)

        self.image_menu = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "menu_tabela_wynikow.png"))
        self.image_field_left = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "tabela_wynikow_pole_lewo.png"))
        self.image_field_right = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "tabela_wynikow_pole_prawo.png"))

        self.result_dict_left = dict()
        self.result_dict_right = dict()

        self.score_load()

        self.muted = self.menu.muted

        self.loop = True
        self.highscore_menu()

    def highscore_menu(self):
        """
        function with main loop
        """
        while self.loop:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP:
                    if event.key in [K_RETURN, K_SPACE, K_ESCAPE]:
                        self.loop = False
                    if event.key == K_m and not self.muted:
                        self.muted = True
                        self.menu.muted = True
                        pygame.mixer.music.stop()
                    elif event.key == K_m and self.muted:
                        self.muted = False
                        self.menu.muted = False
                        pygame.mixer.music.play(-1)

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.image_menu, (0,0))
            self.screen.blit(self.image_field_left, (0,0))
            self.screen.blit(self.image_field_right, (0,0))

            for i in range(1, len(self.result_dict_left)+1):
                self.screen.blit(self.result_dict_left[i], (120, 230+i*50))
            for i in range(13, 13+len(self.result_dict_right)):
                self.screen.blit(self.result_dict_right[i], (1080, 230+(i-12)*50))

            pygame.display.flip()
            main_clock.tick(30)

    def score_load(self):
        """
        function loads scoreboard data
        """
        def score_sort(el):
            """
            function to sort result list
            """
            return float(el[1])

        try:
            with open(os.path.join(path_media_elements, "tablica_wynikow.txt"), "r") as file:
                score = file.read()
        except:
            score = ""

        records = []
        last_record = 0

        for i in range(len(score)):
            if score[i:i+3] == ";;;":
                separator = score[last_record:i].find(":::")
                record_name = score[last_record:last_record+separator]
                record_score = score[last_record+separator+3:i]
                records.append((record_name, record_score))
                last_record = i+3

        records.sort(reverse=True, key=score_sort)

        if len(records)<13:
            for i in range(1,len(records)+1):
                self.result_dict_left[i] = self.myfont.render(f"{i}. {records[i-1][0]}: {records[i-1][1]}", False, (255, 255, 255))
        elif len(records)<25:
            for i in range(1,13):
                self.result_dict_left[i] = self.myfont.render(f"{i}. {records[i-1][0]}: {records[i-1][1]}", False, (255, 255, 255))
            for i in range(13,len(records)+1):
                self.result_dict_right[i] = self.myfont.render(f"{i}. {records[i-1][0]}: {records[i-1][1]}", False, (255, 255, 255))
        else:
            for i in range(1,13):
                self.result_dict_left[i] = self.myfont.render(f"{i}. {records[i-1][0]}: {records[i-1][1]}", False, (255, 255, 255))
            for i in range(13,25):
                self.result_dict_right[i] = self.myfont.render(f"{i}. {records[i-1][0]}: {records[i-1][1]}", False, (255, 255, 255))


class CreditsScreen:
    """
    Credits screen instance
    """
    def __init__(self, menu):
        pygame.init()

        self.menu = menu
        self.screen = menu.screen
        pygame.mouse.set_visible(0)

        self.image_menu = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "menu_o_autorze.png"))

        self.muted = self.menu.muted

        self.loop = True
        self.help_menu()

    def help_menu(self):
        """
        function with main loop
        """
        while self.loop:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP:
                    if event.key in [K_ESCAPE, K_RETURN, K_SPACE]:
                        self.loop = False
                    if event.key == K_m and not self.muted:
                        self.muted = True
                        self.menu.muted = True
                        pygame.mixer.music.stop()
                    elif event.key == K_m and self.muted:
                        self.muted = False
                        self.menu.muted = False
                        pygame.mixer.music.play(-1)


            self.screen.fill((0, 0, 0))
            self.screen.blit(self.image_menu, self.image_menu.get_rect())

            pygame.display.flip()
            main_clock.tick(30)


class PauseScreen:
    """
    Game pause screen instance
    """
    def __init__(self, game):
        pygame.init()

        self.game = game
        self.screen = game.screen
        pygame.mouse.set_visible(0)

        self.sound_select = pygame.mixer.Sound(os.path.join(path_media_elements, "dzwieki", "menu_select.wav"))

        self.highlight_ind = 0
        self.buttons = ["wznów", "zakończ"]

        self.image_game = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "obraz_przed_pauza.png"))
        self.image_pause = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "pauza_przyciski.png"))
        self.image_index = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "wskaznik_bialy.png"))

        self.ind_position = {"wznów": (1130, 519), "zakończ": (1130, 650)}

        self.move_pressed = False
        self.muted = self.game.menu.muted

        self.loop = True
        self.pause()

    def pause(self):
        """
        function with main loop
        """
        while self.loop:
            self.game.tps_delta += self.game.tps_clock.tick() / 1000
            while self.game.tps_delta > 1 / self.game.tps_max:
                self.game.tps_delta -= 1 / self.game.tps_max

            click = False
            highlighted = self.buttons[self.highlight_ind]

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key in [K_UP, K_w, K_DOWN, K_s] and (not self.move_pressed) and (not self.muted):
                    self.sound_select.play()
                    self.move_pressed = True
                if event.type == KEYUP:
                    if event.key in [K_ESCAPE, K_p]:
                        self.loop = False
                    if event.key == K_m and not self.muted:
                        self.muted = True
                        self.game.muted = True
                        self.game.menu.muted = True
                        pygame.mixer.music.stop()
                    elif event.key == K_m and self.muted:
                        self.muted = False
                        self.game.muted = False
                        self.game.menu.muted = False
                        pygame.mixer.music.play(-1)
                    if event.key in [K_RETURN, K_SPACE]:
                        click = True
                    if event.key in [K_UP, K_w]:
                        self.move_pressed = False
                        if self.highlight_ind > 0:
                            self.highlight_ind -= 1
                        else:
                            self.highlight_ind = len(self.buttons)-1
                    if event.key in [K_DOWN, K_s]:
                        self.move_pressed = False
                        if self.highlight_ind < len(self.buttons)-1:
                            self.highlight_ind += 1
                        else:
                            self.highlight_ind = 0
            self.screen.fill((0,0,0))
            self.screen.blit(self.image_game, (0,0))
            self.screen.blit(self.image_pause, (0,0))
            self.screen.blit(self.image_index, self.ind_position[self.buttons[self.highlight_ind]])

            if highlighted == "wznów" and click:
                    self.loop = False
            elif highlighted == "zakończ" and click:
                    self.loop = False
                    ResultScreen(self.game)
                    self.game.loop = False

            pygame.display.flip()
            main_clock.tick(30)


class ResultScreen:
    """
    Game over screen instance
    """
    def __init__(self, game):
        pygame.init()

        self.game = game
        self.screen = game.screen
        pygame.mouse.set_visible(0)
        self.myfont = pygame.font.SysFont('Comic Sans MS', 40)

        self.image_result = pygame.image.load(os.path.join(path_media_elements, "grafika_menu", "podawanie_wyniku.png"))

        self.name = ""

        self.loop = True
        self.result()

    def result(self):
        """
        function with main loop
        """
        while self.loop:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        self.loop = False
                        self.game.break_loop = True
                    if event.key == K_RETURN and len(self.name)>0:
                        self.loop = False
                        self.game.break_loop = True

                        with open(os.path.join(path_media_elements, "tablica_wynikow.txt"), "a")as file:
                            file.write(f"{self.name}:::{self.game.player.score};;;")
                    if event.key == K_BACKSPACE and len(self.name)>0:
                        self.name = self.name[:-1]
                    else:
                        if len(self.name)<10:
                            key = str(pygame.key.name(event.key))
                            if len(key) == 1:
                                self.name += key

            score_surface = self.myfont.render(f"{self.game.player.score}", False, (255, 255, 255))
            name_surface = self.myfont.render(f"{self.name}", False, (255, 255, 255))
            self.screen.fill((0,0,0))
            self.screen.blit(self.image_result, (0,0))
            self.game.screen.blit(score_surface, (960, 435))
            self.game.screen.blit(name_surface, (920, 590))

            pygame.display.flip()
            main_clock.tick(30)


class Game(object):
    """
    Game screen instance
    """
    def __init__(self, menu):
        self.tps_max = 40
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 18)
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.tps_clock = pygame.time.Clock()
        self.tps_delta = 0.0

        self.menu = menu
        self.control_buttons = menu.control_buttons
        self.map_layout = menu.map_layout

        self.player = Shooter(self)
        self.arena = Arena(self)
        self.bots = []
        self.gameplay = GamePlay(self)

        self.muted = self.menu.muted

        self.loop = True
        self.pause_loop = False
        self.break_loop = False

        while self.loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYUP and event.key in [pygame.K_ESCAPE, pygame.K_p]:
                    pygame.image.save(self.screen, os.path.join(path_media_elements, "grafika_menu", "obraz_przed_pauza.png"))
                    PauseScreen(self)
                if event.type == pygame.KEYUP and event.key == K_m and not self.muted:
                    self.muted = True
                    self.menu.muted = True
                    pygame.mixer.music.stop()
                elif event.type == pygame.KEYUP and event.key == K_m and self.muted:
                    self.muted = False
                    self.menu.muted = False
                    pygame.mixer.music.play(-1)

            if self.player.hit_points_current <= 0:
                ResultScreen(self)

            if self.break_loop:
                break

            # ticking
            self.tps_delta += self.tps_clock.tick()/1000
            while self.tps_delta > 1/self.tps_max:
                self.tick()
                self.tps_delta -= 1/self.tps_max

            # drawing
            self.screen.fill((39, 39, 39))
            self.draw()
            pygame.display.flip()

    def tick(self):
        """
        function maintains game instances (player, bots, arena) ticks
        """
        self.player.tick()
        for sec in self.arena.sectors:
            self.arena.sectors[sec].tick()
        for bot in self.bots:
            bot.tick()
        self.gameplay.tick()

    def draw(self):
        """
        function maintains drawing game object on screen
        """
        self.arena.draw()
        self.player.draw()
        self.gameplay.draw()
        for bot in self.bots:
            bot.draw()


if __name__ == "__main__":
    StartScreen()
