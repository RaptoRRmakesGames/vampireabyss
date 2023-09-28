import pygame 

from scripts.utils import  create_room_img

class Start_Room:
    
    def __init__(self):
        
        self.image = create_room_img()
        
        self.rect = self.image.get_rect(topleft = (300,300))
        
    def render(self, display, offset):
        
        render_rect = pygame.Rect(self.rect.x - offset[0], self.rect.y - offset[1], self.rect.width,self.rect.height)
          
        display.fblits([(self.image, render_rect)])
        

        