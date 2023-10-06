import pygame

# from scripts.writing import Writing
from scripts.settings import *
from scripts.font_inits import *

class Button:
    
    def __init__(self,
                 game,pos, action, text, textsize=10,
                 text_color = (255,255,255), button_color = (15, 50, 120), custom_text_offset=(0,0), 
                 hover_text_color=(0,0,0), size_on_hover=(130,50),sizeup_speed=1,hover_color=(255,255,255)):
        
        self.rect = pygame.FRect(pos[0], pos[1], *button_width_height)
        
        self.function = action
        
        self.game = game
        
        self.font = pygame.font.Font('assets/fonts/ttfs/pixuf.ttf', 16)
        
        self.width, self.height = self.rect.width, self.rect.height
        
        self.base_text_color =  pygame.Color(*text_color)
        self.text_color = pygame.Color(*text_color)
        
        self.base_color = pygame.Color(*button_color)
        self.color = pygame.Color(*button_color)
        
        self.cto = custom_text_offset
        
        self.text = text
        
        self.base_pos = self.rect.center
        
        self.clicked = False
        
        self.hover_dict = {
            'size_on_hover' : size_on_hover,
            'sizeup_speed' : sizeup_speed,
            'color' : hover_color,
            'text_color' : pygame.Color(hover_text_color)
        }
        
        
    def render(self, display, offset=(0,0)):
        
        # render_rect = pygame.FRect(self.rect.x - offset[0], self.rect.y - offset[1], self.width, self.height)
        
        self.rect.width = self.width
        
        self.rect.height = self.height
        
        pygame.draw.rect(display, self.color,pygame.Rect(self.rect.x - offset[0], self.rect.y - offset[1], self.width, self.height))
        display.fblits([(self.font.render(self.text, False, self.text_color), (self.rect.center[0] + self.cto[0]-offset[0], self.rect.center[1] + self.cto[1]-offset[1]))])
        # display.blit(self.writing.write(self.text, self.text_color), (self.rect.center[0] + self.cto[0]-offset[0], self.rect.center[1] + self.cto[1]-offset[1]))
        
    def set_fun(self, fun):
        
        self.function = fun
    
    def click_execute_fun(self, *args):

        
        mouse_x, mouse_y = self.game.mouse_pos
        mouse_col = self.rect.collidepoint(mouse_x, mouse_y)
        self.hover = mouse_col
        if mouse_col:   
    
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                

                
                self.clicked = True
                
                self.function(*args)
                
        if not pygame.mouse.get_pressed()[0]:
            
            self.clicked = False
            
    def animate(self,dt):
        goal_size = self.hover_dict['size_on_hover']
        sizeup_speed = self.hover_dict['sizeup_speed']
        self.hover_color = self.hover_dict['color']
        self.hover_text_color = self.hover_dict['text_color']
        
        if self.hover:

            
            if self.width > goal_size[0]:
                
                self.width -= sizeup_speed * dt
                # self.rect.x += sizeup_speed /2
                
            if self.width < goal_size[0]:
                
                self.width += sizeup_speed *  dt
                # self.rect.x -= sizeup_speed /2
                
            if self.height > goal_size[1]:
                
                self.height -= sizeup_speed* dt 
                # self.rect.y += sizeup_speed /2
                
            if self.height < goal_size[1]:
                
                self.height += sizeup_speed* dt
                # self.rect.y -= sizeup_speed /2

            self.color = self.hover_color
            self.text_color = self.hover_text_color
            self.rect.center = self.base_pos
        
        else:
            
            goal_size = button_width_height
            
            if self.width > goal_size[0]:
                
                self.width -= sizeup_speed*dt
                # self.rect.x += sizeup_speed /2
                
            if self.width < goal_size[0]:
                
                self.width += sizeup_speed*dt
                # self.rect.x -= sizeup_speed /2
                
            if self.height > goal_size[1]:
                
                self.height -= sizeup_speed*dt
                # self.rect.y += sizeup_speed /2
                
            if self.height < goal_size[1]:
                
                self.height += sizeup_speed*dt
            self.color = self.base_color
            self.text_color = self.base_text_color
            self.rect.center = self.base_pos
        
    def update(self, *args,):
        
        self.click_execute_fun(*args)
        # self.animate(**kwargs)
        
class MultiSelect:
    
    def __init__(self, game, choices:[],topleft:(0,0),  selected_choice=0, writing_size = 16,):
        self.game =game
        self.choices = choices
        self.selected = selected_choice
        self.next_button = Button(self.game, (topleft[0] + 150,topleft[1]), self.next, 'next', text_color=(255,255,255), custom_text_offset=(-20,0))
        self.prev_button = Button(self.game, (topleft[0],topleft[1]), self.prev, 'previous', text_color=(255,255,255), custom_text_offset=(-40,0))
        self.font = med_more_font
        
        self.pos = topleft
        
    def update(self, *args):
        
        self.next_button.update(*args)
        self.prev_button.update(*args)
        
    def render(self, display:pygame.Surface, offset=(0,0), text_color=(255,255,255)):
        
        text_surf = self.font.render(self.get_choice(), False, text_color)#self.writing.write(self.get_choice(), pygame.Color(text_color))
        
        display.blit(text_surf, (self.pos[0] + 110, self.pos[1] + 10))
        self.next_button.render(display,offset)
        self.prev_button.render(display,offset)
        
    def next(self):
        
        if self.selected < len(self.choices)-1:
            self.selected += 1
        
    def prev(self):
        
        if self.selected > 0:
            self.selected -= 1
        
    def get_choice(self):
        return self.choices[self.selected]
        