import pygame
from pygame.locals import *
from time import time
import math, sys
from random import randint 

from scripts.room import Room, BlankRoom
from scripts.dungeon_generator import Dungeon
from scripts.minimap import Minimap
from scripts.player import Player
from scripts.combat_manager import CombatSystem
from scripts.writing import Writing
from scripts.filehandling import loadvar, savevar
from scripts.main_menu_helper import Button, MultiSelect
from scripts.loot import SpeedUp, StrenghtUp
from scripts.utils import load_images_from_folder
from scripts.animations import Animation

debug = False

pygame.init()
pygame.display.init()
pygame.mouse.set_visible(False)
pygame.display.set_caption("Vampire's Abyss")

def change_color(img,  new_color):
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            pixel_color = img.get_at((x, y))
            if pixel_color.a == 255:
                new_pixel_color = pygame.Color(new_color[0], new_color[1], new_color[2], pixel_color.a)
                img.set_at((x, y), new_pixel_color)

def draw_lighted_image(display: pygame.Surface, img : pygame.Surface, pos:tuple[int, int]):
    
    display.blit(img,pos,special_flags=BLEND_RGBA_ADD)
    
def draw_darkened_image(display, img,pos):
    
    display.blit(img,pos,special_flags=BLEND_MULT)
    
def create_circle_light(color_range=100, circle_multiplier=1, color_extra=(1,1,1)):
    
    
    light_surf = pygame.Surface((color_range *2,color_range *2), pygame.SRCALPHA).convert_alpha()

    for i in range(color_range):
        pygame.draw.circle(light_surf, (round(i *color_extra[0])  ,round(i *color_extra[1])  ,round(i * color_extra[2]) ), (light_surf.get_width()//2,light_surf.get_height()//2), color_range - i)



    light_surf = pygame.transform.scale(light_surf, (light_surf.get_width()*circle_multiplier,light_surf.get_height()*circle_multiplier))
    
    return light_surf

def create_colorized_radial_gradient(radius, center_color, outer_color, intensity=1):
    size = (2 * radius, 2 * radius)
    surface = pygame.Surface(size, pygame.SRCALPHA)
    center = (radius, radius)
    pixels = pygame.PixelArray(surface)
    
    for y in range(size[1]):
        for x in range(size[0]):
            pixel = (x, y)
            distance = pygame.math.Vector2(pixel).distance_to(center)
            normalized_distance = max(0, min(distance / radius, 1))
            interpolated_color = (
                abs(int(center_color[0] + normalized_distance * (outer_color[0] - center_color[0]))),
                abs(int(center_color[1] + normalized_distance * (outer_color[1] - center_color[1]))),
                abs(int(center_color[2] + normalized_distance * (outer_color[2] - center_color[2]))),
            )
            alpha = abs(int(center_color[3] + normalized_distance * (outer_color[3] - center_color[3])))

            pixels[x, y] = pygame.Color(*interpolated_color, alpha)
    
    del pixels
    for _ in range(intensity-1):
        surface.blit(surface.copy(), (0,0), special_flags=pygame.BLEND_ADD)
    return surface

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

class Game:
    
    def save_all_data(self):
        
        savevar('player_coins.wlr', self.player.coins)
        
        savevar('user_settings.wlr', self.fps_choices.selected)
        
    def load_all_data(self):
        
        if not debug:
            
            try:
        
                self.player.coins = loadvar('player_coins.wlr')
            except FileNotFoundError:
                
                pass
            
            try:
        
        
                self.fps_cap_choice = int(loadvar('user_settings.wlr'))
                print(self.fps_cap_choice)
            except FileNotFoundError:
                
                self.fps_cap_choice = 0
            
        else:
            
            self.player.coins = 0
    
    def save_all_every(self, ticks):
        if pygame.time.get_ticks() > self.next_save:
            
            self.save_all_data()
            
            self.next_save = pygame.time.get_ticks() + ticks
            
            # print('quick save')
    
    def load_assets(self):
        
        IMG_PATH = 'assets/images/'
        self.vignette_offset = 100
        self.vignete_zoom = 2

        darkensurf = pygame.Surface(self.display.get_size()).convert_alpha()
        
        self.darken = 150
        
        darkensurf.fill((self.darken, self.darken, self.darken))
        
        light_surfs = {'demontime': None, 'regular': None}
        
        light_surfs['demontime'] = create_circle_light(100, 1.5, (2,1,1))
        light_surfs['regular'] = create_circle_light(255, 0.6, (1,1,1))
        
        
        self.assets = {
            
            'vignette': pygame.transform.scale(pygame.image.load(IMG_PATH+'effects/vignete.png').convert_alpha(), (self.display.get_width() + self.vignette_offset, self.display.get_height()+ self.vignette_offset)),
            'player_light': light_surfs,
            'darken' : darkensurf,
            'chest_glow' : create_circle_light(75, 0.8, (2,2,1)),
            'new_level_block_glow' : create_circle_light(180, 1, (1.2,1.2,1.2)),
            
            'room_light' : create_circle_light(255, 1.5),
            
            'powerup_glow' : {
                
                SpeedUp: create_circle_light(35, 0.4 * 3, (5,5,1)),
                StrenghtUp: create_circle_light(35, 0.4* 3, (5,1,1))
                              
                              },
            
            'mouse_glow' : create_circle_light(100,0.3,(1.1,0,0)),
            
            'mouse_png' : pygame.image.load(IMG_PATH+ 'misc/effects.png').convert_alpha(),
            
            'bat_glow' : create_circle_light(60, 0.8, (1.5, 0, 0)),
            
            'main_menu' : load_images_from_folder(IMG_PATH+'main menu/logo', sizeup=3),
            'bat' : load_images_from_folder(IMG_PATH+'main menu/bat',sizeup=3),
            
            'player' : {
                'idle' :{
                    
                    'up' : load_images_from_folder('assets/images/player/idle'),
                    'down' : load_images_from_folder('assets/images/player/idle', 180),
                    'left' : load_images_from_folder('assets/images/player/idle', 90),
                    'right' : load_images_from_folder('assets/images/player/idle', -90),
                    
                    },
                
                'punch_left' :{
                    
                    'up' : load_images_from_folder('assets/images/player/punch', 0),
                    'down' : load_images_from_folder('assets/images/player/punch', 180),
                    'left' : load_images_from_folder('assets/images/player/punch', 90),
                    'right' : load_images_from_folder('assets/images/player/punch', -90),
                    
                    },
                
                'punch_right' :{
                    
                    'up' : load_images_from_folder('assets/images/player/punch',0,True),
                    'down' : load_images_from_folder('assets/images/player/punch', 180,True),
                    'left' : load_images_from_folder('assets/images/player/punch', 90,True),
                    'right' : load_images_from_folder('assets/images/player/punch', -90,True),
                    
                    },
                
                'big_punch_left' :{
                    
                    'up' : load_images_from_folder('assets/images/player/big_punch'),
                    'down' : load_images_from_folder('assets/images/player/big_punch', 180),
                    'left' : load_images_from_folder('assets/images/player/big_punch', 90),
                    'right' : load_images_from_folder('assets/images/player/big_punch', -90),
                    
                    },
                'big_punch_right' :{
                    
                    'up' : load_images_from_folder('assets/images/player/big_punch',0,True),
                    'down' : load_images_from_folder('assets/images/player/big_punch', 180,True),
                    'left' : load_images_from_folder('assets/images/player/big_punch', 90,True),
                    'right' : load_images_from_folder('assets/images/player/big_punch', -90,True),
                    
                    },
                
                'run' :{
                    
                    'up' : load_images_from_folder('assets/images/player/run'),
                    'down' : load_images_from_folder('assets/images/player/run', 180),
                    'left' : load_images_from_folder('assets/images/player/run', 90),
                    'right' : load_images_from_folder('assets/images/player/run', -90),
                    
                    },
                
            }
        
        }
    
    def __init__(self):
        
        self.next_save = pygame.time.get_ticks() + 15000
        
        self.zoom =2
        
        flags = pygame.SCALED | pygame.FULLSCREEN if not debug else 0
        self.screen = pygame.display.set_mode((1280, 720), flags=flags)
        self.display = pygame.Surface((1280//self.zoom, 720//self.zoom)).convert_alpha()
        self.dis_with_bcg = self.display
        self.dis_with_bcg.fill((36,45,52))
        self.darker_surf = self.display
        self.darker_surf.fill((12,15,28))
        self.clock = pygame.time.Clock()
        self.fps_cap = 10000
        self.time = 100
        
        self.load_assets()
        
        self.state = 'menu' if not debug else 'game'
        
        self.room_count = (10,10)
        
        self.cached_colors = [
            (255,255,255),
            (255,0,0),
            (0,255,0),
            (0,0,255),
        ]
        
        self.writings = {
            'fps' : Writing(8), 
            'coins' : Writing(12),
            'buffs' : Writing(8),
            'timer': Writing(24),
            'settings' : Writing(18),
        }
        
        self.cache_common_colors()
        
        self.dungeon = Dungeon(self, *self.room_count, 1)
        self.player = Player(self.dungeon.middle_room_pos, 0.1, self.dungeon.middle_room, self)
        self.minimap = Minimap(self, (self.screen.get_width() - 195,20), (175,175))
        self.minimap.feed_rooms(self.dungeon.get_room_list())

        self.minimap.feed_hallways(self.dungeon.hallways)
        
        self.combat_system = CombatSystem(self)
        
        self.scroll = [0,0]
        self.scroll_speed = 60
        self.camera_target = [0, 0]
        
        self.ui_cords= {
            'top' : 0,
            'left' : 0,
            'bottom' : self.display.get_height(),
            'right' : self.display.get_width(),
        }
        
        self.last_time = time()
        
        self.load_all_data()

        self.main_menu_buttons = [
            Button(self,(self.display.get_width()//2 - 50, self.display.get_height()//3 + 50), self.start_game, 'start game', text_color=(255,255,255),custom_text_offset=(-40, -3), size_on_hover=(120, 50), sizeup_speed=1, hover_color=(200, 200, 200), hover_text_color=(15, 50, 120)) ,
            Button(self,(self.display.get_width()//2 - 50, self.display.get_height()//3 + 100), self.goto_settings, 'settings',text_color=(255,255,255), custom_text_offset=(-35, -3), size_on_hover=(120, 50), sizeup_speed=1, hover_color=(200, 200, 200), hover_text_color=(15, 50, 120)) ,
            Button(self,(self.display.get_width()//2 - 50, self.display.get_height()//3 + 150), self.exit_game, 'Quit',text_color=(255,255,255), custom_text_offset=(-18, -3), size_on_hover=(120, 50), sizeup_speed=1, hover_color=(200, 200, 200), hover_text_color=(15, 50, 120)) ,
            ]
        
        self.main_menu_anim = Animation(self.assets['main_menu'])
        self.bat_anim = Animation(self.assets['bat'], 100)
        
        self.cached_outlines = {}
        
        self.fps_choices = MultiSelect(self, ['30', '60', '120', '144', '165', '240', '0'], (200,45), self.fps_cap_choice)
        self.main_menu_button = Button(self,(55, self.display.get_height()//3 + 200), self.goto_main_menu, 'Back', text_color=(255,255,255),custom_text_offset=(-20, -3), size_on_hover=(120, 50), sizeup_speed=1, hover_color=(200, 200, 200), hover_text_color=(15, 50, 120))

        for i in range(4):
            
            self.bat_anim.index = i
            
            img = self.bat_anim.get_image()
            
            self.cached_outlines[img] = outline(img)

        self.mouse_pos = pygame.mouse.get_pos()
        
        self.time_till_close = pygame.time.get_ticks() + 7500
        self.frames = []
        self.performance_testing = False
        
        self.light_width = self.assets['player_light'][self.player.state].get_width()//2 
        self.light_height = self.assets['player_light'][self.player.state].get_height()//2
                
        self.chest_width = self.assets['chest_glow'].get_width()//2 - 40
        self.chest_height = self.assets['chest_glow'].get_height()//2 - 20
        
        self.vignete_cord = (-self.vignette_offset//2,-self.vignette_offset//2)
        
        self.do_lighting = True
        self.show_fps = True
        
        self.started_game = False
        
        self.time_from_start = time()
        
        self.bat_pos = self.generate_bats(8)
        
    def generate_bats(self, n):
        
        bat_pos = [
            (
                randint(0,self.display.get_width()-60),
                randint(0,self.display.get_height()-60),
                ) for i in range(n)
            ]
        
        main_menu_rect = pygame.Rect(self.display.get_width()//2 - 125, 40, self.assets['main_menu'][0].get_width(), self.assets['main_menu'][0].get_height())
        for pos in bat_pos:
            
            test_rect = pygame.Rect(*pos, 60,60)
            
            if main_menu_rect.colliderect(test_rect):
                
               
                
                bat_pos.remove(pos)
                
        return bat_pos
        
    def exit_game(self):
        
        self.save_all_data()
        sys.exit()
        
    def goto_main_menu(self):
        
        self.save_all_data()
        self.state = 'menu'
        
    def draw_text(self, writing:Writing, text:str, pos:(0,0), color=(255,255,255)):
        
        self.display.blit(writing.write(str(text), pygame.Color(color)), pos)
        
    def draw_cursor(self):
        
        draw_lighted_image(self.display, self.assets['mouse_glow'], (
            self.mouse_pos[0] - self.assets['mouse_glow'].get_width()//2,
            self.mouse_pos[1] - self.assets['mouse_glow'].get_height()//2,
                                                                     ))
                
        self.display.blit(self.assets['mouse_png'], (
            self.mouse_pos[0], self.mouse_pos[1] - 2
            ))

    def start_game(self):
        
        self.time_from_start = time()
        self.state = 'game' 
        self.started_game = True
        
    def goto_settings(self):
        
        self.state = 'settings'
        
    def settings(self):
        self.fps_choices.update()
        
        self.draw_text(self.writings['settings'], 'fps limit:', (50, 50))
        self.fps_choices.render(self.display, (0,0))
        
        self.main_menu_button.update()
        self.main_menu_button.animate(self.dt)
        self.main_menu_button.render(self.display)
        
        self.fps_cap = int(self.fps_choices.get_choice())
        
    def main_menu(self):
        self.display.blit(self.writings['fps'].write(str(round(self.clock.get_fps()))+ 'fps', pygame.Color(255,255,255)) , (self.ui_cords['right'] - 45, self.ui_cords['bottom']-8))
        
        self.main_menu_anim.update()
        self.bat_anim.update()
        
        
        for pos in self.bat_pos:
            outline_img = self.cached_outlines[self.bat_anim.get_image()]
            draw_lighted_image(self.display, self.assets['bat_glow'], (pos[0] - 24, pos[1]- 31))
            self.display.blit(self.bat_anim.get_image(),(pos))   
            self.display.blit(outline_img,(pos) )
            
        
        
        self.display.blit(self.main_menu_anim.get_image(),(self.display.get_width()//2 - 125, 40) )   
        
        for button in self.main_menu_buttons:
            
            button.update()
            button.animate(self.dt)
            button.render(self.display)
        
    def cache_common_colors(self):
        
        writing_key_list = list(self.writings.keys())
        
        for key in writing_key_list:
            
            writing = self.writings[key]
            
            for color in self.cached_colors:
                
                writing.cache_full_color(pygame.Color(*color))

    def keep_player_in_rooms(self):
        
        for roomkey in self.dungeon.rooms:
            grid = self.dungeon.rooms[roomkey]
            room = grid[1]
            
            
            if isinstance(room, BlankRoom):
            
                if pygame.math.Vector2(room.rect.center).distance_to(self.player.rect.center) < 1000:
                    
                    if self.player.dx != 0:
                        
                        if room.rect.colliderect(pygame.FRect(self.player.rect.x + self.player.dx , self.player.rect.y, self.player.rect.width, self.player.rect.height)):
                            if self.player.dx > 0:
                                self.player.rect.right = room.rect.left
                            if self.player.dx < 0:
                                self.player.rect.left = room.rect.right
                            self.player.dx = 0
                            
                    if self.player.dy != 0:
                        
                        if room.rect.colliderect(pygame.FRect(self.player.rect.x , self.player.rect.y + self.player.dy, self.player.rect.width, self.player.rect.height)):
                            if self.player.dy > 0:
                                self.player.rect.bottom = room.rect.top
                            if self.player.dy < 0:
                                self.player.rect.top = room.rect.bottom
                            self.player.dy = 0
                        
    def update_ui(self):
        #print(round(self.clock.get_fps()))
        if self.show_fps:
            self.display.blit(self.writings['fps'].write(str(round(self.clock.get_fps()))+ 'fps', pygame.Color(255,255,255)) , (self.ui_cords['right'] - 45, self.ui_cords['bottom']-8))
        
        self.display.blit(self.writings['coins'].write('coins: '+str(self.player.coins), pygame.Color(255,255,0)), (5, 5))
        self.display.blit(self.writings['coins'].write('health: '+str(self.player.hp), pygame.Color(0,250,250)), (5, 20))
        self.display.blit(self.writings['buffs'].write('speed: '+str(int((self.player.powers['speed'] /self.player.speed) * 10) ) + '%', pygame.Color(0,250,250)), (5, 43))
        self.display.blit(self.writings['buffs'].write('damage: '+str(int((self.player.powers['damage'] /self.player.damage) * 100) ) + '%', pygame.Color(0,250,250)), (5, 54))
  
        ttime = str(round(time()-self.time_from_start,1))
        time_surf = self.writings['timer'].write(f"{ttime.split('.')[0]}.{ttime.split('.')[1]}", pygame.Color(255,255,255))
        time_rect = time_surf.get_rect(center = (self.display.get_width()//2, 20))
        
        self.display.blit(time_surf, (time_rect.x, time_rect.y))
  
        # if self.player.inventory.open:
        self.player.inventory.render(self.display)
    
    def _render_sprites(self):
        
        self.dungeon.render_rooms(self.display, self.scroll)
        
        self.dungeon.render_hallways(self.display, self.scroll)
        
        self.dungeon.render_enemies(self.display, self.scroll)
        
        self.dungeon.render_level_block(self.display, self.scroll)
        
        self.dungeon.chest_manager.render_chests(self.display, self.scroll)
        
        self.dungeon.powerup_manager.render_powerups(self.display, self.scroll)
        
        self.player.render(self.display, self.scroll)
        
    def _collisions(self):
        
        self.keep_player_in_rooms()
        self.player.keep_in_locked_room()
        self.player.keep_in_hallway(self.display, self.scroll)
        self.dungeon.enemy_manager.keep_enemies_in(self.player)
        
    def _update_sprites(self):
        
        self.dungeon.update_hallways(self.player)
        self.dungeon.update_rooms()
        self.player.update(self.scroll, self.dt)
        self.dungeon.update_enemies(self.player, self.dt)
        if self.dungeon.update_level_block(self.player) == 'refresh':
            self.dungeon = self.dungeon.copy()
            self.minimap.feed_rooms(self.dungeon.get_room_list())
            self.minimap.feed_hallways(self.dungeon.hallways)
            self.player.set_pos(self.dungeon.middle_room_pos)
            self.save_all_data()
            
        self.dungeon.chest_manager.update_chests(self.player)
        self.dungeon.powerup_manager.update_powerups(self.dt, self.player)
        self.combat_system.update()
        
        self.player.inventory.update(self.dt)
        
    def _move_sprites(self):
        self.player.apply_movement(self.dt)
        self.dungeon.move_enemies(self.dt)
        
    def _lighting(self):
        
        self.assets['darken'].fill((self.darken, self.darken, self.darken))
        
        if not self.player.current_room.type == 'fight' or( self.player.curent_hallway and self.player.curent_hallway.rect.colliderect(self.player.rect)):
            draw_lighted_image(
                self.assets['darken'],
                self.assets['player_light'][self.player.state],
                (
              
                (self.player.render_rect.centerx) - self.light_width,
                (self.player.render_rect.centery) - self.light_height 
          
          
                )
            )
            

            
            
        else:
            draw_lighted_image(
                self.assets['darken'],
                self.assets['room_light'],
                (
                    
                (self.player.current_room.rect.centerx - self.scroll[0]) - self.light_width - self.player.current_room.rect.width // 2 + 0,
                (self.player.current_room.rect.centery - self.scroll[1]) - self.light_height - self.player.current_room.rect.height // 2 
                
                
                )
            )
            
        
        
        self.display.blit(self.assets['darken'], (0,0), special_flags=BLEND_RGB_MULT)
        
        for chest in self.dungeon.chest_manager.chests:
            if self.display.get_rect().colliderect(chest.render_rect) and not chest.opened:
            
                self.display.blit(self.assets['chest_glow'], (chest.rect.centerx - self.scroll[0] - self.chest_width, chest.rect.centery - self.scroll[1] - self.chest_height,), special_flags=BLEND_RGB_ADD)
            
        for powerup in self.dungeon.powerup_manager.powerups:
            
            if self.display.get_rect().colliderect(powerup.render_rect):
                self.display.blit(self.assets['powerup_glow'][type(powerup)], (powerup.rect.centerx - self.scroll[0] - 40, powerup.rect.centery - self.scroll[1] - 40 ,), special_flags=BLEND_RGB_ADD)
        self.display.blit(self.assets['new_level_block_glow'], 
                          
                          (
                              
                              (self.dungeon.next_level_block.render_rect.x - 100,
                              self.dungeon.next_level_block.render_rect.y - 100,)
                           
                           )
                          
                          ,special_flags=BLEND_RGB_ADD)
        
        self.display.blit(self.assets['vignette'], self.vignete_cord )
    
    def update(self):
        
        #self.pause = self.player.inventory.open
        
        self.save_all_every(30000)
        
        self.dt = self.get_dt()
        
        self.mouse_pos = pygame.mouse.get_pos()[0]/ self.zoom, pygame.mouse.get_pos()[1] / self.zoom

        if self.state == 'game':
            
            self.display = self.dis_with_bcg.copy()
            

    
            self._move_sprites()
            
            self._update_sprites()
            
            self._collisions()
            
            self.update_camera()
            
            self._render_sprites()
            
            self.player.render(self.display, self.scroll, False)
            if self.do_lighting:
                self._lighting()

            self.update_ui()
            
        elif self.state == 'menu' :
            
            self.display = self.darker_surf.copy()
            
            self.main_menu()
            
        elif self.state == 'settings':
            
            self.display = self.darker_surf.copy()
            
            self.settings()
            
        self.draw_cursor()
        
        self.screen.blit(pygame.transform.scale(self.display, (self.screen.get_width(),self.screen.get_height())), (0,0)) 
        
            
        self.minimap.render(self.screen, self.player)

        self.scroll_speed = 55 / self.player.powers['speed']
        
    def update_camera(self):
        # calculate the camera's target
        
        if not self.player.current_room.locked:
            target_x = self.player.rect.centerx - self.display.get_width() / 2
            target_y = self.player.rect.centery- self.display.get_height() / 2
        else:
            target_x = self.player.current_room.rect.centerx  - self.display.get_width() / 2
            target_y = self.player.current_room.rect.centery  - self.display.get_height() / 2
        # move the camera
        self.camera_target[0] += ((target_x - self.camera_target[0]) / self.scroll_speed) *self.dt
        self.camera_target[1] += ((target_y - self.camera_target[1]) / self.scroll_speed)*self.dt
        # Apply the camera target position as the scroll position
        
        
        self.scroll[0] = round(self.camera_target[0])
        self.scroll[1] = round(self.camera_target[1])

    def run(self):
        # infinite game loop
        
        run = True
        while run:
            
            # cap the framerate
            
            self.clock.tick(self.fps_cap)
            
            # update everything in the game
            
            self.update()
            
            self.frames.append(self.clock.get_fps())
            
            if pygame.time.get_ticks() > self.time_till_close and debug and self.performance_testing:
                
                print(round(sum(self.frames) / len(self.frames)))
                run = False

            # event handler

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    self.save_all_data()
                    
                    run = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    for button in self.main_menu_buttons:
                        
                        if button.rect.collidepoint(*self.mouse_pos):
                            continue
                        
                        if len(self.bat_pos) > 60:
                            self.bat_pos.remove(self.bat_pos[0])
                    
                        self.bat_pos.append((self.mouse_pos[0]-25, self.mouse_pos[1]-15))
                    
                if event.type == pygame.KEYDOWN:
                    
                    # refresh dungeon
                    if event.key == pygame.K_4:
                        self.do_lighting = not self.do_lighting
                    
                    if event.key == pygame.K_3:
                        
                        self.player.state = 'demontime' if self.player.state == 'regular' else 'regular'
                        
                    if event.key == pygame.K_TAB:
                        
                        self.player.inventory.open = not self.player.inventory.open
                        self.player.inventory.vel = 0
                        
                        self.time = 100 if not self.player.inventory.open else 25
                    
                    if event.key == pygame.K_r:
                        
                        self.dungeon = self.dungeon.copy()
                        self.minimap.feed_rooms(self.dungeon.get_room_list())
                        self.minimap.feed_hallways(self.dungeon.hallways)
                        self.player.set_pos(self.dungeon.middle_room_pos)
                        
                    if event.key == pygame.K_ESCAPE:
                        
                        self.main_menu_buttons[0].text = 'Continue'
                        self.main_menu_buttons[0].cto = (-30, -4)
                        
                        self.goto_main_menu()
                    
                    if event.key == pygame.K_p:
                        
                        self.save_all_data()
                        
                        print('save')
                    
                    if event.key == pygame.K_b:
                        
                        n = randint(8, 25)
                        
                        self.bat_pos = self.generate_bats(n)    
                        
                    if event.key == pygame.K_f:
                        
                        print(self.clock.get_fps())
            # update the screen
            pygame.display.update()
            
    def get_dt(self):
        time_now = time()
        dt = time_now - self.last_time
        dt*=self.time
        self.last_time = time_now

        return dt
            
if __name__ == '__main__':
    t1 = time() 
    game = Game()
    print(f'finished loading in {round(time()- t1, 2)} seconds')

    game.run()
    
    pygame.quit()


print('to alaksa teleios')
