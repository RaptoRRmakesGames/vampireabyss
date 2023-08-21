import pygame 
import os
pygame.init()

from scripts.utils import load_images_from_folder


class Writing:
    def __init__(self, size):
        self.size = size
        images = load_images_from_folder('assets/fonts/font_images/')
        self.char_names = list('abcdefghijklmnopqrstuvwxyz1234567890%:.')
        self.characters = {}
        for index, charname in enumerate(self.char_names):
            self.characters[charname] = pygame.transform.scale(images[index], (self.size, self.size))

        self.offset = self.size - int(self.size /5)
        
        self.cached_colors = {}
        self.cached_texts = {}
        
    def cache_full_color(self, color):
        self.cached_colors[(color.r, color.g, color.b)] = {}
        for i,image in enumerate(self.characters.values()):
            img = self.characters[list(self.characters.keys())[i]].copy()
            self.change_color(img, color)
            
            self.cached_colors[(color.r, color.g, color.b)][self.char_names[i]] = img

    def cache_color(self, letter, color, image):
        
        if (color.r, color.g, color.b) in self.cached_colors.keys():
            self.cached_colors[(color.r, color.g, color.b)][letter] = image
        else:
            
            self.cached_colors[(color.r, color.g, color.b)] = {}
            
    def cache_text(self, text, color, surface):
        
        if (color.r, color.g, color.b) in self.cached_texts.keys():
            
            self.cached_texts[(color.r, color.g, color.b)][text] = surface
        else:
            
            self.cached_texts[(color.r, color.g, color.b)] = {}
            self.cached_texts[(color.r, color.g, color.b)][text] = surface
            
    def change_color(self, img, color):
        for x in range(img.get_width()):
            for y in range(img.get_height()):
                color.a = img.get_at((x, y)).a
                img.set_at((x, y), color)

    def write(self, text, color=pygame.Color(0, 0, 0)):
        
        write_surface = pygame.Surface((len(text) * self.size, self.size), pygame.SRCALPHA)
        
        text = text.lower()
        
        
        if (color.r, color.g, color.b) in self.cached_texts.keys() and text in self.cached_texts[(color.r, color.g, color.b)].keys():
            write_surface = self.cached_texts[(color.r, color.g, color.b)][text]
        else:
            for i, letter in enumerate(text):
                if letter in self.characters:



                    if (color.r, color.g, color.b) in self.cached_colors.keys() and letter in self.cached_colors[(color.r, color.g, color.b)].keys():
                        final_img = self.cached_colors[(color.r, color.g, color.b)][letter]

                    else:


                        img_copy = self.characters[letter.lower()].copy()
                        # for x in range(img_copy.get_width()):
                        #     for y in range(img_copy.get_height()):
                        #         color.a = img_copy.get_at((x, y)).a
                        #         img_copy.set_at((x, y), color)
                        self.change_color(img_copy, color)

                        self.cache_color(letter, color, img_copy)

                        final_img = img_copy




                    write_surface.blit(final_img, (i * self.offset, 0))
                
            self.cache_text(text, color, write_surface)
        return write_surface

room_writing = Writing(16)