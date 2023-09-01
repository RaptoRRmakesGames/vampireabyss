import pygame

class Minimap:

    def __init__(self, game,pos, size, ):
        self.game = game 
        
        game_display = self.game.display
        
        self.diffrence_x, self.diffrence_y = (game_display.get_width() / size[0]) * 15,( game_display.get_height() / size[1]) * 15
        
        self.background = pygame.Surface(size).convert()
        self.bcg_with_color = self.background.copy()
        self.bcg_with_color.fill((15,25,100))
        
        self.size = size[0] * 1, size[1]*1
        
        self.pos = pos
        
        
    def feed_rooms(self, rooms):
        self.rooms = []
        self.rooms = rooms
        self.room_surface = pygame.Surface(self.size).convert_alpha()
        for room in self.rooms:
            color = (255,255,255)
            if room.type == 'start':
                color = (0,255,255)
                
            elif room.type == 'fight':
                color = (255,0,0)
                
            elif room.type == 'chest':
                color = (255,255,0)
                
            elif room.type == 'finish':
                color = (100,100,0)
                
            pygame.draw.rect(self.room_surface, color, pygame.Rect(room.rect.x//self.diffrence_x - self.game.dungeon.leftest//self.diffrence_x + 410 //self.diffrence_x, room.rect.y //self.diffrence_x - self.game.dungeon.leftest//self.diffrence_x + 400 //self.diffrence_x, room.rect.width // self.diffrence_x,room.rect.height//self.diffrence_x))
        self.room_surface.set_colorkey((0,0,0))
        
    def feed_hallways(self, hallways):
        
        self.hallways = hallways
        
        self.hallway_surface = pygame.Surface(self.size).convert_alpha()
        for hall in self.hallways:
            pygame.draw.rect(self.hallway_surface, (255,255,255), pygame.Rect(hall.rect.x//self.diffrence_x - self.game.dungeon.leftest//self.diffrence_x + 410 //self.diffrence_x, hall.rect.y //self.diffrence_x - self.game.dungeon.leftest//self.diffrence_x + 400 //self.diffrence_x, hall.rect.width // self.diffrence_x,hall.rect.height//self.diffrence_x))
        self.hallway_surface.set_colorkey((0,0,0))
        
        self.room_surface.blit(self.hallway_surface, (0,0))
            
        
    def render(self, display, player):
        self.background = self.bcg_with_color.copy()

        self.background.blit(self.room_surface, (0,0))
        # self.background.blit(self.hallway_surface, (-35,-35))
        player_rect = pygame.Rect(
            player.rect.x // self.diffrence_x - self.game.dungeon.leftest//self.diffrence_x + 400  // self.diffrence_x ,
            player.rect.y // self.diffrence_x - self.game.dungeon.leftest//self.diffrence_x + 400 //self.diffrence_x + 35,
            player.rect.width* 5 // self.diffrence_x,
            player.rect.height * 5 // self.diffrence_x - 70)
        pygame.draw.circle(self.background, (0,250,150), player_rect.center, 1)
        pygame.draw.circle(self.background, (0,0,0), player_rect.center, 1, 2)
       
        display.blit(self.background, self.pos)