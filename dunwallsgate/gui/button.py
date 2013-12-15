import pygame
from gui.textpanel import TextPanel

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
            "border_color": (122, 66, 0)
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
        "center": False,
        "fontsize": 17
    }
}


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
        self._image = {"clicked": None, "overred": None, "default": None}
        for key in self._image:
            self._image[key] = pygame.surface.Surface(size, pygame.SRCALPHA)
            self._image[key].fill(self.style[key]["background_color"])
            if "border_color" in self.style[key]:
                pygame.draw.rect(self._image[key],
                                 self.style[key]["border_color"],
                                 (0, 0, size[0], size[1]), 3)
            text_img = TextPanel(self.text, font=("joystix",
                                                  self.style["fontsize"]),
                                 color=self.style[key]["text_color"],
                                 box=size)
            pos = pygame.Rect()
            if self.style.get("center", True):
                pos.center = self.rect.center
            else:
                pos.ycenter = self.rect.ycenter
                pos.x = 3
            self._image[key].blit(text_img.image, pos)
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
            return self._image["clicked"]
        elif self.overred:
            return self._image["clicked"]
        else:
            return self._image["clicked"]

    @property
    def click_time(self):
        return max(0, self._click_time)

    @click_time.setter
    def click_time(self, value):
        self._click_time = max(0, value)
