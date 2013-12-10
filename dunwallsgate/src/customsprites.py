import pygame
from screens.text_render import TextRender

GREEN_RGB = (0, 255, 0)
YELLOW_RGB = (255, 215, 0)
RED_RGB = (255, 0, 0)
BLACK_RGB = (0, 0, 0)
ORANGE_RGB = (255, 69, 0)

class LifeBox(pygame.sprite.Sprite):
    """shows a bar with the health of a charac"""

    def __init__(self, charac):
        self.charac = charac
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((190, 80), pygame.SRCALPHA)
        self.image.fill((225,227,202,144))
        pygame.draw.rect(self.image, (225,227,202), (0, 0, 190, 80), 1)
        pygame.draw.rect(self.image, BLACK_RGB, (0, 0, 185, 65), 1)
        a = TextRender((185, 65), "joystix", 18, BLACK_RGB, self.charac.name)
        self.image.blit(a.next(), (6, 60))
        self.rect = self.image.get_rect()
        self.percent = 0
        self.oldpercent = 0
        self.smooth_revision = 0
        self.i = 0

    def resize(self, width=0, height=0):
        self.image = pygame.transform.scale(self.image, (width, height))

    def move(self, x=0, y=0):
        self.rect = self.image.get_rect(midtop=(x, y))

    def draw_text(self, health):
        if health != 0:
            a = TextRender((185, 65), "joystix", 41, self.get_color(health/self.charac.maxhealth), "%dHP" % (health))
            self.image.blit(a.next(), (6, 7))
        else:
            a = self.pg_font.render("DEAD", 26, RED_RGB)
            self.image.blit(a, (1, 75))

    def get_color(self, hppercent):
        if hppercent == 0:
            return (0, 0, 0)
        elif hppercent > 0.5:
            return (133 * (1 - hppercent) * 1.097744+133, 206, 135)
        else:
            return (206, 133 * (hppercent) * 1.097744+133, 135)

    def update(self):
        if self.smooth_revision != self.charac.health:
            health_left = self.smooth_revision - self.charac.health
            self.smooth_revision -= abs(health_left) / health_left
            self.percent = self.smooth_revision / self.charac.maxhealth
            color = self.get_color(self.percent)
            if self.percent != self.oldpercent or color != self.old_color:
                pygame.draw.rect(self.image, BLACK_RGB,
                                 (0, 0, 185, 65))  # fill black
                self.draw_text(self.smooth_revision)
                self.oldpercent = self.percent
                self.old_color = color

        if self.charac.health == 0:
            pygame.draw.rect(self.image, BLACK_RGB,
                             (0, 0, 185, 65))  # fill black
            self.draw_text(self.charac.health)
                               
                               
class LifeBar(pygame.sprite.Sprite):
    """shows a bar with the health of a charac"""

    def __init__(self, charac):
        self.charac = charac
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((26, 200))
        pygame.draw.rect(self.image, BLACK_RGB, (0, 0, 26, 200), 1)
        self.rect = self.image.get_rect()
        self.percent = 0
        self.oldpercent = 0
        self.smooth_revision = 0
        self.i = 0
        self.pg_font = pygame.font.SysFont("joystix", 26)
        self.block = False

    def resize(self, width=26, height=200):
        self.image = pygame.transform.scale(self.image, (width, height))

    def move(self, x=0, y=0):
        self.rect = self.image.get_rect(midtop=(x, y))

    def draw_greenbar(self, health, color):
        self.image = pygame.transform.rotate(self.image, 180)
        pygame.draw.rect(self.image, color, (3, 0,
                         20, int(200 * health / self.charac.maxhealth)-5),
                         0)  # fill green
        self.image = pygame.transform.rotate(self.image, 180)

    def get_color(self, hppercent):
        if hppercent == 0:
            return (0, 0, 0)
        elif hppercent > 0.5:
            return (133 * (1 - hppercent) * 1.097744+133, 206, 135)
        else:
            return (206, 133 * (hppercent) * 1.097744+133, 135)

    def update(self):
        if self.smooth_revision != self.charac.health:
            health_left = self.smooth_revision - self.charac.health
            self.smooth_revision -= abs(health_left) / health_left
            #self.percent = self.charac.health / self.charac.maxhealth
            self.percent = self.smooth_revision / self.charac.maxhealth
            color = self.get_color(self.percent)
            if self.percent != self.oldpercent or color != self.old_color:
                pygame.draw.rect(self.image, BLACK_RGB,
                                 (0, 0, 26,  200))  # fill black
                self.draw_greenbar(self.smooth_revision, color)
                self.oldpercent = self.percent
                self.old_color = color

        if self.percent == 0:
            pygame.draw.rect(self.image, BLACK_RGB,
                             (0, 0, 26,  200))  # fill black
            self.draw_greenbar(self.charac.health,
                               self.get_color(self.charac.health))


