import pygame 
from random import choice

from scripts.room import Room, BlankRoom, Hallway
from scripts.settings import *
from scripts.enemies import EnemyManager
from scripts.loot import Chest, ChestManager, PowerupManager
from scripts.loot import NextLevelBlock
from scripts.writing import room_writing
from scripts.utils import create_room_img

from time import time

class Dungeon:
    
    def __init__(self,game ,width, height, level):
        self.leftest = -(width / 2) * ROOM_SIZE
        self.room_distance = 250
        
        self.level = level

        
        self.game = game
        
        self.width = width
        self.height = height
        
        self.enemy_manager = EnemyManager(self)
        self.chest_manager = ChestManager(self)
        self.powerup_manager = PowerupManager(self)
        
        self.hallways = []
        self.rooms = {'{};{}'.format(i, y): [(self.leftest + ((ROOM_SIZE + self.room_distance) * i), self.leftest + ((ROOM_SIZE + self.room_distance) * y)), BlankRoom(((self.leftest + ((ROOM_SIZE + self.room_distance) * i)), self.leftest + ((ROOM_SIZE + self.room_distance) * y)), self, "{};{}".format(i, y))]
                      for i in range(width+ 1) for y in range(height + 1)}
        self.generate_rooms()
        
        self.enemy_manager.spawn_enemies()
        
        self.chest_manager.spawn_chests()
        self.next_level_block = NextLevelBlock(self.finish_room)
        
    
        
    def update_level_block(self, player):
        
        if self.next_level_block.rect.colliderect(player.rect):
            
            return 'refresh'
        
    def render_level_block(self, display, offset):
        
        self.next_level_block.render(display, offset)

    def generate_rooms(self):

        set_finish = False
        finish_inside = False

        
        while not finish_inside:
            choices = ['fight','fight', 'chest', 'empty', 'empty']
            
            middle_room = f'{self.width // 2};{self.height // 2}'
            self.rooms[middle_room][1] = Room(self.rooms[middle_room][0], 'start', self, middle_room, create_room_img())
            self.middle_room_pos = self.rooms[middle_room][1].rect.center
            self.middle_room = self.rooms[middle_room][1]
            
            for x in range(3):
            
                coord_x = int(f'{self.width // 2};{self.height // 2}'.split(';')[0])
                coord_y = int(f'{self.width // 2};{self.height // 2}'.split(';')[1])
                
                for i in range(10): 
                
                    what = choice(['up', 'down', 'left', 'right'])
                    
                    if what == 'up' and coord_y > 1:
                        coord_y -= 1
                        htype = 'v'
                        
                    if what == 'down' and coord_y < self.height - 2:
                        coord_y += 1
                        htype = 'v'
                    if what == 'left' and coord_x > 1:
                        coord_x -= 1
                        htype = 'h'
                    if what == 'right' and coord_x < self.width - 2:
                        coord_x += 1
                        htype = 'h'
                        
                    str_cord = f'{coord_x};{coord_y}'
                    
                    if isinstance(self.rooms[str_cord][1], BlankRoom):
                        if i < 3 or set_finish:
                            room_choice = choice(choices)

                            self.rooms[str_cord][1] = Room(self.rooms[str_cord][0], room_choice, self,f"{coord_x};{coord_y}", create_room_img())
                        else:
                            set_finish = True
                            self.rooms[str_cord][1] = Room(self.rooms[str_cord][0], 'finish', self,f"{coord_x};{coord_y}", create_room_img())
                            self.finish_room = self.rooms[str_cord][1]
                            
                        newroom = self.rooms[str_cord][1]
                            
                        if htype == 'h':
                            if what=='left':
                                self.hallways.append(Hallway((newroom.rect.right, newroom.rect.y + ROOM_SIZE//2 - 60),self, htype, what))
                            if what=='right':
                                self.hallways.append(Hallway((newroom.rect.left - self.room_distance,newroom.rect.y + ROOM_SIZE//2  -60),self, htype, what))
                        if htype == 'v':
                            if what=='up':
                                self.hallways.append(Hallway((newroom.rect.x + ROOM_SIZE//2 - 60, newroom.rect.bottom),self, htype, what))
                            if what=='down':
                                self.hallways.append(Hallway((newroom.rect.x + ROOM_SIZE//2 - 60, newroom.rect.top - self.room_distance),self, htype, what))
                                
            room_list = self.get_room_list()
            
            finish_inside = False
            for room in room_list:
                if room.type == 'finish':
                    finish_inside = True 
                    break
                
        if not finish_inside:
            self.generate_rooms()
            
    def render_hallways(self, display, offset):
        for hallway in self.hallways:
            render_rect = pygame.FRect(hallway.rect.x - offset[0], hallway.rect.y - offset[1], hallway.rect.width, hallway.rect.height)  
            if display.get_rect().colliderect(render_rect):
            
                hallway.render(display, offset)
            
    def update_hallways(self, player):
        hallways = []
        
        for hallway in self.hallways:
            
            hallways.append((hallway, pygame.math.Vector2(hallway.rect.center).distance_to(pygame.math.Vector2(player.rect.center)), ))
            
        sorted_hallways = sorted(hallways, key=lambda x: x[1])
        
        player.curent_hallway = sorted_hallways[0][0] if sorted_hallways[0][1] < 300 else None

           
    def get_room_list(self):
        roomlist = []
        for roomekey in self.rooms:
            
            grid = self.rooms[roomekey]
            
            if isinstance(grid[1], Room):
                
                roomlist.append(grid[1])
                
        return roomlist
        
    def render_rooms(self, display: pygame.Surface, offset=(0,0)):
        room_poses= []
        for room in self.rooms:
            
            
            grid = self.rooms[room]
            
            if isinstance(grid[1], Room):
     
                
                render_rect = pygame.FRect(grid[1].rect.x - offset[0], grid[1].rect.y - offset[1], grid[1].rect.width, grid[1].rect.height)   
                
                if display.get_rect().colliderect(pygame.FRect(render_rect.x - 16, render_rect.y - 16, ROOM_SIZE + 32, ROOM_SIZE + 32)):
                    
                    room_poses.append((grid[1].image, (render_rect.x - 16, render_rect.y - 16)))
                    # grid[1].render(display, offset)
                    
        display.blits(room_poses)
                    
        # display.blit(room_writing.write(f'level: {self.level}', pygame.Color(255,255,255)), (self.middle_room_pos[0] - offset[0] - 40, self.middle_room_pos[1] - offset[1] - 8))
                    
    def update_rooms(self):
                 
        plr = self.game.player
        
        for room in list(self.rooms.keys()):
            
            
            roo = self.rooms[room][1]
            
            if not isinstance(roo, BlankRoom):
                roo.has_player = False
                if plr.rect.colliderect(roo.rect):
                    
                    plr.current_room = roo
                    roo.has_player = True
                    
                    if roo.type == 'fight' :
                        if plr.rect.colliderect(roo.check_player_in_rect) and not roo.locked:
                            roo.locked = True
                        
                        if roo.locked and len(self.enemy_manager.get_enemies_by_room(roo)) < 1:
                            
                            roo.locked = False
                        # roo.locked = False
                        

                                         
    def render_enemies(self, display, offset=(0,0)):
        
        self.enemy_manager.render_enemies(display, offset)
        
    def update_enemies(self, player, dt):
        
        self.enemy_manager.update_enemies(player, dt)
        
    def move_enemies(self, dt):
        
        self.enemy_manager.move_enemies(dt)
   
    def copy(self):
       return Dungeon(self.game, self.width, self.height, self.level + 1)



if __name__ == '__main__':
    d = Dungeon(5,5)