import pygame
from screens.text_render import TextRender

GREEN_RGB = (0, 255, 0)
YELLOW_RGB = (255, 215, 0)
RED_RGB = (255, 0, 0)
BLACK_RGB = (0, 0, 0)
ORANGE_RGB = (255, 69, 0)

_button_style = {
    "default": {
        "clicked": {
            "text_color": RED_RGB,
            "background_color": (15, 15, 15),
            "border_color": ORANGE_RGB
        },
        "overred": {
            "text_color": ORANGE_RGB,
            "background_color": BLACK_RGB,
            "border_color": (109, 130, 38)
        },
        "default": {
            "text_color": (255, 255, 255),
            "background_color": BLACK_RGB,
            "border_color": (122,66,0)
        },
        "fontsize": 22
    },
    "box_options": {
        "clicked": {
            "text_color": RED_RGB,
            "background_color": (15, 15, 15, 120)
        },
        "overred": {
            "text_color": ORANGE_RGB,
            "background_color": (0, 0, 0, 120)
        },
        "default": {
            "text_color": (255, 158, 0),
            "background_color": (0, 0, 0, 120)
        },
        "fontsize": 13
    },
    "dialogue_choices": {
        "clicked": {
            "text_color": RED_RGB,
            "background_color": (0, 0, 0, 255)
        },
        "overred": {
            "text_color": ORANGE_RGB,
            "background_color": (0, 0, 0, 120)
        },
        "default": {
            "text_color": (255, 158, 0),
            "background_color": (0, 0, 0, 120)
        },
        "center" : False,
        "fontsize": 17
    }
}

def centering(size, k, i, center=True):
    a = b = 0
    if not center:
        k = size[0]-3
    while 2*a != round(size[0]-k,0) and a <= 7000:
        a += 0.5
    while 2*b != round(size[1]-i,0) and b <= 7000:
        b += 0.5
    if a == 7000 or b == 7000:
        print("Ce code est bien foireux")
    return (a, b)


class Button(pygame.sprite.Sprite):
    """generic button which can be improved"""

    def __init__(self, eventmanager, cat, text, size=(380, 50),
                 style="default", customstyle=None):
        super().__init__()
        try:
            self.style = _button_style[style]
        except KeyError:
            self.style = _button_style["default"]
        self.eventmanager = eventmanager
        self.cat = cat
        self.text = text
        self.overred = False
        self.is_clicked = False
        self._click_time = 0
        self.click_time = 0
        self.id = None
        self.events = []
        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.default_image = pygame.surface.Surface(size, pygame.SRCALPHA)
        self.default_image.fill(self.style["default"]["background_color"])
        self.clicked_image = pygame.surface.Surface(size, pygame.SRCALPHA)
        self.clicked_image.fill(self.style["clicked"]["background_color"])
        self.overred_image = pygame.surface.Surface(size, pygame.SRCALPHA)
        self.overred_image.fill(self.style["overred"]["background_color"])
        if "border_color" in self.style["default"]:
            pygame.draw.rect(self.default_image,
                             self.style["default"]["border_color"],
                             (0, 0, size[0], size[1]), 3)
        text_img = TextRender(size, "joystix", self.style["fontsize"],
                              self.style["default"]["text_color"], self.text)
        self.default_image.blit(text_img.next(), centering(size, text_img.width, text_img.height, self.style.get("center", True)))
        if "border_color" in self.style["clicked"]:
            pygame.draw.rect(self.clicked_image,
                             self.style["clicked"]["border_color"],
                             (0, 0, size[0], size[1]), 3)
        text_img = TextRender(size, "joystix", self.style["fontsize"],
                              self.style["clicked"]["text_color"], self.text)
        self.clicked_image.blit(text_img.next(), centering(size, text_img.width, text_img.height, self.style.get("center", True)))
        if "border_color" in self.style["overred"]:
            pygame.draw.rect(self.overred_image,
                             self.style["overred"]["border_color"],
                             (0, 0, size[0], size[1]), 3)
        text_img = TextRender(size, "joystix", self.style["fontsize"],
                              self.style["overred"]["text_color"], self.text)
        self.overred_image.blit(text_img.next(), centering(size, text_img.width, text_img.height, self.style.get("center", True)))
        self._register_events()

    def _register_events(self):
        self.events.append(self.eventmanager.on_mouse_down(
            lambda e: self.set_is_clicked(), self.cat, 1, self))
        self.events.append(self.eventmanager.on_mouse_up(
            lambda e: self.set_is_clicked(False), self.cat, 1, self))
        self.events.append(self.eventmanager.on_mouse_in(
            self, lambda e: self.set_overred(), self.cat))
        self.events.append(self.eventmanager.on_mouse_out(
            self, lambda e: self.set_overred(False), self.cat))

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, value):
        if value:
            self._disabled = True
            self._lock_events()
        else:
            self._disabled = False
            self._unlock_events()

    def _lock_events(self):
        self.eventmanager.lock_callback(*self.events)
        if self.id:
            self.eventmanager.lock_callback(self.id)

    def _unlock_events(self):
        self.eventmanager.unlock_callback(*self.events)
        if self.id:
            self.eventmanager.unlock_callback(self.id)

    def set_is_clicked(self, state=True):
        self.is_clicked = state
        if not state:
            self.click_time = 3

    def set_overred(self, value=True):
        self.overred = value

    def on_click(self, to_do):
        if self.id:
            self.eventmanager.remove_callback(self.id)
        self.id = self.eventmanager.on_click_on(self, to_do, self.cat)

    def update(self):
        self.click_time -= 1

    @property
    def image(self):
        if self.is_clicked or self.click_time:
            return self.clicked_image
        elif self.overred:
            return self.overred_image
        else:
            return self.default_image

    @property
    def click_time(self):
        return max(0, self._click_time)

    @click_time.setter
    def click_time(self, value):
        self._click_time = max(0, value)
