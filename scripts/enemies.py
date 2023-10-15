import pygame
from random import randint , uniform, choice

from scripts.room import Room
from scripts.settings import *
from scripts.player import Item, item_dict


class ItemDrop:
    
    def __init__(self, item, pos):
        
        self.drop= item
        self.rect = pygame.FRect(*pos, 12,12)
        self.vel = [0,-2]
        
        self.can_be_collected = False
        self.to_be_removed = False
        
    def update(self,player, dt):
        
        self.rect.y += self.vel[1] * dt
        
        self.vel[1] = pygame.math.Vector2(self.vel).move_towards((0,0), (0.01)).y  * dt
        
        if self.vel[1] == 0:
            
            self.can_be_collected = True
            
        if self.can_be_collected:
            
            if player.rect.colliderect(self.rect) and not self.to_be_removed:
                
                player.inventory.add_item(self.drop)
                
                self.to_be_removed = True

                
                
    def render(self, display, offset=(0,0)):
        
        render_rect = pygame.FRect(self.rect.x - offset[0], self.rect.y - offset[1], *self.rect.size)
        
        display.fblits([(self.drop.image, render_rect.topleft)])
            
        
        
        
        
        
        

class Enemy:
    
    def __init__(self,dungeon ,pos, room):
        self.dungeon = dungeon
        self.enemy_manager = dungeon.enemy_manager
        self.room = room
        self.rect = pygame.FRect(*pos, 30,30)
        
        self.health = randint(3, 5)
        
        self.speed = round(uniform(0.3, 1), 1)
        
        self.knockback_toughness = round(uniform(self.health/4,self.health/2), 1)
        
        red_img = pygame.Surface((32,32))
        red_img.fill((255,0,0))
        
        pwr_drop = ItemDrop(Item('powerup', 'health',red_img ), (self.rect.center))
        
        drop = choice([pwr_drop])
        
        self.drop = drop
        
        self.attacking = False
        self.dead = False
        
        self.color = (100,250,169)
        
        self.vel = [0,0]
        
    def get_player(self):
        
        self.player = self.dungeon.game.player
        
    def cap_velocity(self, max_vel):
        
        if self.vel[0] > max_vel :
            self.vel[0] = max_vel
            
        if self.vel[1] > max_vel:
            self.vel[1] = max_vel
            
        if self.vel[0] < -max_vel :
            self.vel[0] = -max_vel
            
        if self.vel[1] < -max_vel:
            self.vel[1] = -max_vel
        
    def setForce(self, vel):
        
        self.vel[0] += vel[0] / self.knockback_toughness
        self.vel[1] += vel[1] / self.knockback_toughness
        # self.move()
        
    def update(self, player,dt):
        self.dx,self.dy = 0,0
        # self.cap_velocity(6)
        if not self.dead:
            self.dx += self.vel[0]
            self.dy += self.vel[1]
            
            
            
            if player.current_room == self.room:
                direction = pygame.math.Vector2(player.rect.center) - pygame.math.Vector2(self.rect.center)
                
                if direction.length() > 0:
                    direction.normalize_ip()
                    self.vel2 = direction * self.speed
                    self.dx += self.vel2.x 
                    self.dy += self.vel2.y
            
            self.vel = list(pygame.math.Vector2(self.vel).move_towards((0,0), 1 * dt))

        
        if self.health <= 0 and not self.dead:
            
            self.drop.rect.center = self.rect.center
            self.color = (150,150,150)
            self.knockback_toughness =1
            
            self.dead = True
            
        if self.dead:
            self.dx += self.vel[0]
            self.dy += self.vel[1]
            
            if self.dungeon.game.player.lifesteal:
                
                if self.dungeon.game.player.hp < self.dungeon.game.player.max_hp:
                    
                    self.dungeon.game.player.hp += 1
            
            self.vel = list(pygame.math.Vector2(self.vel).move_towards((0,0), 1))
            
            self.drop.update(player,dt)

    def keep_in_room(self, player):
        
        room = self.room
        
        if room == player.current_room:
        
        # if room.locked:
            
            if room.top_rect.colliderect(pygame.Rect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height)):
                
                self.rect.top = room.top_rect.bottom
                
                self.dy = 0


                
            if room.bottom_rect.colliderect(pygame.Rect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height)):
                
                self.rect.bottom = room.bottom_rect.top
                
                self.dy = 0

                
            if room.left_rect.colliderect(pygame.Rect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height)):
                
                self.rect.left = room.left_rect.right
                
                self.dy = 0


                
            if room.right_rect.colliderect(pygame.Rect(self.rect.x + self.dx, self.rect.y , self.rect.width, self.rect.height)):
                
                self.rect.right = room.right_rect.left
                
                self.dy = 0

            
    def move(self, dt):
        
        try:
            self.rect.x += self.dx * dt
            self.rect.y += self.dy * dt
        except AttributeError:
            pass

        
        
        
    def render(self, display , offset, on_camera):
        render_rect = pygame.FRect(self.rect.x - offset[0], self.rect.y - offset[1], self.rect.width, self.rect.height)

        if self.room.locked and on_camera:
            
            # if render_rect.colliderect(display.get_rect()):
            pygame.draw.rect(display, self.color, render_rect)
            pygame.draw.rect(display, (0,0,0), render_rect, 3)
            
        if self.dead and on_camera:
            if not self.drop.to_be_removed:
                self.drop.render(display, offset)
    
        
class EnemyManager:
    
    def __init__(self, dungeon):
        self.dungeon = dungeon
        self.enemies = set()
        
        self.collision_rate = 150
        self.next_check_for_cols = pygame.time.get_ticks() + self.collision_rate
        
    def spawn_enemies(self):
        
            
        for room in self.dungeon.rooms:
            
            grid = self.dungeon.rooms[room]
            
            if isinstance(grid[1], Room):
                
                room = grid[1]
                
                if room.type == 'fight':
                    
                    for i in range(randint(3,7)):
                        
                        pos = grid[1].rect.center[0] + randint(-200,200), grid[1].rect.center[1] + randint(-200,200)
                        
                        self.enemies.add(Enemy(self.dungeon,pos, room))
                        
    def give_enemies_player(self):
        
        for enemy in self.enemies:
            enemy.get_player()
            print('gave plr', enemy.player.lifesteal)
                        
    def render_enemies(self, display, offset):
    
        for enemy in self.enemies:
            enemy_rect = pygame.FRect(enemy.rect.x - offset[0], enemy.rect.y - offset[1], enemy.rect.width, enemy.rect.height)
            can = display.get_rect().colliderect(enemy_rect)
            enemy.render(display, offset, can)
            
    def get_enemies_by_room(self, room):
        enemies = []
        for enemy in self.enemies:
            
            if enemy.room== room and not enemy.dead:
                enemies.append(enemy)
                
        return enemies
                
            
    def update_enemies(self, player, dt):
        
        
        for enemy in self.enemies:
            
            if enemy.room == player.current_room:
                enemy.update(player,dt)

                
                
    def keep_enemies_in(self, player):
        for enemy in self.enemies:
            
            enemy.keep_in_room(player)
        
                
    def move_enemies(self, dt):
        for enemy in self.enemies:
            
            enemy.move(dt)
        
            
        
        
        