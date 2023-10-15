
import pygame 
from random import randint, choice

from scripts.combat_manager import Hitbox
# from scripts.writing import Writing
from scripts.settings import coin_multi
from scripts.animations import Animation, Animator
from scripts.font_inits import *

def outline(img):
    mask = pygame.mask.from_surface(img)
    mask_outline = mask.outline()
    
    # Create a new display surface with the same dimensions as the image
    new_display = pygame.Surface(img.get_size())
    
    # Fill the new display with a transparent color
    new_display.fill((0, 0, 0))
    new_display.set_colorkey((0, 0, 0))
    
    # Draw the outline on the new display
    for pixel in mask_outline:
        new_display.set_at(pixel, (255, 255, 255))
    
    return new_display

class Item:
    
    def __init__(self, tag, name, img: pygame.Surface, world_game_name='',carry_type='single_hand', stack_size=-1, desc = ''):
        
        self.tag = tag 
        self.name = name 
        self.image = pygame.transform.scale(img, (32,32))
        self.rect = pygame.FRect(0,0, 36,36)
        self.desc = desc
        
        self.image.blit(outline(self.image), (0,0))
        imgs = [med_font.render(line, False, (255,255,255)).convert_alpha() for line in desc.split('lnbr')]
        largest_width = sorted(imgs, key= lambda x : x.get_width(), reverse=True)[0].get_width()
        
        self.text_surf = pygame.Surface(
            (largest_width + 10, 16 * len(imgs) )
            ).convert_alpha()
        
        for i, img in enumerate(imgs):
            self.text_surf.blit(img, (0, i * 16))

        self.text_surf.set_colorkey((0,0,0))
        
        self.name_img = med_font.render(self.name, False, (0,100,255)).convert_alpha()
        self.name_img.set_colorkey((0,0,0))
        
        if world_game_name != '':

            world_game_image = pygame.image.load(f'assets/images/weapons/game_world_weapon_sprites/hidden_blade.png')
            self.world_game_img_name = world_game_name
            self.carry_type = carry_type
            self.world_image = world_game_image.convert_alpha()


        self.stack_size = stack_size
        
        self.dropped = False 
        
        self.inventory = None 
        
        self.remove_from_dropped = False
        
        self.pickable = False
    
    def trace_in_animation(self, image_list : [pygame.Surface, pygame.Surface], points : [(),()], save=True):
        
        img_list = []
        
        for i, image in enumerate(image_list):
            
            img = pygame.Surface(image.get_size())
            img.blit(image, (0,0))
            img.blit(self.world_image, points[i])
            
            img_list.append(img)
            
            image.blit(self.world_image, points[i])
            
            if not save:
                return img_list
            
            pygame.image.save(image, f"assets/images/weapons/game_world_weapon_sprites/game_generated/{self.carry_type}_{self.world_game_img_name}_{i}.png")
            
            
        return 
    
    def set_inventory(self, inventory):
        
        self.inventory = inventory
        
    def pickup(self):
        
        self.remove_from_dropped = True
        
        self.inventory.add_item(self.copy())
    
    def drop(self, player=None, give_vel=True):
        
        self.dropped = True
        
        self.vel_y = 0.5 if give_vel else 0
        
        self.pos = list(self.inventory.player.rect.topleft if self.inventory is not None else player.rect.topleft)
        
    def copy(self):
        
        return Item(self.tag, self.name, self.image, self.stack_size, desc=self.desc)
    
    def update_dropped(self, dt):
            
        self.vel_y = pygame.math.Vector2((0, self.vel_y)).move_towards((0,0), 0.15*dt).y
            
        self.pos[1] += self.vel_y
        
        if pygame.FRect(*self.pos, 36,36).colliderect(self.inventory.player.rect):
            
            if self.vel_y == 0:
                
                if self.tag == 'weapon':
                    
                    for item in list(self.inventory.items.values()):
                        
                        if item[0].tag == 'weapon':
                            
                            return
                
                self.pickup()
        
    def render_dropped(self, display : pygame.Surface, scroll=[0,0]):
        
        render_rect = pygame.FRect(self.pos[0] - scroll[0], self.pos[1] - scroll[1], *self.rect.size)
        
        display.fblits([(self.image, render_rect.topleft)])
        
    def list(self):
        
        return  '{}, {}'.format(self.tag, self.name)
        
    def __str__(self):
        
        return '{}, {}'.format(self.tag, self.name)
    
