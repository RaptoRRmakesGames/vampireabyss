import pygame 

pygame.display.set_mode((1280, 920))

from scripts.settings import *
from scripts.writing import room_writing

class Hallway:
    
    def  __init__(self, pos, dungeon, type, ori):
        
        self.height = 120
        if type == 'h':
            self.rect = pygame.Rect(*pos, dungeon.room_distance, self.height)     
        if type == 'v':  
            self.rect = pygame.Rect(*pos,  self.height, dungeon.room_distance,) 
            
        self.type = type 
        self.ori = ori
        self.render_rect = pygame.Rect(0,0,0,0)

    def render(self, display, offset):
        
        
        self.render_rect = pygame.Rect(self.rect.x - offset[0], self.rect.y - offset[1], self.rect.width, self.rect.height)
        if display.get_rect().colliderect(self.render_rect):
            pygame.draw.rect(display, (100,100,100), self.render_rect) 
            # pygame.draw.rect(display, (255,255,255), render_rect, 5) 

            # display.blit(room_writing.write(self.ori, pygame.Color(255,255,255)), (self.render_rect.centerx - 30, self.render_rect.centery - 30))


class Room:
    
    def __init__(self, topleft, type, dungeon, cord):
        
        self.rect = pygame.FRect(topleft[0], topleft[1], ROOM_SIZE, ROOM_SIZE,)
        
        self.type = type 
        
        self.cords = cord
        
        self.dungeon = dungeon
        
        self.locked = False
        
        self.has_player = False
        self.top_rect = pygame.FRect(self.rect.x, self.rect.y - 20, ROOM_SIZE, 20)
        self.left_rect = pygame.FRect(self.rect.x - 20, self.rect.y , 20, ROOM_SIZE)
        self.right_rect= pygame.FRect(self.rect.x + ROOM_SIZE, self.rect.y, 20, ROOM_SIZE)
        self.bottom_rect= pygame.FRect(self.rect.x , self.rect.y + ROOM_SIZE, ROOM_SIZE, 20)
        
        self.outer_rects = [self.top_rect, self.left_rect, self.right_rect, self.bottom_rect]
        

        if self.type == 'fight':
            self.check_player_in_rect = pygame.FRect(0,0,ROOM_SIZE -50, ROOM_SIZE-50)
            self.check_player_in_rect.center = self.rect.center
            

        
        
    def render(self, display, offset=(0,0)):
        render_rect = pygame.FRect(self.rect.x - offset[0], self.rect.y - offset[1], self.rect.width, self.rect.height)     
        

        pygame.draw.rect(display, (40,40,40), render_rect,)
        # display.blit(room_writing.write(str(self.has_player), pygame.Color(255,255,255)),( self.rect.center[0] - offset[0], self.rect.center[1] - offset[1]))
        
        
        # if self.type == 'fight':
        #     render_rect = pygame.FRect(self.check_player_in_rect.x - offset[0], self.check_player_in_rect.y - offset[1], self.check_player_in_rect.width, self.check_player_in_rect.height)     
            
                

        #     pygame.draw.rect(display, (0,100,100), render_rect,)
        #     for rect in self.outer_rects:
        #         render_rect = pygame.FRect(rect.x - offset[0], rect.y - offset[1], rect.width, rect.height)     
        #         pygame.draw.rect(display, (255,255,100), render_rect,)
            
    
class BlankRoom:
    
    
    def __init__(self, topleft, dungeon, cord):
        self.dungeon = dungeon
        
        self.cords = cord
        
        self.rect = pygame.FRect(topleft[0] - self.dungeon.room_distance, topleft[1] - self.dungeon.room_distance, ROOM_SIZE + self.dungeon.room_distance * 2, ROOM_SIZE + self.dungeon.room_distance *2,)
        