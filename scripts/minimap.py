import pygame

class Minimap:

    def __init__(self, game,pos, size, ):
        self.game = game 
        
        game_display = self.game.display
        
        self.diffrence = game_display.get_width() / size[0] * (self.game.room_count[0] * 1.5)

        
        self.background = pygame.Surface(size).convert_alpha()
        
        self.size = size
        
        self.rect = self.background.get_rect(center=pos)
        
        self.pos = self.rect.center
        

        
    def feed_rooms(self, rooms):
        
        show_coloured_map = 'Compass' in self.game.player.inventory.get_tag_list()
        
        self.rooms = []
        self.rooms = rooms
        self.room_surface = self.background.copy()
        self.room_surface.fill((0,0,0, 0))
        for room in self.rooms:
            color = (255,255,255)
            if show_coloured_map:
                if room.type == 'start':
                    color = (0,255,255) 
                    
                elif room.type == 'fight':
                    color = (255,0,0)
                    
                elif room.type == 'chest':
                    color = (255,255,0)
                    
                elif room.type == 'finish':
                    color = (100,100,0)
                
            pygame.draw.rect(self.room_surface, color, 
            pygame.Rect(
                room.rect.x // self.diffrence - room.dungeon.leftest // self.diffrence, 
                room.rect.y // self.diffrence - room.dungeon.leftest // self.diffrence,
                room.rect.width // self.diffrence,
                room.rect.height// self.diffrence))
        self.room_surface.set_colorkey((0,0,0))
        
        
    def feed_hallways(self, hallways):
        
        self.hallways = hallways
        
        self.hallway_surface = pygame.Surface(self.size).convert_alpha()
        for hall in self.hallways:
            pygame.draw.rect(self.hallway_surface, (255,255,255), 
        pygame.Rect(
        hall.rect.x//self.diffrence - self.game.dungeon.leftest//self.diffrence  ,
        hall.rect.y //self.diffrence - self.game.dungeon.leftest//self.diffrence ,
        hall.rect.width // self.diffrence,
        hall.rect.height//self.diffrence)
        )
        self.hallway_surface.set_colorkey((0,0,0))
        
        self.room_surface.fblits([(self.hallway_surface, (0,0))])
            
        
    def render(self, display, player):
        self.background.fill((0,0,0, 0))

        self.background.fblits([(self.room_surface, (0,0))])
        # self.background.blit(self.hallway_surface, (-35,-35))
        player_rect = pygame.Rect(
            player.rect.x // self.diffrence- self.game.dungeon.leftest//self.diffrence,
            player.rect.y // self.diffrence- self.game.dungeon.leftest//self.diffrence,
            player.rect.width* 5 // self.diffrence,
            player.rect.height * 5 // self.diffrence)
        pygame.draw.circle(self.background, (200,0,0), player_rect.center, 1)
        pygame.draw.circle(self.background, (0,0,0), player_rect.center, 2, 1)
        # pygame.draw.circle(self.background, (0,0,0), player_rect.center, 1, 2)
       
        display.fblits([(self.background, self.pos)])