class Portrait(pygame.sprite.Sprite):

    def __init__(self, cache, charact, position="front", highlighted=True):
        super().__init__()
        self.name = charact.name
        self.id = (charact, position)
        self.default_image = cache.get_portrait_image(charact.ref, position)
        self.transparent = pygame.Surface((300, 37), pygame.SRCALPHA)
        self.transparent.fill((0, 0, 0, 200))
        self.highlighted = highlighted
        self.highlighted_image = None
        self.attenuated_image = None
        self.resize()

    def update(self, highlighted):
        if self in highlighted:
            self.highlighted = True
        else:
            self.highlighted = False

    def resize(self, width=440, height=221):
        self.width = width
        self.height = height
        self.default_image = pygame.transform.scale(self.default_image,
                                                    (width, height))
        self.init_highlighted()
        self.init_attenuated()

    def move(self, x=0, y=0):
        self.rect = self.image.get_rect(midtop=(x, y))

    def init_highlighted(self):
        label = TextRender((300, 50), "joystix", 35, (200, 80, 15),
                           ">" + self.name)
        self.highlighted_image = pygame.Surface.copy(self.default_image)
        self.highlighted_image.blit(self.transparent, (self.width*0.11, 0.856*self.height))
        self.highlighted_image.blit(label.next(), (self.width*0.12, 0.836*self.height))

    def init_attenuated(self):
        label = TextRender((300, 50), "joystix", 35, (200, 80, 15),
                           self.name)
        self.attenuated_image = pygame.Surface.copy(self.default_image)
        self.attenuated_image.fill((255, 255, 255, 140), None,
                                   pygame.BLEND_RGBA_MULT)
        self.attenuated_image.blit(self.transparent, (self.width*0.11, 0.856*self.height))
        self.attenuated_image.blit(label.next(), (self.width*0.12, 0.836*self.height))

    @property
    def image(self):
        if self.highlighted:
            return self.highlighted_image
        else:
            return self.attenuated_image

class MiniPortrait(pygame.sprite.Sprite):

    def __init__(self, cache, charact, highlighted=True):
        super().__init__()
        self.name = charact.name
        self.id = (charact,)
        self.default_image = cache.get_portrait_image(charact.ref, "mini")
        self.highlighted = highlighted
        self.highlighted_image = None
        self.attenuated_image = None
        self.resize()

    def update(self, highlighted):
        if self in highlighted:
            self.highlighted = True
        else:
            self.highlighted = False

    def resize(self, width=100, height=100):
        self.width = width
        self.height = height
        self.default_image = pygame.transform.scale(self.default_image,
                                                    (width, height))
        self.init_highlighted()
        self.init_attenuated()

    def move(self, x=0, y=0):
        self.rect = self.image.get_rect(midtop=(x, y))

    def init_highlighted(self):
        self.highlighted_image = pygame.Surface.copy(self.default_image)

    def init_attenuated(self):
        self.attenuated_image = pygame.Surface.copy(self.default_image)
        self.attenuated_image.fill((255, 255, 255, 140), None,
                                   pygame.BLEND_RGBA_MULT)

    @property
    def image(self):
        if self.highlighted:
            return self.highlighted_image
        else:
            return self.attenuated_image