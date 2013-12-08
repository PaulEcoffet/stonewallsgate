import pygame
from screens.text_render import TextRender

GREEN_RGB = (0, 255, 0)
YELLOW_RGB = (255, 215, 0)
RED_RGB = (255, 0, 0)
BLACK_RGB = (0, 0, 0)
ORANGE_RGB = (255, 69, 0)


class LifeBar(pygame.sprite.Sprite):
    """shows a bar with the health of a charac"""

    def __init__(self, charac):
        self.charac = charac
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((200, 15))
        pygame.draw.rect(self.image, BLACK_RGB, (0, 0, 200, 15), 1)
        self.rect = self.image.get_rect()
        self.percent = 0
        self.oldpercent = 0
        self.smooth_revision = 0
        self.i = 0
        self.pg_font = pygame.font.SysFont("joystix", 26)
        self.block = False

    def resize(self, width=0, height=0):
        self.image = pygame.transform.scale(self.image, (width, height))

    def move(self, x=0, y=0):
        self.rect = self.image.get_rect(midtop=(x, y))

    def draw_greenbar(self, health, color):
        pygame.draw.rect(self.image, color, (0, 0,
                         int(200 * health / self.charac.maxhealth), 15),
                         0)  # fill green
        if health != 0:
            a = self.pg_font.render("%d/%d" % (health, self.charac.maxhealth),
                                    1, (200, 80, 15))
            self.image.blit(a, (147, 1))
        else:
            a = self.pg_font.render("DEAD", 1, RED_RGB)
            self.image.blit(a, (75, 1))

    def get_color(self, hppercent):
        if hppercent == 0:
            return (0, 0, 0)
        elif hppercent > 0.5:
            return (255 * (1 - hppercent) * 2, 255, 0)
        else:
            return (255, 255 * (hppercent) * 2, 0)

    def update(self):
        if self.smooth_revision != self.charac.health:
            health_left = self.smooth_revision - self.charac.health
            self.smooth_revision -= abs(health_left) / health_left
            #self.percent = self.charac.health / self.charac.maxhealth
            self.percent = self.smooth_revision / self.charac.maxhealth
            color = self.get_color(self.percent)
            if self.percent != self.oldpercent or color != self.old_color:
                pygame.draw.rect(self.image, BLACK_RGB,
                                 (0, 0, 200 - 2, 15))  # fill black
                self.draw_greenbar(self.smooth_revision, color)
                self.oldpercent = self.percent
                self.old_color = color

        if self.percent == 0:
            pygame.draw.rect(self.image, BLACK_RGB,
                             (0, 0, 200 - 2, 15))  # fill black
            self.draw_greenbar(self.charac.health,
                               self.get_color(self.charac.health))


class Portrait(pygame.sprite.Sprite):

    def __init__(self, cache, charact, position="front", highlighted=True):
        super().__init__()
        self.name = charact.name
        self.id = (charact, position, highlighted)
        self.default_image = cache.get_portrait_image(charact.ref, position)
        self.transparent = pygame.Surface((300, 100), pygame.SRCALPHA)
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
        self.default_image = pygame.transform.scale(self.default_image,
                                                    (width, height))
        self.init_highlighted()
        self.init_attenuated()

    def move(self, x=0, y=0):
        self.rect = self.image.get_rect(midtop=(x, y))

    def init_highlighted(self):
        label = TextRender((300, 100), "joystix", 35, (200, 80, 15),
                           ">" + self.name)
        self.highlighted_image = pygame.Surface.copy(self.default_image)
        self.highlighted_image.blit(self.transparent, (20, 185))
        self.highlighted_image.blit(label.next(), (25, 181))

    def init_attenuated(self):
        label = TextRender((300, 100), "joystix", 35, (200, 80, 15),
                           ">" + self.name)
        self.attenuated_image = pygame.Surface.copy(self.default_image)
        self.attenuated_image.fill((255, 255, 255, 140), None,
                                   pygame.BLEND_RGBA_MULT)
        self.attenuated_image.blit(self.transparent, (20, 185))
        self.attenuated_image.blit(label.next(), (25, 181))

    @property
    def image(self):
        if self.highlighted:
            return self.highlighted_image
        else:
            return self.attenuated_image
