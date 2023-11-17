
import pygame 


class Lighting: 
    
    def __init__(self, game) -> None:
        self.lights = {}
        self.base_surf = pygame.Surface((game.display.get_size())).convert_alpha()
        self.dark_amount = 50
        self.__reset_dark_surf()
    
    def __reset_dark_surf(self):
        self.base_surf.fill((self.dark_amount, self.dark_amount, self.dark_amount))
    
    def __create_light_surf(self, color_range, circle_multiplier, color_extra):
        light_surf = pygame.Surface((color_range *2,color_range *2), pygame.SRCALPHA).convert_alpha()

        for i in range(color_range):
            pygame.draw.circle(light_surf, (round(i *color_extra[0])  ,round(i *color_extra[1])  ,round(i * color_extra[2]) ), (light_surf.get_width()//2,light_surf.get_height()//2), color_range - i)

        light_surf = pygame.transform.scale(light_surf, (light_surf.get_width()*circle_multiplier,light_surf.get_height()*circle_multiplier))
        
        return light_surf
    
    def get_base_surf(self):
        
        return self.base_surf
    
    def get_light_surf(self, nick):
        
        return self.lights[nick]
        
    def set_dark_amount(self, newamount):
        self.dark_amount = newamount
        
    def clear_lights(self):
        self.__reset_dark_surf()
        
    def create_light(self, nick, col_range=100, size_multi= 1, color_extra = (1,1,1)):
        self.lights[nick] = self.__create_light_surf(col_range, size_multi, color_extra)
        
    
    
    def create_light_folder(self, fold_name, keys, vals):
        
        self.lights[fold_name] = {}
        
        for x, key in enumerate(keys):
            
            self.lights[fold_name][key] = vals[x]
            
    def render_nat_from_folder(self, fold_name, key, pos, scroll=[0,0], dark=False):
        
        self.base_surf.blit(self.lights[fold_name][key], (pos[0] - scroll[0],pos[1] - scroll[1]), special_flags = pygame.BLEND_RGBA_ADD if not dark else pygame.BLEND_MULT)
        
    def render_unnat_from_folder(self, display, fold_name, key, pos, scroll=[0,0], dark=False):
        
        display.blit(self.lights[fold_name][key], (pos[0] - scroll[0],pos[1] - scroll[1]), special_flags = pygame.BLEND_RGBA_ADD if not dark else pygame.BLEND_MULT)
        
    
    def render_nat_light(self, nick, pos, scroll=[0,0], dark=False):
        self.base_surf.blit(self.lights[nick], (pos[0]- scroll[0], pos[1]- scroll[1]), special_flags = pygame.BLEND_RGBA_ADD if not dark else pygame.BLEND_MULT)

    def render_unnat_light(self, display, nick, pos, scroll=[0,0], dark=False):
        display.blit(self.lights[nick], (pos[0]- scroll[0], pos[1]- scroll[1]), special_flags = pygame.BLEND_RGBA_ADD if not dark else pygame.BLEND_MULT)
        
    