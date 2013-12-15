import unittest
import pygame
from gui.textpanel import TextPanel


class TestTextPanel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.surface = pygame.display.set_mode((300, 300))
        cls.surface.fill((255, 255, 255))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_line_number(self):
        panel = TextPanel("word\nword", height=2000)
        self.assertEqual(len(panel.lines), 2)

    def test_panel_wrap(self):
        panel = TextPanel("word word\nword word", width=50)
        self.assertEqual(len(panel.lines), 4)
        panel = TextPanel("word word\nword word\n" * 10, width=50)
        self.assertEqual(len(panel.lines), 40)
        panel = TextPanel("word word\nword word\n" * 10, width=500)
        self.assertEqual(len(panel.lines), 20)

    def test_loading_unexisting_font(self):
        panel = TextPanel("test", font=("__unexisting_font__", 10))
        self.assertEqual(panel.font.name, "Larabiefont")

    def test_cache_font(self):
        panel1 = TextPanel("test", font=("larabiefont", 10))
        panel2 = TextPanel("test", font=("larabiefont", 10))
        self.assertIs(panel1.font, panel2.font)

    def test_set_current_panel_index_failure(self):
        panel = TextPanel("word " * 5, font=("larabiefont", 10))

        def set_wrong_value():
            panel.current_panel_index = 1
        self.assertRaises(ValueError, set_wrong_value)

    def test_get_current_panel_index(self):
        panel = TextPanel("word " * 5, font=("larabiefont", 10), width=50,
                          height=20)
        self.assertEqual(panel.current_panel_index, 0)
        panel.next_panel()
        self.assertEqual(panel.current_panel_index, 1)

    @unittest.skip("Should not be reviewed by human")
    def test_drawing(self):
        panel = TextPanel("Lorem ipsum dolor sit amet, consectetur adipiscing"
                          " elit. Praesent tristique, turpis vitae facilisis"
                          " condimentum, libero libero venenatis ipsum,"
                          " id commodo lorem ante in eros.\nDonec elementum,"
                          " nisi ut ornare rutrum.", font=("larabiefont", 18),
                          width=self.surface.get_rect().width - 20,
                          height=self.surface.get_rect().height - 20)
        self.surface.fill((255, 255, 255))
        panel.update(to_end=True)
        self.surface.blit(panel.image, (10, 10))
        pygame.display.flip()

    @unittest.skip("Should not be reviewed by human")
    def test_animation(self):
        fpsclock = pygame.time.Clock()
        self.surface.fill((255, 255, 255))
        panel = TextPanel("Lorem ipsum dolor sit amet, consectetur adipiscing"
                          " elit. Praesent tristique, turpis vitae facilisis"
                          " condimentum, libero libero venenatis ipsum,"
                          " id commodo lorem ante in eros.\nDonec elementum,"
                          " nisi ut ornare rutrum.", font=("larabiefont", 18),
                          width=self.surface.get_rect().width - 20,
                          height=self.surface.get_rect().height - 20)
        while not panel.anim_has_ended:
            self.surface.fill((255, 255, 255))
            self.surface.blit(panel.image, (10, 10))
            panel.update()
            fpsclock.tick(30)
            pygame.display.flip()
