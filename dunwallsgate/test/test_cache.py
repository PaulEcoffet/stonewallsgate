import unittest
import cache
import pygame


class TestCache(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.surface = pygame.display.set_mode((200, 200))

    def test_load_all(self):
        cache.load_all()
        self.assertTrue(cache._background_images and cache._portrait_images)
        cache.clear_all()
        self.assertDictEqual(cache._background_images, {})
        self.assertDictEqual(cache._portrait_images, {})

    def test_portrait_get_image(self):
        a = cache.get_portrait_image("hero", "front")
        b = cache.get_portrait_image("hero", "front")
        self.assertIs(a, b)
