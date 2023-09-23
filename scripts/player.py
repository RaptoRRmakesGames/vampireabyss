
import pygame 
from random import randint, choice

from scripts.combat_manager import Hitbox
from scripts.writing import Writing
from scripts.settings import coin_multi
from scripts.animations import Animation, Animator



class Item:
    
    def __init__(self, tag, name, img: pygame.Surface, stack_size=-1):
        
        self.tag = tag 
        self.name = name 
        self.image = img
        self.rect = pygame.Rect(0,0, 36,36)
        
        self.stack_size = stack_size
        
    def list(self):
        
        return  '{}, {}'.format(self.tag, self.name)
        
    def __str__(self):
        
        return '{}, {}'.format(self.tag, self.name)
    
item_dict = {
    'compass' : Item('util', 'Compass', pygame.image.load('assets/images/icons/compass.png').convert_alpha()),
}

class Inventory:
    
    def __init__(self, player):
        
        self.player = player
        
        self.items = {}
        self.rendered_dict = {}

        self.open = False
        
        self.rect = pygame.FRect(60,400, 500, 75)
        
        self.max_y = 400
        self.least_y = 300
        
        self.item_positions = [(self.rect.center[0] - self.rect.width//2 + 47 +(50* i), self.least_y+20 ) for i in range(1, 7)]
        
        self.vel = 0
        
        self.writing = Writing(10)
        
        self.selected_item=  None
        
        self.weapon_surf = pygame.Surface((32,32)).convert_alpha()
        self.weapon_surf.fill((150,255,255))
        
        self.util_surf = pygame.Surface((32,32)).convert_alpha()
        self.util_surf.fill((255,255,150))
        
        self.test_surf = pygame.Surface((32,32)).convert_alpha()
        self.test_surf.fill((255,255,255))
        
        self.item_background_colors = {
            
            'weapon' : self.weapon_surf,
            'util' : self.util_surf,
            'test': self.test_surf
            
        }
        
        
        
        self.clicked = False
        
        self.slot_binds = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]
        
    def get_tag_list(self):
        
        return list(self.items.keys())
    
    def remove_item(self, itemname, count=1):
        
        
        
        if len(self.items[itemname]) == 1:
        
            self.items[itemname].pop(0)
            
            del self.items[itemname]
            
            self.refresh_stuff()
            
            self.affect_player()
            
            self.selected_item = None
            
            return 
        
        self.items[itemname].pop(0)
        self.affect_player()
            
        
    def add_item(self, item):
        
        if len(self.items.keys()) < 10 or item.name in self.get_tag_list():
        
            if item.tag == 'powerup':
                
                
                if item.name == 'maxhealth':
                    

                    
                    self.player.max_hp += 1
                    
                    self.player.hp += 1
                    
                    return
                
                if item.name == 'health':
                    
                    
                    if self.player.hp < self.player.max_hp:
                        self.player.hp += 1
                        return
                    
                    self.player.coins += randint(17*coin_multi,23*coin_multi)
                    
                    return

            if item.name in list(self.items.keys()):
                if len(self.items[item.name]) -1 < item.stack_size:
                
                    self.items[item.name].append(item)
        
            else:
                self.items[item.name] = []
                self.items[item.name].append(item)
                
            self.refresh_stuff()
            self.affect_player()
            
    def refresh_stuff(self):
        
        self.rendered_dict = {}
        
        for itemkey in list(self.items.keys()):
            
            items = self.items[itemkey]
            
            for item in items:
                if itemkey in list(self.rendered_dict.keys()):
                    self.rendered_dict[itemkey][1] += 1

                else:

                    self.rendered_dict[itemkey] = {}
                    self.rendered_dict[itemkey] = [item, 1]
                    
    def update(self, dt):
        
        if self.player.game.time == 25:
            dt *= 4
        
        
        
        self.rect.y += self.vel * dt
        if self.open: 

            self.vel -= 0.3
            
            if self.rect.y < self.least_y:
                
                self.rect.y = self.least_y
                self.vel  =0 
            
        else:

            self.vel += 0.3
            
            if self.rect.y > self.max_y:
                
                self.rect.y = self.max_y
                
                self.vel = 0 
                

                    
    def render(self, display):
        
        if display.get_rect().colliderect(self.rect):
            
            pygame.draw.rect(display, (100,100,100), self.rect)
            pygame.draw.rect(display, (0,0,0), self.rect, 5)
            
            for x, itemkey in enumerate(list(self.rendered_dict.keys())):
                
                
                item_list = self.rendered_dict[itemkey]
                
                item_count = item_list[1]
                
                
                pos = [self.item_positions[x][0] , self.item_positions[x][1]  -( self.max_y- self.rect.y - 90  if self.open else self.least_y - self.rect.y - 90)]

                display.blit(self.item_background_colors[item_list[0].tag], (pos))

                display.blit(item_list[0].image, (pos[0] , pos[1] ))
                
                text = self.writing.write(str(item_count), pygame.Color(255,255,255))
                
                text_rect = text.get_rect(bottomleft = item_list[0].image.get_rect(topleft=  pos).bottomleft)
                
                display.blit(text, text_rect.topleft) if item_count > 1 else 0
                
                if self.selected_item and item_list[0].name == self.selected_item.name:
                    
                    pygame.draw.circle(display, (255,255,255), (pos[0] + 15, pos[1] + 15), 20, 5)
                    
                col_rect = pygame.Rect(*pos, item_list[0].image.get_rect().width, item_list[0].image.get_rect().height)
                
                if col_rect.collidepoint(pygame.mouse.get_pos()):
                    
                    if pygame.mouse.get_pressed()[0] and not self.clicked:
                        
                        self.selected_item = item_list[0] if self.selected_item != item_list[0] else None
                        
                        self.clicked = True
                        
                if not pygame.mouse.get_pressed()[0]:
                    
                    self.clicked = False
                    
                
    def affect_player(self):
        
        # self.player.game.minimap.show_coloured_map = False
        
        self.player.game.minimap.feed_rooms(self.player.game.dungeon.get_room_list())
        self.player.game.minimap.feed_hallways(self.player.game.dungeon.hallways)
        for item in list(self.items.values()):
            item = item[0]
                
                

                

class Player:
    
    def __init__(self, pos, speed, start_room, game):
        
        self.rect = pygame.FRect(*pos, 24,24)
        self.velocity = pygame.math.Vector2(0,0)
        self.speed = speed
        
        self.game = game
        
        self.last_ori = 'up'
        self.ori = 'up'
        self.state = 'regular'
        
        self.rect.center = pos
        
        self.attacking = False
        self.can_attack = True
        self.hitboxes = []
        
        self.current_room = start_room
        self.curent_hallway = None
        
        self.coins = 0
        self.damage = 1
        self.powers = {'speed': 1, 'damage' : 1,'dash_strength' : 1 }
        self.base_powers = {'speed': 1, 'damage' : 1,'dash_strength' : 1 }
        
        self.hp = 3
        self.max_hp = 3
        
        self.stop_interval = 50
        self.stop_attack_time = pygame.time.get_ticks() + self.stop_interval
    
        self.attack_interval = 250
        self.next_attack = pygame.time.get_ticks() + self.attack_interval
        
        self.go_left = range(-45,45)
        self.go_right = list(range(135,180)) +  list(range(-180,-135))
        self.go_down = range(-135,-45)
        self.go_up = range(45, 135)
        
        
        
        self.inventory = Inventory(self)
        
        
        self.animator = Animator(
            
            {
                'idle_up' : Animation(self.game.assets['player']['idle']['up'],), 
                'idle_down' : Animation(self.game.assets['player']['idle']['down'],), 
                'idle_left' : Animation(self.game.assets['player']['idle']['left'],), 
                'idle_right' : Animation(self.game.assets['player']['idle']['right'],), 
                
                
                'run_up' : Animation(self.game.assets['player']['run']['up'],), 
                'run_down' : Animation(self.game.assets['player']['run']['down'],), 
                'run_left' : Animation(self.game.assets['player']['run']['left'],), 
                'run_right' : Animation(self.game.assets['player']['run']['right'],), 
                
                
                'punch_up_left' : Animation(self.game.assets['player']['punch_left']['up'],30), 
                'punch_down_left' : Animation(self.game.assets['player']['punch_left']['down'],30), 
                'punch_left_left' : Animation(self.game.assets['player']['punch_left']['left'],30), 
                'punch_right_left' : Animation(self.game.assets['player']['punch_left']['right'],30), 
                
                'punch_up_right' : Animation(self.game.assets['player']['punch_right']['up'],30), 
                'punch_down_right' : Animation(self.game.assets['player']['punch_right']['down'],30), 
                'punch_left_right' : Animation(self.game.assets['player']['punch_right']['left'],30), 
                'punch_right_right' : Animation(self.game.assets['player']['punch_right']['right'],30), 
                
                'bigpunch_up_left' : Animation(self.game.assets['player']['big_punch_left']['up'],60), 
                'bigpunch_down_left' : Animation(self.game.assets['player']['big_punch_left']['down'],60), 
                'bigpunch_left_left' : Animation(self.game.assets['player']['big_punch_left']['left'],60), 
                'bigpunch_right_left' : Animation(self.game.assets['player']['big_punch_left']['right'],60), 
                
                'bigpunch_up_right' : Animation(self.game.assets['player']['big_punch_right']['up'],60), 
                'bigpunch_down_right' : Animation(self.game.assets['player']['big_punch_right']['down'],60), 
                'bigpunch_left_right' : Animation(self.game.assets['player']['big_punch_right']['left'],60), 
                'bigpunch_right_right' : Animation(self.game.assets['player']['big_punch_right']['right'],60), 
                
            },'idle'+'_'+self.ori)
        
        self.dx, self.dy = 0,0
        self.last_attack_turn = 'left'
        
        self.image = self.animator.get_image()
        
        self.dash_strength = 9
        self.can_dash = True
        self.dash = False
        self.stop_dash_time = 150
        self.next_stop_dash = pygame.time.get_ticks() + self.stop_dash_time
        
        self.dash_timer = 2000
        self.time_till_next_dash = pygame.time.get_ticks() + self.dash_timer
        
    def dashing(self):
        
        k = pygame.key.get_pressed()
        
        if k[pygame.K_LSHIFT] and self.can_dash and not self.dash:
            
            self.dash = True 
            self.next_stop_dash = pygame.time.get_ticks() + self.stop_dash_time
            self.can_dash = False
            
        if self.dash and pygame.time.get_ticks() > self.next_stop_dash:
            
            self.dash = False
            self.time_till_next_dash = pygame.time.get_ticks() + self.dash_timer
            
        if pygame.time.get_ticks() > self.time_till_next_dash and not self.can_dash and not k[pygame.K_LSHIFT]:
            
            self.can_dash = True
            
    def normalise_speed(self):
        
        try:
            self.dx, self.dy = pygame.math.Vector2(self.dx, self.dy).normalize()
            #self.velocity = self.velocity.normalize()
        except ValueError:
            
            return
        
    def keep_in_locked_room(self):
        
        room = self.current_room
        
        if room.locked:
            
            if room.top_rect.colliderect(pygame.Rect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height)):
                
                self.rect.top = room.top_rect.bottom
                
                self.dy = 0
                self.velocity.y = 0
                
            if room.bottom_rect.colliderect(pygame.Rect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height)):
                
                self.rect.bottom = room.bottom_rect.top
                
                self.dy = 0
                self.velocity.y = 0
                
            if room.left_rect.colliderect(pygame.Rect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height)):
                
                self.rect.left = room.left_rect.right
                
                self.dy = 0
                self.velocity.y = 0
                
            if room.right_rect.colliderect(pygame.Rect(self.rect.x + self.dx, self.rect.y , self.rect.width, self.rect.height)):
                
                self.rect.right = room.right_rect.left
                
                self.dy = 0
                self.velocity.y = 0
    
    def keep_in_hallway(self, display=pygame.Surface((0,0)), offset=[0,0]):
        if self.curent_hallway:
            
            if self.curent_hallway.type == 'h':
                
                toprect = pygame.Rect(self.curent_hallway.rect.x, self.curent_hallway.rect.y - self.curent_hallway.height - 60, self.curent_hallway.rect.width, self.curent_hallway.rect.height+60 ,)
                
                    
                if toprect.colliderect(pygame.Rect(self.rect.x  + self.dx , self.rect.y  , self.rect.width, self.rect.height)):
                    
                    
                    if self.dx > 0:
                        
                        self.rect.right = toprect.left
                            
                        self.dx = 0
                        self.velocity.x = 0
                    if self.dx < 0:
                        
                        self.rect.left = toprect.right
                            
                        self.dx = 0
                        self.velocity.x = 0
                    
                elif toprect.colliderect(pygame.Rect(self.rect.x  , self.rect.y + self.dy , self.rect.width, self.rect.height)):
                    
                    self.rect.top = toprect.bottom
                        
                    self.dy = 0
                    self.velocity.y = 0

                bottom = pygame.Rect(self.curent_hallway.rect.x, self.curent_hallway.rect.y + self.curent_hallway.height , self.curent_hallway.rect.width, self.curent_hallway.rect.height + 60,)
                
                if bottom.colliderect(pygame.Rect(self.rect.x  + self.dx , self.rect.y  , self.rect.width, self.rect.height)):
                    
                    
                    if self.dx > 0:
                        
                        self.rect.right = bottom.left
                            
                        self.dx = 0
                        self.velocity.x = 0
                    if self.dx < 0:
                        
                        self.rect.left = bottom.right
                            
                        self.dx = 0
                        self.velocity.x = 0
                    
                elif bottom.colliderect(pygame.Rect(self.rect.x  , self.rect.y + self.dy , self.rect.width, self.rect.height)):
                    
                    self.rect.bottom = bottom.top
                        
                    self.dy = 0
                    self.velocity.y = 0
                    
                rrec1 = pygame.Rect(toprect.x - offset[0],toprect.y - offset[1], toprect.width, toprect.height)
                rrect2 = pygame.Rect(bottom.x - offset[0],bottom.y - offset[1], bottom.width, bottom.height)
                
                return rrec1, rrect2
                    
            elif self.curent_hallway.type == 'v':
                
                leftrect = pygame.Rect(self.curent_hallway.rect.x-self.curent_hallway.height - 60, self.curent_hallway.rect.y , self.curent_hallway.rect.width+ 60, self.curent_hallway.rect.height,)
                
                if leftrect.colliderect(pygame.Rect(self.rect.x + self.dx , self.rect.y , self.rect.width, self.rect.height)):
                    
                    self.rect.left = leftrect.right
                        
                    self.dx = 0
                    self.velocity.x = 0
                    
                elif leftrect.colliderect(pygame.Rect(self.rect.x  , self.rect.y + self.dy , self.rect.width, self.rect.height)):
                    
                    
                    if self.dy > 0:
                        
                        self.rect.bottom = leftrect.top
                            
                        self.dy = 0
                        self.velocity.y = 0
                    if self.dy < 0:
                        
                        self.rect.top = leftrect.bottom
                            
                        self.dy = 0
                        self.velocity.y = 0
                        
         
         
                bottom = pygame.Rect(self.curent_hallway.rect.x + self.curent_hallway.height, self.curent_hallway.rect.y , self.curent_hallway.rect.width + 60, self.curent_hallway.rect.height,)
                
                if bottom.colliderect(pygame.Rect(self.rect.x +self.dx , self.rect.y , self.rect.width, self.rect.height)):
                    
                    self.rect.right = bottom.left
                        
                    self.dx = 0
                    self.velocity.x = 0
                    
                elif bottom.colliderect(pygame.Rect(self.rect.x  , self.rect.y + self.dy , self.rect.width, self.rect.height)):
                    
                    
                    if self.dy > 0:
                        
                        self.rect.bottom = bottom.top
                            
                        self.dy = 0
                        self.velocity.y = 0
                    if self.dy < 0:
                        
                        self.rect.top = bottom.bottom
                            
                        self.dy = 0
                        self.velocity.y = 0
                        self.velocity.y = 0
                    
                    
                rrec1 = pygame.Rect(leftrect.x - offset[0],leftrect.y - offset[1], leftrect.width, leftrect.height)
                rrect2 = pygame.Rect(bottom.x - offset[0],bottom.y - offset[1], bottom.width, bottom.height)
                    
                    
                return rrec1, rrect2
            
        return pygame.Rect(0,0,0,0), pygame.Rect(0,0,0,0)
    
    def update_orientation(self, scroll):
        
        self.pos = pygame.math.Vector2(self.rect.center)
        self.mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos()) + scroll  # Consider the scroll offset

        angle_to_mouse = self.pos - self.mouse_pos  # Calculate the vector pointing to the mouse
        self.degrees = round(angle_to_mouse.as_polar()[1])   # Get the angle from the polar coordinates
        
        self.ori = 'up' if self.degrees in self.go_up else 'right' if self.degrees in self.go_right else 'left' if self.degrees in self.go_left else 'down' if self.degrees in self.go_down else self.last_ori
        self.last_ori = self.ori
        
   
        
    def cap_velocity(self, max_vel):
        
        if self.velocity.x > max_vel :
            self.velocity.x = max_vel
            
        if self.velocity.y > max_vel:
            self.velocity.y = max_vel
            
        if self.velocity.x < -max_vel :
            self.velocity.x = -max_vel
            
        if self.velocity.y < -max_vel:
            self.velocity.y = -max_vel
            
    def slow_velocity(self, vel_slow ,dt):
        k = pygame.key.get_pressed()
        
        if not k[pygame.K_d] and not k[pygame.K_a]:
            
            self.velocity.x = self.velocity.move_towards((0,0), vel_slow * dt ).x
            
        if not k[pygame.K_w] and not k[pygame.K_s]:
            
            self.velocity.y = self.velocity.move_towards((0,0), vel_slow * dt ).y
                   
    def update_anims(self):
        
        self.animator.update_animations()
        
        if self.animator.anim_name.split('_')[0] == 'punch' or self.animator.anim_name.split('_')[0] == 'bigpunch':
            if self.animator.anim.done:
                
                self.animator.set_anim('idle'+'_'+self.ori)
                
        elif pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_d]:
            
            self.animator.set_anim_no_refresh('run_'+self.ori)
            
        else:
                
        # if self.animator.anim_name.split('_')[0] == 'idle':
            
            self.animator.set_anim_no_refresh('idle'+'_'+self.ori)
        
        self.image = self.animator.get_image()
    
    def update(self, scroll, dt):
        k = pygame.key.get_pressed()

        # Create a Vector2 instance for velocity
        velocity_change = pygame.math.Vector2(
            (k[pygame.K_d] - k[pygame.K_a]) * self.speed * self.powers['speed'] * dt * max(1, self.dash * self.dash_strength),
            (k[pygame.K_s] - k[pygame.K_w]) * self.speed * self.powers['speed'] * dt * max(1, self.dash * self.dash_strength)
        )

        # Normalize the velocity change vector
        try:
            velocity_change.normalize_ip()
        except Exception:
            pass

        # Add the normalized velocity change to the current velocity
        self.velocity += velocity_change

        self.cap_velocity(1.5 * self.powers['speed'] * max(1, self.dash * self.dash_strength)) if not self.dash else 0

        self.dx, self.dy = self.velocity.x, self.velocity.y

        self.slow_velocity(0.05, dt)

        self.update_anims()

        self.dashing()

        self.update_orientation(scroll)

        self.update_combat()

        self.render_rect = pygame.FRect(self.rect.x - 0, self.rect.y - 0, self.rect.width, self.rect.height)

    def apply_movement(self, dt):
        
        
        # self.normalise_speed()
        self.rect.x += self.dx * dt
        self.rect.y += self.dy * dt

        
    def update_combat(self):
        keys = pygame.key.get_pressed()
        
        now_attack = 'right' if self.last_attack_turn == 'left' else 'left'
        if not self.inventory.open:
            if keys[pygame.K_LCTRL] and self.can_attack:
                self.can_attack = False
                
                self.last_attack_type = 'big'
                
                self.animator.set_anim('bigpunch_'+self.ori+'_'+now_attack)
                self.last_attack_turn = now_attack
                
                if self.ori == 'up':
                    top = self.rect.y - 32
                    left = self.rect.x - 7
                    width_height = (32 + 14,32)
                if self.ori == 'down':
                    top = self.rect.y + self.rect.width 
                    left = self.rect.x - 7
                    width_height = (32 + 14,32)
                    
                if self.ori == 'left':
                    top = self.rect.y - 7
                    left = self.rect.x - 32
                    width_height = (32,32 + 14)
                    
                if self.ori == 'right':
                    top = self.rect.y - 7
                    left = self.rect.x + self.rect.width 
                    width_height = (32,32 + 14)

                self.hitboxes.append(Hitbox((left, top , *width_height, ), self.ori, self.damage * self.powers['damage'] *1.5))
                
                self.attacking = True
                
                self.stop_attack_time = pygame.time.get_ticks() + self.stop_interval + 150
            
            if keys[pygame.K_SPACE] and self.can_attack:
                
                self.last_attack_type = 'small'
                
                self.can_attack = False
                
                self.animator.set_anim('punch'+'_'+self.ori+'_'+now_attack)
                self.last_attack_turn = now_attack
                
                if self.ori == 'up':
                    top = self.rect.y - 32
                    left = self.rect.x - 7
                    width_height = (32 + 14,32)
                if self.ori == 'down':
                    top = self.rect.y + self.rect.width 
                    left = self.rect.x - 7
                    width_height = (32 + 14,32)
                    
                if self.ori == 'left':
                    top = self.rect.y - 7
                    left = self.rect.x - 32
                    width_height = (32,32 + 14)
        
                if self.ori == 'right':
                    top = self.rect.y - 7
                    left = self.rect.x + self.rect.width 
                    width_height = (32,32 + 14)

                self.hitboxes.append(Hitbox((left, top , *width_height, ), self.ori, self.damage * self.powers['damage']))
        
                self.attacking = True
                
                self.stop_attack_time = pygame.time.get_ticks() + self.stop_interval
                
                
            if pygame.time.get_ticks() > self.stop_attack_time and self.attacking:
                
                self.attacking = False
                
                self.hitboxes = []
                
                if self.last_attack_type == 'big':
                
                    self.next_attack = pygame.time.get_ticks() + self.attack_interval + 150
                    
                else:
                    self.next_attack = pygame.time.get_ticks() + self.attack_interval
                
            if pygame.time.get_ticks() > self.next_attack and not self.can_attack and not self.attacking:
                
                self.can_attack = True
        else:
            
            self.hitboxes = []
               
    def render(self, display, offset, nocap=True):
        self.render_rect = pygame.FRect(self.rect.x - offset[0], self.rect.y - offset[1], self.rect.width, self.rect.height)

        
        # pygame.draw.rect(display, (125, 250, 100), self.render_rect)
        # pygame.draw.circle(display, (0,0,0), self.render_rect.center, 3)
        
        if nocap:
            display.blit(self.image, (self.rect.x - offset[0] , self.rect.y - offset[1] ))
            
            # pygame.draw.circle(display, (255,255,255), self.pos + pygame.math.Vector2(400 + 29,300 - 57), 16)
            
            # for box in self.hitboxes:
                
            #     box.render(display, offset)
     
    def set_pos(self, pos):
        
        self.rect.topleft = pos 
        