item_dict = {
    'compass' : Item('util', 'Compass', pygame.image.load('assets/images/icons/compass.png').convert_alpha(), desc='Colours your Minimap lnbrTo show you the Way'),
    'spoon' : Item('util', 'Comically Large Spoon', pygame.image.load('assets/images/icons/spoon.png').convert_alpha(), desc='Increases your Hit Range lnbr'),
    'vial' : Item('util', 'Blood Vial', pygame.image.load('assets/images/icons/vial.png').convert_alpha(), desc='Vastly Increases Damage lnbrBut lowers your endurance'),
    'fang_extendors' : Item('util', 'Fang Extendors', pygame.image.load('assets/images/icons/fang_extendors.png').convert_alpha(), desc='Suck your enemies blood lnbrIn order to heal yourself'),
    'stim' : Item('util', 'Stim Pack', pygame.image.load('assets/images/icons/stim.png').convert_alpha(), desc='Injecting severely lowers yourlnbrhealth, But gives a speed boost'),
}
weapons_dict = {
    'axe' : Item('weapon', 'Frozen Axe', pygame.image.load('assets/images/weapons/axe.png').convert_alpha(),world_game_name='', carry_type='single_hand' ,desc='Mythical Axe from the Norse era.lnbrFreezes enemies and is throwable'),
    'sicles' : Item('weapon', "Devil's Sicles", pygame.image.load('assets/images/weapons/sicles.png').convert_alpha(),world_game_name='', carry_type='single_hand' ,desc='These divine Sicles are sentlnbrstraight from Hells hottest level'),
    'blades' : Item('weapon', "Zeus's Hidden Blades", pygame.image.load('assets/images/weapons/hidden_blade.png').convert_alpha(),world_game_name='hidden_blade', carry_type='single_hand' ,desc='Handcrafted from Zeus himself,lnbrThese blades strike lighting fast and stun', stack_size=-1),
    'katana' : Item('weapon', "Fujin's Sword", pygame.image.load('assets/images/weapons/katana.png').convert_alpha(),world_game_name='', carry_type='single_hand' ,desc='Created in Fujins finest forgery,lnbrThis Katana will slice flesh like its wind'),
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
        
        self.item_positions = [(self.rect.center[0] - self.rect.width//2 + 93 +(50* i), self.least_y+20 ) for i in range(1, 7)]
        
        self.vel = 0
        
        self.writing = med_font
        
        self.selected_item=  None
        
        self.dropped_items = []
        
        self.weapon_surf = pygame.Surface((32,32)).convert_alpha()
        self.weapon_surf.fill((75,180,180))
        
        self.util_surf = pygame.Surface((32,32)).convert_alpha()
        self.util_surf.fill((150,150,60))
        
        self.test_surf = pygame.Surface((32,32)).convert_alpha()
        self.test_surf.fill((255,255,255))
        
        self.item_background_colors = {
            
            'weapon' : self.weapon_surf,
            'util' : self.util_surf,
            
        }
        
        self.clicked = False
        
        self.slot_binds = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]
        
    def get_tag_list(self):
        
        return list(self.items.keys())
    
    def render_dropped_items(self, dt, display, scroll):
        
        if self.player.game.time == 100:
            dt /= 4
        
        for item in self.dropped_items:
            item.update_dropped(dt)
            item.render_dropped(display, scroll)
            
            if item.remove_from_dropped:
                
                self.dropped_items.remove(item)
    
    def remove_item(self, itemname, count=1, give_vel = True):

        if len(self.items[itemname]) == 1:
        
            self.items[itemname][0].set_inventory(self)
            self.items[itemname][0].drop(give_vel=give_vel)
            self.dropped_items.append(self.items[itemname][0])
            # self.items[itemname].pop(0)
            
            del self.items[itemname]
            
            self.refresh_stuff()
            
            self.affect_player()
            
            self.selected_item = None
            
            return 
        
        self.items[itemname][0].drop()
        self.dropped_items.append(self.items[itemname][0])
        self.items[itemname].pop(0)
        self.affect_player()

    def add_item(self, item):
        
        if len(self.items.keys()) < 4 or item.name in self.get_tag_list():
        
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

            if item.tag == 'weapon':
                
                for itemm in list(self.items.values()):
                    if itemm[0].tag == 'weapon':
                
                        if item.name in list(self.items.keys()):
                            
                            self.items[item.name].append(item)
                        
                        else:
                            
                            self.items[item.name] = []
                            self.items[item.name].append(item)
                
                        
                        self.remove_item(item.name, True)
                        item.vel_y =0
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
                    
        self.sort_by_tag()
                    
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
           
    def sort_by_tag(self):
        
        # first weapons, then utils
        
        self.key_list = []
        self.val_list = []
        
        for item_list in list(self.rendered_dict.values()):
            
            
            
            tag = item_list[0].tag
            
            if tag == 'weapon':
                
                self.key_list.insert(0, item_list[0].name)
                self.val_list.insert(0, item_list[0])
            else:
                
                self.key_list.append(item_list[0].name)
                self.val_list.append(item_list[0])
             
    def highlight_selected(self, item, display, pos):
        
        if self.selected_item and item.name == self.selected_item.name:
                
                pygame.draw.circle(display, (255,255,255), (pos[0] + 15, pos[1] + 15), 20, 5)
           
    def render_item_image(self, item, display, pos):
        display.fblits([(self.item_background_colors[item.tag], (pos))])
        display.fblits([(item.image, (pos[0] , pos[1] ))])
        
    def render(self, display, mouse_pos, dt=1, scroll=[0,0]): 
        
        if not display.get_rect().colliderect(self.rect):
            return 
            
        pygame.draw.rect(display, (100,100,100), self.rect)
        pygame.draw.rect(display, (0,0,0), self.rect, 5)
        
        for x, itemkey in enumerate(self.key_list):
            
            item_list = self.rendered_dict[itemkey]
            
            item_count = item_list[1]
            
            pos = [self.item_positions[x][0] , self.item_positions[x][1]  -( self.max_y- self.rect.y - 90  if self.open else self.least_y - self.rect.y - 90)]

            self.render_item_image(item_list[0], display, pos )
            
            text = self.writing.render(str(item_count), False, (255,255,255))
            
            text_rect = text.get_rect(bottomleft = item_list[0].image.get_rect(topleft=  pos).bottomleft)
            
            display.fblits([(text, text_rect.topleft)]) if item_count > 1 else 0
                
            self.highlight_selected(item_list[0], display, pos)
                
            col_rect = pygame.Rect(*pos, item_list[0].image.get_rect().width, item_list[0].image.get_rect().height)
            
            if col_rect.collidepoint(mouse_pos):
                pygame.draw.rect(display, (30,30,30), pygame.Rect(pos[0], pos[1] - 95, item_list[0].text_surf.get_width() +8 , 70))
                pygame.draw.rect(display, (30,30,30), pygame.Rect(pos[0], pos[1] - 25, 8, 25))
                
                display.fblits([(item_list[0].text_surf, (pos[0]+ 5, pos[1] - 70))])
                display.fblits([(item_list[0].name_img, (pos[0]+ 5, pos[1] - 90))])
                
                if pygame.mouse.get_pressed()[0] and not self.clicked:
                    
                    self.selected_item = item_list[0] if self.selected_item != item_list[0] else None
                    
                    self.clicked = True
                    
            # print(self.dropped_items)
                        
            if not pygame.mouse.get_pressed()[0]:
                
                self.clicked = False
 
    def affect_player(self):
        
        self.player.game.minimap.feed_rooms(self.player.game.dungeon.get_room_list())
        self.player.game.minimap.feed_hallways(self.player.game.dungeon.hallways)
        
        all_items = list(self.items.values())
        
        item_name_list = [item[0].name for item in all_items ]
        
        base_player_hp = 3
        base_player_damage = 1
        
        if 'Comically Big Spoon' in item_name_list:
            
            self.player.big_spoon_buff = 10
        else:
            self.player.big_spoon_buff = 0

        if 'Blood Vial' in item_name_list:
            base_player_hp -= 1 
            # if self.player.hp > self.player.max_hp:
            #     self.player.hp = self.player.max_hp
            # self.player.base_powers['damage'] = 1.7
            base_player_damage += .2
            self.player.refresh_powers()
        else:
            # if self.player.hp > self.player.max_hp:
            #     self.player.hp = self.player.max_hp
            # self.player.base_powers['damage'] = 1
            self.player.refresh_powers()
            
        if 'Fang Extendors' in item_name_list:
            self.player.lifesteal = True
        else:
            self.player.lifesteal = False
            
        if 'Stim Pack' in item_name_list:
            base_player_hp -= 1 
            self.player.base_powers['speed'] = 1.201
            self.player.refresh_powers()
        else:
            self.player.base_powers['speed'] = 1
            self.player.refresh_powers()
            
        if 'Frozen Axe' in item_name_list:
            
            base_player_damage += .6
        if "Devil's Sicles" in item_name_list:
            
            base_player_damage += .32
        if "Zeus's Hidden Blades" in item_name_list:
            
            base_player_damage += .15
        if "Fujin's Sword" in item_name_list:
            
            base_player_damage += .4
            
        if self.val_list[0].tag == 'weapon':
            
            carry_type = self.val_list[0].carry_type
            
            for ori in ['up', 'down', 'left', 'right']:
                
                for dir in ['left', 'right']:
                    
                    
                
            
                    string = carry_type + '_temp' +'_'+ori+'_'+dir
                    self.val_list[0].trace_in_animation(
                        self.player.animator.animations[string].images,
                        [
                            [0,0],
                            [0,0],
                            [0,0],
                            [0,0],
                            [0,0],
                            [0,0],

                        ], False
                        
                    )
            
            self.player.has_weapon = True 
            self.player.weapon = self.val_list[0]
            
        else:
            
            self.player.has_weapon = False 
            self.player.weapon = None

            
        self.player.max_hp = base_player_hp
        if self.player.hp > self.player.max_hp:
            self.player.hp = max(self.player.max_hp, 1)
            
        self.player.base_powers['damage'] = base_player_damage
        
        self.player.refresh_powers()
        

class Player:
    
    def __init__(self, pos, speed, start_room, game):
        
        self.rect = pygame.FRect(*pos, 24,24)
        self.velocity = pygame.math.Vector2(0,0)
        self.speed = speed
        
        self.game = game
        
        self.last_ori = 'up'
        self.ori = 'up'
        self.state = 'regular'
        
        self.has_weapon = False
        self.weapon = None
        
        self.rect.center = pos
        
        self.attacking = False
        self.can_attack = True
        self.hitboxes = []
        
        self.lifesteal = False
        
        self.current_room = start_room
        self.curent_hallway = None
        
        self.coins = 0
        self.damage = 1
        self.base_powers = {'speed': 1, 'damage' : 1,'dash_strength' : 1 }
        self.power_adds = {'speed': 0, 'damage' : 0,'dash_strength' : 0}
        self.powers = self.base_powers.copy()
        
        self.hp = 0
        self.max_hp = 3
        
        self.stop_interval = 50
        self.stop_attack_time = pygame.time.get_ticks() + self.stop_interval
    
        self.attack_interval = 250
        self.next_attack = pygame.time.get_ticks() + self.attack_interval
        
        self.go_left = range(-45,45)
        self.go_right = list(range(135,180)) +  list(range(-180,-135))
        self.go_down = range(-135,-45)
        self.go_up = range(45, 135)
        
        self.big_spoon_buff = 0
        
        self.inventory = Inventory(self)
        
        
        self.animator = Animator(
            
            {
                'idle' : Animation(self.game.assets['player']['idle'],), 
                
                'run' : Animation(self.game.assets['player']['run'],), 
                
                'punch' : Animation(self.game.assets['player']['punch'],30), 
                
                'bigpunch' : Animation(self.game.assets['player']['big_punch'],60),
                
                'single_hand_temp' : Animation(self.game.assets['player']['single_hand'],160),
                
                
            },'idle'+'_'+self.ori)
        
        self.animator.clone_in_4_dirs('idle')
        self.animator.clone_in_4_dirs('run')
        
        self.animator.clone_in_4_dirs_and_flip('punch')
        self.animator.clone_in_4_dirs_and_flip('bigpunch')
        self.animator.clone_in_4_dirs_and_flip('single_hand_temp')
        
        self.animator.set_base_anim()
        
        self.dx, self.dy = 0,0
        self.last_attack_turn = 'left'
        
        self.image = self.animator.get_image()
        
        self.dash_strength = 15
        self.can_dash = True
        self.dash = False
        self.stop_dash_time = 50
        self.next_stop_dash = pygame.time.get_ticks() + self.stop_dash_time
        
        self.dash_timer = 2000
        self.time_till_next_dash = pygame.time.get_ticks() + self.dash_timer
        
    def dashing(self):
        
        k = pygame.key.get_pressed()
        
        if k[pygame.K_LSHIFT] and self.can_dash and not self.dash:
            
            self.dash = True 
            self.next_stop_dash = pygame.time.get_ticks() + self.stop_dash_time
            self.can_dash = False
            
        if self.dash:
            
            if pygame.time.get_ticks() > self.next_stop_dash:
                self.dash = False
                self.time_till_next_dash = pygame.time.get_ticks() + self.dash_timer
            else:
                
                self.hitboxes.append(Hitbox(self.rect, self.ori, 1, 1 ))

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
        
    def refresh_powers(self):
        
        self.powers['damage'] = self.base_powers['damage'] + self.power_adds['damage']
        self.powers['speed'] = self.base_powers['speed'] + self.power_adds['speed']
        self.powers['dash_strength'] = self.base_powers['dash_strength'] + self.power_adds['dash_strength']
        
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

        self.cap_velocity(1.5 * self.powers['speed'] * max(1, self.dash * self.dash_strength)) #if not self.dash else 0

        self.dx, self.dy = self.velocity.x, self.velocity.y

        self.slow_velocity(0.13, dt)

        self.update_anims()

        self.dashing()

        self.update_orientation(scroll)

        self.update_combat()

        self.render_rect = pygame.FRect(self.rect.x - 0, self.rect.y - 0, self.rect.width, self.rect.height)

    def apply_movement(self, dt):
        
        
        # self.normalise_speed()
        self.rect.x += self.dx * dt
        self.rect.y += self.dy * dt

    def attack(self, type, anim_name, damage_multi = 1, interval_plus = 0):
        
        now_attack = 'right' if self.last_attack_turn == 'left' else 'left'
                    
        self.can_attack = False
        
        self.last_attack_type = type
        
        if self.weapon == None:
        
            self.animator.set_anim(f'{anim_name}_'+self.ori+'_'+now_attack)
        else:
            
            self.animator.set_anim(self.weapon.carry_type+'_temp_'+self.ori+'_'+now_attack)
        
        self.last_attack_turn = now_attack
        
        match self.ori: 
            
            case 'up':
                top = self.rect.y - 32  - self.big_spoon_buff
                left = self.rect.x - 11
                width_height = (32 + 14,32 + self.big_spoon_buff)
                
            case 'down':
                top = self.rect.y + self.rect.width #+ self.big_spoon_buff
                left = self.rect.x - 11
                width_height = (32 + 14,32 + self.big_spoon_buff)
            
                
            case 'left':
                top = self.rect.y - 11
                left = self.rect.x - 32
                width_height = (32 + self.big_spoon_buff,32 + 14)
                
            case 'right':
                top = self.rect.y - 11
                left = self.rect.x + self.rect.width 
                width_height = (32 + self.big_spoon_buff,32 + 14)
        
        self.hitboxes.append(Hitbox((left, top , *width_height, ), self.ori, self.damage * self.powers['damage'] * damage_multi),)
        
        self.attacking = True
        
        self.stop_attack_time = pygame.time.get_ticks() + self.stop_interval + interval_plus
    
    def update_combat(self):
        keys = pygame.key.get_pressed()
        
        # now_attack = 'right' if self.last_attack_turn == 'left' else 'left'
        
        if pygame.time.get_ticks() > self.stop_attack_time and self.attacking:
            
            self.attacking = False
            
            self.hitboxes = []
            
            if self.last_attack_type == 'big':
            
                self.next_attack = pygame.time.get_ticks() + self.attack_interval + 150
                
            else:
                self.next_attack = pygame.time.get_ticks() + self.attack_interval
            
        if pygame.time.get_ticks() > self.next_attack and not self.can_attack and not self.attacking:
            
            self.can_attack = True

        for hitbox in self.hitboxes:
            
            if hitbox.die_time != 'stayforever':
                
                hitbox.update()
                
                if hitbox.be_removed:
                    
                    self.hitboxes.remove(hitbox)
        
        if self.inventory.open:
                
            self.hitboxes = []
            return
            
        if not self.can_attack:
            return
            
        if keys[pygame.K_LCTRL]:
            
            self.attack('big', 'bigpunch', 1.5, 150)
        
        elif keys[pygame.K_SPACE]:
            
            self.attack('big', 'punch' )
            
            
               
    def render(self, display, offset, nocap=True):
        self.render_rect = pygame.FRect(self.rect.x - offset[0], self.rect.y - offset[1], self.rect.width, self.rect.height)

        
        # pygame.draw.rect(display, (125, 250, 100), self.render_rect)
        # pygame.draw.circle(display, (0,0,0), self.render_rect.center, 3)
        
        if nocap:
            display.fblits([(self.image, (self.rect.x - offset[0] , self.rect.y - offset[1] ))])
            
            # pygame.draw.circle(display, (255,255,255), self.pos + pygame.math.Vector2(400 + 29,300 - 57), 16)
            
            for box in self.hitboxes:
                
                box.render(display, offset)
     
    def set_pos(self, pos):
        
        self.rect.topleft = pos 
        