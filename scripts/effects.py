import pygame , os

from scripts.animations import Animation

class Lighting:
    
    def __init__(self, hit_pos) -> None:
        self.animation = Animation([pygame.image.load('assets/images/lighting/' + fn).convert_alpha() for fn in os.listdir('assets/images/lighting/')], 50)
        
        self.rect = pygame.FRect(0,0,*self.animation.get_image().get_size())
        self.rect.left, self.rect.bottom = hit_pos
        
        self.to_be_removed = False
        
    def update(self):
        
        self.animation.update()
        
        self.image = self.animation.get_image()
        
        if self.animation.done:
            self.to_be_removed = True
        
    def render(self, display, offset):
        
        render_rect = pygame.FRect(self.rect.x - offset[0], self.rect.y - offset[1], self.rect.width, self.rect.height)
        
        display.blit(self.image, render_rect)
        
        return render_rect