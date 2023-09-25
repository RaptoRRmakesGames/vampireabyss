import pygame 
from random import *

from scripts.room import Room
from scripts.settings import *
# from scripts.writing import Writing
from scripts.player import item_dict
from scripts.font_inits import *

powerups = ['idk what this does']
class Chest:
    
    def __init__(self, room):
        self.contents = [choice([powerups])]
        self.room = room
        self.width, self.height = 75, 50
        self.rect = pygame.FRect(self.room.rect.center[0] - self.width, self.room.rect.center[1] - self.height, self.width, self.height)
        self.render_rect = self.rect
        
        self.opened = False
        
    def render(self, display, offset=(0,0)):
        
        self.render_rect = pygame.FRect(self.rect.center[0] - offset[0], self.rect.center[1] - offset[1], self.width, self.height)
        
        pygame.draw.rect(display, (255,255,0), self.render_rect)
        pygame.draw.rect(display, (139,69,19), self.render_rect, 3)

class ChestManager:
    
    def __init__(self, dungeon):
        self.dungeon = dungeon
        self.chests= set()
        
    def spawn_chests(self):
        
        for room in self.dungeon.rooms:
            
            grid = self.dungeon.rooms[room]
            
            if isinstance(grid[1], Room):
                
                room = grid[1]
                
                if room.type == 'chest':
                    
                    self.chests.add(Chest(room))
        
    def render_chests(self, display, offset):
        
        for chest in self.chests:
            
            render_rect = pygame.FRect(chest.rect.center[0] - offset[0], chest.rect.center[1] - offset[1], chest.width, chest.height)
            
            if display.get_rect().colliderect(render_rect):
                chest.render(display, offset)
            
    def update_chests(self, player):
        
        for chest in self.chests:
            
            if pygame.math.Vector2(chest.rect.center).distance_to(pygame.math.Vector2(player.rect.center)) < 100:
                

                if pygame.key.get_pressed()[pygame.K_e] and not chest.opened:
                    
     
                    
                    self.dungeon.powerup_manager.spawn_powerup(chest)

                    chest.opened = True

class PowerUpBase:
    
    def __init__(self, color, chest):
        self.to_be_removed = False
        self.color = color
        self.type = type 
        self.chest = chest 
        
        self.just_spawned = True
        
        self.velocity = pygame.math.Vector2(0,3)
        
        self.player_powers = self.chest.room.dungeon.game.player.power_adds
        self.base_player_powers = self.chest.room.dungeon.game.player.base_powers
        self.refresh_player_powers = self.chest.room.dungeon.game.player.refresh_powers
        self.player = self.chest.room.dungeon.game.player
        
        self.rect = pygame.FRect(self.chest.rect.x + 65, self.chest.rect.y + 30, 15,15)
        self.render_rect = self.rect
        
    def update(self, dt):
        
        self.velocity = self.velocity.move_towards((0,0), 0.01)
        
        self.rect.y += self.velocity.y * dt
        
        if self.velocity.y == 0:
            
            self.just_spawned = False
            
    def round_player_buffs(self):
        
        for buff in list(self.player_powers.keys()):
            self.player_powers[buff] = round(self.player_powers[buff], 2)
        
        
    def render(self, display, offset=(0,0)):
        
        self.render_rect = pygame.FRect(self.rect.x - offset[0], self.rect.y - offset[1], self.rect.width, self.rect.height)
        
        pygame.draw.rect(display, self.color, self.render_rect)
        
class SpeedUp(PowerUpBase):
    
    def __init__(self,   chest):
        super().__init__((255,255,0), chest)
        self.explanation = 'Speed Up: Increase the players speed by 10% (stacks)'
        
    def do_effect_and_die(self):
        
        self.player_powers['speed'] += self.base_player_powers['speed'] / 15
        self.refresh_player_powers()
        
        c = randint(15*coin_multi, 23*coin_multi)
        self.player.coins += c

        self.round_player_buffs()
        
class StrenghtUp(PowerUpBase):
    
    def __init__(self,   chest):
        super().__init__((255,0,0),  chest)
        self.explanation = 'Strenght Buff: Increases the players strength by 15% (stacks)'
        
    def do_effect_and_die(self):
        
        self.player_powers['damage'] += self.base_player_powers['damage'] / 30
        self.refresh_player_powers()
        c = randint(15*coin_multi, 23*coin_multi)
        self.player.coins += c
        self.round_player_buffs()
        
class Compass(PowerUpBase):
    
    def __init__(self,   chest):
        super().__init__((255,0,0),  chest)
        self.explanation = 'Strenght Buff: Increases the players strength by 15% (stacks)'
        
    def do_effect_and_die(self):
        
        self.player.inventory.add_item(item_dict['compass'])
class Spoon(PowerUpBase):
    
    def __init__(self,   chest):
        super().__init__((255,0,0),  chest)
        self.explanation = 'Strenght Buff: Increases the players strength by 15% (stacks)'
        
    def do_effect_and_die(self):
        
        self.player.inventory.add_item(item_dict['spoon'])

class Vial(PowerUpBase):
    
    def __init__(self,   chest):
        super().__init__((255,0,0),  chest)
        self.explanation = 'Strenght Buff: Increases the players strength by 15% (stacks)'
        
    def do_effect_and_die(self):
        
        self.player.inventory.add_item(item_dict['vial'])
class Fangs(PowerUpBase):
    
    def __init__(self,   chest):
        super().__init__((255,0,0),  chest)
        self.explanation = 'Strenght Buff: Increases the players strength by 15% (stacks)'
        
    def do_effect_and_die(self):
        
        self.player.inventory.add_item(item_dict['fang_extendors'])
class PowerupManager:
    
    def __init__(self, dungeon):
        
        self.dungeon = dungeon
        
        
        self.powerup_types = {"speedup":SpeedUp, 'damage':StrenghtUp, 'compass' : Compass, 'spoon' : Spoon, 'vial' : Vial, 'fangs': Fangs}
        self.powerups = []
        
    def spawn_powerup(self, chest):
        
        self.powerups.append(self.powerup_types  [choice( list(self.powerup_types.keys()) )]   (chest) )
        
    def update_powerups(self, dt, player):
        
        for powerup in self.powerups:
            
            powerup.update(dt)
            
            if powerup.rect.colliderect(player.rect) and not powerup.just_spawned:
                
                powerup.do_effect_and_die()

                self.powerups.remove(powerup)
            
    def render_powerups(self, display, offset):
        
        for powerup in self.powerups:
            
            powerup.render(display, offset)

class NextLevelBlock:
        
    def __init__(self, room):
        
        self.width, self.height = (150,150)
        
        self.rect = pygame.Rect(room.rect.center[0] - self.width //2, room.rect.center[1] - self.height //2, self.width, self.height)
        self.render_rect = pygame.Rect(0,0,0,0)
        
        
        self.writing = huge_font#Writing(32)
        
    def render(self, display, offset=(0,0)):
        
        self.render_rect = pygame.Rect(self.rect.x-offset[0],self.rect.y-offset[1],self.width, self.height)
        
        pygame.draw.rect(display, (255,255,255), self.render_rect)
        
        display.blit(self.writing.render('Next', False, (0,0,0)), (self.render_rect.centerx - self.width//2 + 6, self.render_rect.centery - self.height//2 + 23))
        display.blit(self.writing.render('Level', False, (0,0,0)), (self.render_rect.centerx - self.width//2 + 6, self.render_rect.centery - self.height//2 + 78))
        