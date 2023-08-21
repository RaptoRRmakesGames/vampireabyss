import pygame 

from random import randint

class Hitbox:
    
    def __init__(self, rect_values, ori, damage):
        
        self.rect = pygame.FRect(*rect_values)
        
        self.ori = ori
        
        self.damage = damage
        
        self.hit_sprites = []
        
    def render(self, display, offset):
        
        render_rect = pygame.FRect(self.rect.x - offset[0], self.rect.y - offset[1], self.rect.width, self.rect.height)
        
        pygame.draw.rect(display, (255,0,0), render_rect)
        
class CombatSystem:
    
    def __init__(self, game):
        self.game = game 
        
    def update(self):
        
        enemies = self.game.dungeon.enemy_manager.enemies
        player_hitboxes = self.game.player.hitboxes
        
        
        for enemy in enemies:
            for hitbox in player_hitboxes:
                if enemy.rect.colliderect(hitbox.rect) and not enemy in hitbox.hit_sprites:
                    enemy.health -= hitbox.damage
                    knock_back_strenght = randint(14,20)
                    knock_back_sideoff = randint(3, 7)
                    match hitbox.ori :
                        case 'up':
                            vel = (knock_back_sideoff, -knock_back_strenght)
                            
                            # print('eh')
                            
                        case 'down':
                            vel = (knock_back_sideoff, knock_back_strenght)
                            # print('eh')
                            
                        case 'left':
                            vel = (-knock_back_strenght,knock_back_sideoff)
                            # print('eh')
                            
                        case 'right':
                            vel = (knock_back_strenght,knock_back_sideoff)
                            # print('eh')
                            
                    enemy.setForce(vel)
                            
                    hitbox.hit_sprites.append(enemy)
                    # print('hit')
            
            
        