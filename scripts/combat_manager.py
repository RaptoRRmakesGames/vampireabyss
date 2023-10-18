import pygame 

from random import randint

class Hitbox:
    
    def __init__(self, rect_values, ori, damage, time_to_be_removed=False, special_tags = []):
        
        self.rect = pygame.FRect(*rect_values)
        
        self.ori = ori
        
        self.damage = damage
        
        self.tags = special_tags
        
        self.hit_sprites = []
        
        self.die_time = pygame.time.get_ticks() + time_to_be_removed if time_to_be_removed != False else 'stayforever'
        self.be_removed = False
        
    def update(self):
        if self.die_time != 'stayforever':
            
            if pygame.time.get_ticks()> self.die_time:
                self.be_removed = True
            
        
        
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

                            
                        case 'down':
                            vel = (knock_back_sideoff, knock_back_strenght)

                            
                        case 'left':
                            vel = (-knock_back_strenght,knock_back_sideoff)

                            
                        case 'right':
                            vel = (knock_back_strenght,knock_back_sideoff)

                            
                    if not 'no_kb' in hitbox.tags:
                        enemy.setForce(vel)
                            
                    hitbox.hit_sprites.append(enemy)

            
        