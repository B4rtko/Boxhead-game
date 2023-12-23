from dataclasses import dataclass, field

import pygame


@dataclass
class ConfigControls:
    """Class for storing game parameters for different difficulty levels"""
    góra: int = pygame.K_w
    dół: int = pygame.K_s
    lewo: int = pygame.K_a
    prawo: int = pygame.K_d
    strzał: int = pygame.K_k
    następna: int = pygame.K_e
    poprzednia: int = pygame.K_q

    def __getitem__(self, item):
        return getattr(self, item)
