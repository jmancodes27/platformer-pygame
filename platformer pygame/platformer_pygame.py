import pygame
import sys
import time
import math
import random
# part of the code was written with chatgpt(see bottom)
start_time = time.time()
game_time = 0
# for some reason the pygame graph goes like this:
#
#           0
#           _
#           _
#           _
#           _
#0_________500_______1000
#           _
#           _
#           _
#           _
#          1000
#
# Player direction goes like this:
#     0
#  7     1
# 6        2
#  5      3
#     4
#    
#4 is currently not used
pygame.init()
def update_time():
    game_time = time.time() - start_time

# Screen dimensions
WIDTH, HEIGHT = 1200, 600

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

def rotate_image_from_list(List, angle):
    for i in range(len(List)):
        List[i] = pygame.transform.rotate(List[i], angle)
    return List
        
class Obstacle:
    def __init__(self, x, y, width, height):
        self.tile = pygame.image.load("grass.png")
        self.tile = pygame.transform.scale(self.tile, (width, height))
        self.tile_rect = self.tile.get_rect()
        self.tile_rect.x = x
        self.tile_rect.y = y
        self.tile_coli_rect = pygame.Rect(x + 10, y + 7, width - 10, height - 25)

class LaserProjectile:
    def __init__(self, origin_x, origin_y, angle):
        self.projectile = pygame.image.load("laser.png")
        self.projectile = pygame.transform.scale(self.projectile, (int(self.projectile.get_width() * 0.25), int(self.projectile.get_height() * 0.25)))
        if angle == 0:
            self.projectile = pygame.transform.rotate(self.projectile, 90)
        elif angle == 1 or angle == 5:
            self.projectile = pygame.transform.rotate(self.projectile, 45)
        elif angle == 7 or angle == 3:
            self.projectile = pygame.transform.rotate(self.projectile, -45)
        self.projectile_rect = self.projectile.get_rect()
        self.projectile_rect.x = origin_x
        self.projectile_rect.y = origin_y
        self.angle = angle
        self.boss_distance = 0

class Fireball:
    def __init__(self, origin_x, origin_y, angle):
        fireball0 = pygame.image.load("Wizard/FireBallUp/fireball0.png")
        fireball0 = pygame.transform.scale(fireball0, (int(fireball0.get_width() * 2.5), int(fireball0.get_height() * 2.5)))
        fireball1 = pygame.image.load("Wizard/FireBallUp/fireball1.png")
        fireball1 = pygame.transform.scale(fireball1, (int(fireball1.get_width() * 2.5), int(fireball1.get_height() * 2.5)))
        fireball2 = pygame.image.load("Wizard/FireBallUp/fireball2.png")
        fireball2 = pygame.transform.scale(fireball2, (int(fireball2.get_width() * 2.5), int(fireball2.get_height() * 2.5)))
        fireball3 = pygame.image.load("Wizard/FireBallUp/fireball3.png")
        fireball3 = pygame.transform.scale(fireball3, (int(fireball3.get_width() * 2.5), int(fireball3.get_height() * 2.5)))
        self.fireball_frames = [fireball0, fireball1, fireball2, fireball3]
        self.fireball_rect = fireball0.get_rect()
        self.fireball_rect.x = origin_x
        self.fireball_rect.y = origin_y
        self.angle = angle
        for i in range(8):
            if angle == i:
                self.fireball_frames = rotate_image_from_list(self.fireball_frames, i * -45)
                break

class Flag:
    def __init__(self, x, y):
        self.flag = pygame.image.load("flag.png")
        self.flag = pygame.transform.scale(self.flag, (int(self.flag.get_width() * 0.15), int(self.flag.get_height() * 0.15)))
        self.flag_rect = self.flag.get_rect()
        self.flag_rect.x = x
        self.flag_rect.y = y
# potential optemization: have the instance of AirElemental have an int veriable that represents which surface to use
class AirElemental:
    def __init__(self, x, y, target_destination):
        air_elemental_idle_right1 = pygame.image.load("AirElementalIdle/air_idle_right0.png")
        air_elemental_idle_right2 = pygame.image.load("AirElementalIdle/air_idle_right1.png")
        air_elemental_idle_right3 = pygame.image.load("AirElementalIdle/air_idle_right2.png")
        air_elemental_idle_right4 = pygame.image.load("AirElementalIdle/air_idle_right3.png")
        air_elemental_idle_right5 = pygame.image.load("AirElementalIdle/air_idle_right4.png")
        air_elemental_idle_right6 = pygame.image.load("AirElementalIdle/air_idle_right5.png")
        self.air_elemental_idle_right_frames = [air_elemental_idle_right1, air_elemental_idle_right2, air_elemental_idle_right3,
        air_elemental_idle_right4, air_elemental_idle_right5, air_elemental_idle_right6]
        air_elemental_idle_left1 = pygame.image.load("AirElementalIdle/air_idle_left/air_idle_left0.png")
        air_elemental_idle_left2 = pygame.image.load("AirElementalIdle/air_idle_left/air_idle_left1.png")
        air_elemental_idle_left3 = pygame.image.load("AirElementalIdle/air_idle_left/air_idle_left2.png")
        air_elemental_idle_left4 = pygame.image.load("AirElementalIdle/air_idle_left/air_idle_left3.png")
        air_elemental_idle_left5 = pygame.image.load("AirElementalIdle/air_idle_left/air_idle_left4.png")
        air_elemental_idle_left6 = pygame.image.load("AirElementalIdle/air_idle_left/air_idle_left5.png")
        self.air_elemental_idle_left_frames = [air_elemental_idle_left1, air_elemental_idle_left2, air_elemental_idle_left3,
        air_elemental_idle_left4, air_elemental_idle_left5, air_elemental_idle_left6]
        self.elemental_rect = air_elemental_idle_right1.get_rect()
        self.elemental_rect.x = x
        self.elemental_rect.y = y
        self.origin_x = x
        self.origin_y = y
        self.dist_to_plyr = 0
        self.hp = 3
        self.hpcd = 0
        self.chasing = False
        self.target_desti = target_destination
        if x < target_destination:
            self.current_direction = 1
        else:
            self.current_direction = -1

class LightningAttack:
    def __init__(self, x, y):
        lightning0 = pygame.image.load("lightningAttack/lightning0.png")
        lightning0 = pygame.transform.scale(lightning0, (int(lightning0.get_width() * 0.45), int(lightning0.get_height() * 0.45)))
        lightning1 = pygame.image.load("lightningAttack/lightning1.png")
        lightning1 = pygame.transform.scale(lightning1, (int(lightning1.get_width() * 0.45), int(lightning1.get_height() * 0.45)))
        lightning2 = pygame.image.load("lightningAttack/lightning2.png")
        lightning2 = pygame.transform.scale(lightning2, (int(lightning2.get_width() * 0.45), int(lightning2.get_height() * 0.45)))
        lightning3 = pygame.image.load("lightningAttack/lightning3.png")
        lightning3 = pygame.transform.scale(lightning3, (int(lightning3.get_width() * 0.45), int(lightning3.get_height() * 0.45)))
        lightning4 = pygame.image.load("lightningAttack/lightning4.png")
        lightning4 = pygame.transform.scale(lightning4, (int(lightning4.get_width() * 0.45), int(lightning4.get_height() * 0.45)))
        self.frames = [lightning0, lightning1, lightning2, lightning3, lightning4]
        self.lightning_rect = lightning0.get_rect()
        self.lightning_rect.x = x
        self.lightning_rect.y = y
        self.frame_num = 0
        self.frame_counter = 0
current_lightning = []

# Player initializing
player = pygame.image.load("plyr.png")
plyr_width, plyr_height = int(player.get_width() * 0.10), int(player.get_height() * 0.10)
player = pygame.transform.scale(player, (plyr_width, plyr_height))
# kinda unpleasant to look at but not sure how to simplify
# basically loads all the possible rotations of guns into surfaces and scales them
gun_up = pygame.image.load("Up.png")
gun_up = pygame.transform.scale(gun_up, (int(gun_up.get_width() * 0.15), int(gun_up.get_height() * 0.15)))
gun_right_up = pygame.image.load("RightUp.png")
gun_right_up = pygame.transform.scale(gun_right_up, (int(gun_right_up.get_width() * 0.15), int(gun_right_up.get_height() * 0.15)))
gun_right = pygame.image.load("Right.png")
gun_right = pygame.transform.scale(gun_right, (int(gun_right.get_width() * 0.15), int(gun_right.get_height() * 0.15)))
gun_right_down = pygame.image.load("RightDown.png")
gun_right_down = pygame.transform.scale(gun_right_down, (int(gun_right_down.get_width() * 0.15), int(gun_right_down.get_height() * 0.15)))
gun_left_down = pygame.image.load("LeftDown.png")
gun_left_down = pygame.transform.scale(gun_left_down, (int(gun_left_down.get_width() * 0.15), int(gun_left_down.get_height() * 0.15)))
gun_left = pygame.image.load("Left.png")
gun_left = pygame.transform.scale(gun_left, (int(gun_left.get_width() * 0.15), int(gun_left.get_height() * 0.15)))
gun_left_up = pygame.image.load("LeftUp.png")
gun_left_up = pygame.transform.scale(gun_left_up, (int(gun_left_up.get_width() * 0.15), int(gun_left_up.get_height() * 0.15)))

# All boss animations
boss_walk_right0 = pygame.image.load("Wizard/WizardRunRight/wizard_run_right0.png")
boss_walk_right1 = pygame.image.load("Wizard/WizardRunRight/wizard_run_right1.png")
boss_walk_right2 = pygame.image.load("Wizard/WizardRunRight/wizard_run_right2.png")
boss_walk_right3 = pygame.image.load("Wizard/WizardRunRight/wizard_run_right3.png")
boss_walk_right4 = pygame.image.load("Wizard/WizardRunRight/wizard_run_right4.png")
boss_walk_right5 = pygame.image.load("Wizard/WizardRunRight/wizard_run_right5.png")
boss_walk_right6 = pygame.image.load("Wizard/WizardRunRight/wizard_run_right6.png")
boss_walk_right7 = pygame.image.load("Wizard/WizardRunRight/wizard_run_right7.png")
boss_walk_right_frames = [boss_walk_right0, boss_walk_right1, boss_walk_right2, boss_walk_right3, boss_walk_right4, 
boss_walk_right5, boss_walk_right6, boss_walk_right7]

boss_walk_left0 = pygame.image.load("Wizard/WizardRunLeft/wizard_run_left0.png")
boss_walk_left1 = pygame.image.load("Wizard/WizardRunLeft/wizard_run_left1.png")
boss_walk_left2 = pygame.image.load("Wizard/WizardRunLeft/wizard_run_left2.png")
boss_walk_left3 = pygame.image.load("Wizard/WizardRunLeft/wizard_run_left3.png")
boss_walk_left4 = pygame.image.load("Wizard/WizardRunLeft/wizard_run_left4.png")
boss_walk_left5 = pygame.image.load("Wizard/WizardRunLeft/wizard_run_left5.png")
boss_walk_left6 = pygame.image.load("Wizard/WizardRunLeft/wizard_run_left6.png")
boss_walk_left7 = pygame.image.load("Wizard/WizardRunLeft/wizard_run_left7.png")
boss_walk_left_frames = [boss_walk_left0, boss_walk_left1, boss_walk_left2, boss_walk_left3, boss_walk_left4, 
boss_walk_left5, boss_walk_left6, boss_walk_left7]

boss_l_atck0 = pygame.image.load("Wizard/WizardLightningAttack1/wizard_atk0.png")
boss_l_atck1 = pygame.image.load("Wizard/WizardLightningAttack1/wizard_atk1.png")
boss_l_atck2 = pygame.image.load("Wizard/WizardLightningAttack1/wizard_atk2.png")
boss_l_atck3 = pygame.image.load("Wizard/WizardLightningAttack1/wizard_atk3.png")
boss_l_atck4 = pygame.image.load("Wizard/WizardLightningAttack1/wizard_atk4.png")
boss_l_atck5 = pygame.image.load("Wizard/WizardLightningAttack1/wizard_atk5.png")
boss_l_atck6 = pygame.image.load("Wizard/WizardLightningAttack1/wizard_atk6.png")
boss_l_atck7 = pygame.image.load("Wizard/WizardLightningAttack1/wizard_atk7.png")
boss_l_atck_frames = [boss_l_atck0, boss_l_atck1, boss_l_atck2, boss_l_atck3, boss_l_atck4, boss_l_atck5, 
boss_l_atck6, boss_l_atck7]

boss_l_atck_left0 = pygame.image.load("Wizard/WizardLightningAttackLeft1/wizard_lightning_atck_left0.png")
boss_l_atck_left1 = pygame.image.load("Wizard/WizardLightningAttackLeft1/wizard_lightning_atck_left1.png")
boss_l_atck_left2 = pygame.image.load("Wizard/WizardLightningAttackLeft1/wizard_lightning_atck_left2.png")
boss_l_atck_left3 = pygame.image.load("Wizard/WizardLightningAttackLeft1/wizard_lightning_atck_left3.png")
boss_l_atck_left4 = pygame.image.load("Wizard/WizardLightningAttackLeft1/wizard_lightning_atck_left4.png")
boss_l_atck_left5 = pygame.image.load("Wizard/WizardLightningAttackLeft1/wizard_lightning_atck_left5.png")
boss_l_atck_left6 = pygame.image.load("Wizard/WizardLightningAttackLeft1/wizard_lightning_atck_left6.png")
boss_l_atck_left7 = pygame.image.load("Wizard/WizardLightningAttackLeft1/wizard_lightning_atck_left7.png")
boss_l_atck_frames_left = [boss_l_atck_left0, boss_l_atck_left1, boss_l_atck_left2, boss_l_atck_left3, boss_l_atck_left4, 
boss_l_atck_left5, boss_l_atck_left6, boss_l_atck_left7]

boss_p_atck_left0 = pygame.image.load("Wizard/WizardAttack2Left/WizardAttack2Left0.png")
boss_p_atck_left1 = pygame.image.load("Wizard/WizardAttack2Left/WizardAttack2Left1.png")
boss_p_atck_left2 = pygame.image.load("Wizard/WizardAttack2Left/WizardAttack2Left2.png")
boss_p_atck_left3 = pygame.image.load("Wizard/WizardAttack2Left/WizardAttack2Left3.png")
boss_p_atck_left4 = pygame.image.load("Wizard/WizardAttack2Left/WizardAttack2Left4.png")
boss_p_atck_left_frames = [boss_p_atck_left0, boss_p_atck_left1, boss_p_atck_left2, boss_p_atck_left3, boss_p_atck_left4]

boss_p_atck_right0 = pygame.image.load("Wizard/WizardAttack2Right/wizard_attack2_right0.png")
boss_p_atck_right1 = pygame.image.load("Wizard/WizardAttack2Right/wizard_attack2_right1.png")
boss_p_atck_right2 = pygame.image.load("Wizard/WizardAttack2Right/wizard_attack2_right2.png")
boss_p_atck_right3 = pygame.image.load("Wizard/WizardAttack2Right/wizard_attack2_right3.png")
boss_p_atck_right4 = pygame.image.load("Wizard/WizardAttack2Right/wizard_attack2_right4.png")
boss_p_atck_right_frames = [boss_p_atck_right0, boss_p_atck_right1, boss_p_atck_right2, boss_p_atck_right3, boss_p_atck_right4]

boss_s_atck_right0 = pygame.image.load("Wizard/WizardSummonRight/wizard_summon_attack00.png")
boss_s_atck_right1 = pygame.image.load("Wizard/WizardSummonRight/wizard_summon_attack01.png")
boss_s_atck_right2 = pygame.image.load("Wizard/WizardSummonRight/wizard_summon_attack02.png")
boss_s_atck_right3 = pygame.image.load("Wizard/WizardSummonRight/wizard_summon_attack03.png")
boss_s_atck_right4 = pygame.image.load("Wizard/WizardSummonRight/wizard_summon_attack04.png")
boss_s_atck_right5 = pygame.image.load("Wizard/WizardSummonRight/wizard_summon_attack05.png")
boss_s_atck_right6 = pygame.image.load("Wizard/WizardSummonRight/wizard_summon_attack06.png")
boss_s_atck_right7 = pygame.image.load("Wizard/WizardSummonRight/wizard_summon_attack07.png")
boss_s_atck_right8 = pygame.image.load("Wizard/WizardSummonRight/wizard_summon_attack08.png")
boss_s_atck_right9 = pygame.image.load("Wizard/WizardSummonRight/wizard_summon_attack09.png")
boss_s_atck_right10 = pygame.image.load("Wizard/WizardSummonRight/wizard_summon_attack10.png")
boss_s_atck_right11 = pygame.image.load("Wizard/WizardSummonRight/wizard_summon_attack11.png")
boss_s_atck_right12 = pygame.image.load("Wizard/WizardSummonRight/wizard_summon_attack12.png")
boss_s_atck_right13 = pygame.image.load("Wizard/WizardSummonRight/wizard_summon_attack13.png")
boss_s_atck_right14 = pygame.image.load("Wizard/WizardSummonRight/wizard_summon_attack14.png")
boss_s_atck_right15 = pygame.image.load("Wizard/WizardSummonRight/wizard_summon_attack15.png")
boss_s_atck_right_frames = [boss_s_atck_right0, boss_s_atck_right1, boss_s_atck_right2, boss_s_atck_right3, boss_s_atck_right4, 
boss_s_atck_right5, boss_s_atck_right6, boss_s_atck_right7, boss_s_atck_right8, boss_s_atck_right9, boss_s_atck_right10, 
boss_s_atck_right11, boss_s_atck_right12, boss_s_atck_right13, boss_s_atck_right14, boss_s_atck_right15]

bossbar = pygame.image.load("Wizard/wizard_bossbar.png")
bossbar15 = pygame.transform.scale(bossbar, (666, 375))
bossbar14 = pygame.transform.scale(bossbar, (621, 375))
bossbar13 = pygame.transform.scale(bossbar, (576, 375))
bossbar12 = pygame.transform.scale(bossbar, (531, 375))
bossbar11 = pygame.transform.scale(bossbar, (477, 375))
bossbar10 = pygame.transform.scale(bossbar, (432, 375))
bossbar9 = pygame.transform.scale(bossbar, (387, 375))
bossbar8 = pygame.transform.scale(bossbar, (342, 375))
bossbar7 = pygame.transform.scale(bossbar, (297, 375))
bossbar6 = pygame.transform.scale(bossbar, (252, 375))
bossbar5 = pygame.transform.scale(bossbar, (207, 375))
bossbar4 = pygame.transform.scale(bossbar, (162, 375))
bossbar3 = pygame.transform.scale(bossbar, (117, 375))
bossbar2 = pygame.transform.scale(bossbar, (72, 375))
bossbar1 = pygame.transform.scale(bossbar, (28, 375))
bossbar0 = pygame.transform.scale(bossbar, (29, 375))
bossbarbg = pygame.image.load("Wizard/wizard_bossbar_bg.png")
bossbar_list = [bossbarbg, bossbar0, bossbar1, bossbar2, bossbar3, bossbar4, bossbar5, bossbar6, bossbar7, bossbar8, bossbar9, bossbar10, 
bossbar11, bossbar12, bossbar13, bossbar14, bossbar15]

tutorial = pygame.image.load("Wizard/wizard_tutorial.png")
heart = pygame.image.load("Wizard/heart.png")
heart = pygame.transform.scale(heart, (int(heart.get_width() * 0.05), int(heart.get_height() * 0.05)))

flag = pygame.image.load("flag.png")
flag = pygame.transform.scale(flag, (int(flag.get_width() * 0.15), int(flag.get_height() * 0.15)))
flag_rect = flag.get_rect()
game_level = 0
# tile width and height gotten from original width / 10
tile_width = 38
tile_height = 38
# I wish python had arrays :sobbing:
#all boxes in all levels are here
#how to add more levels: add another box list and add the list to all lists list, add more to flag list, 
# same process for boxes for air elementals, you will probably have to change all the if game_level == 6 to 7
box_x_list1 = [1000, 800, 600, 400, 200]
box_y_list1 = [ 500, 400, 300, 200, 100]

box_x_list2 = [1000, 750, 500, 250]
box_y_list2 = [ 400, 450, 500, 550]

box_x_list3 = [200, 250, 350, 400, 750, 800, 650, 477] #kal was here
box_y_list3 = [500, 500, 450, 450, 400, 400, 250, 232]

box_x_list4 = [200, 400, 200, 400, 800, 850]
box_y_list4 = [450, 300, 150,  50, 400, 400]

box_x_list5 = [400, 450, 500, 550, 600,  50, 200, 700, 750, 800, 850, 900, 950, 1000]
box_y_list5 = [350, 400, 400, 400, 350, 500, 400, 250, 300, 300, 300, 250, 250,  250]

box_x_list6 = [200, 300, 200, 400, 450, 500, 550, 600, 650, 700, 750, 800]
box_y_list6 = [450, 400, 300, 250, 300, 300, 300, 300, 250, 200, 200, 200]

box_x_list7 = [100]
box_y_list7 = [500]

box_x_list8 = [250, 300, 300, 350, 450, 500, 550, 550, 550, 500, 450, 450, 650, 650, 650, 700, 750, 750, 750, 200, 225,
              250, 275, 300, 325, 350, 375, 400, 500, 550, 600, 550, 500, 550, 600, 700, 700, 700, 750, 800, 800, 800]
box_y_list8 = [150, 200, 250, 150, 150, 150, 150, 200, 250, 250, 250, 200, 150, 200, 250, 250, 250, 200, 150, 350, 400,
              450, 400, 350, 400, 450, 400, 350, 350, 350, 350, 400, 450, 450, 450, 450, 400, 350, 400, 450, 400, 350]

all_box_x_lists = [box_x_list1, box_x_list2, box_x_list3, box_x_list4, box_x_list5, box_x_list6, box_x_list7, box_x_list8]
all_box_y_lists = [box_y_list1, box_y_list2, box_y_list3, box_y_list4, box_y_list5, box_y_list6, box_y_list7, box_y_list8]
obstacle_list = []
for i in range(len(all_box_x_lists[game_level])):
    obstacle_list.append(Obstacle(all_box_x_lists[game_level][i], all_box_y_lists[game_level][i], tile_width, tile_height))

flag_x_list = [200, 1000, 650, 850, 1000, 800, 100, 100]
flag_y_list = [100,  400, 250, 400,  250, 200, 9999, 9999]

#format: x, y, target
air_elemental_list1 = []
air_elemental_list2 = []
air_elemental_list3 = []
air_elemental_list4 = []
air_elemental_list5 = [400, 300, 550, 700, 200, 850]
air_elemental_list6 = [400, 200, 600, 600, 200, 400]
air_elemental_list7 = []
air_elemental_list8 = []
all_elemental_lists = [air_elemental_list1, air_elemental_list2, air_elemental_list3, 
air_elemental_list4, air_elemental_list5, air_elemental_list6, air_elemental_list7, air_elemental_list8]
current_elementals_list = []
laser_projectiles = []
current_fireballs = []

boss_anim_state = 0
boss_rect = boss_walk_right7.get_rect()
boss_rect.x = 300
boss_rect.y = 400
# 0 is not moving, 1 is moving right, 2 is moving left
boss_direction = 1
boss_ai_on = True
boss_hp_cd = 1000
boss_hp = 15
boss_random_attack_cd = 8000
flag_rect.x = 200
flag_rect.y = 100
player_rect = player.get_rect()
player_rect.center = (1000, 400)
can_jump = True
frame_rate = 180
time_per_frame = 1 / frame_rate
# Set initial movement variables
player_speed = 1
x_velocity = 0
y_velocity = 0
x_velocity_dir = False
player_rect.y = 300
last_time_comped = 0
player_gun_dir = 2
gun_cooldown = 0
air_anim_counter = 0
air_anim_frame = 0
boss_anim_counter1 = 0
boss_anim_frame1 = 0
boss_anim_frame2 = 0
boss_anim_frame3 = 0
boss_anim_frame4 = 0
fireball_anim_frame = 0
debug_level = 6
lightning_frame = 0
boss_target_x = 0
boss_target_y = 0
temp_elemental_count = 0
boss_fireball_counter = 0
tutorial_closed = False
player_health = 5
player_dmg_cd = 0
boss_fight_done = False
# Game loop
running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
  #updates the in game time
  update_time()

  # Handle player movement
  keys = pygame.key.get_pressed()
  if keys[pygame.K_a]:
    if x_velocity > -2.5:
        x_velocity += -0.15
        x_velocity_dir = True
  elif keys[pygame.K_d]:
    if x_velocity < 2.5:
        x_velocity += 0.15
        x_velocity_dir = False
  if keys[pygame.K_w]:
    if y_velocity < 5 and can_jump:
        y_velocity += 5
        player_rect.y -= 5
        can_jump = False
# player direction; see diagram above
  if keys[pygame.K_LEFT]:
      if keys[pygame.K_UP]:
          player_gun_dir = 7
      elif keys[pygame.K_DOWN]:
          player_gun_dir = 5
      else:
          player_gun_dir = 6
  elif keys[pygame.K_RIGHT]:
      if keys[pygame.K_UP]:
          player_gun_dir = 1
      elif keys[pygame.K_DOWN]:
          player_gun_dir = 3
      else:
          player_gun_dir = 2
  elif keys[pygame.K_UP]:
      player_gun_dir = 0

  if keys[pygame.K_y] and not game_level == debug_level:
      print("user cheated to move level forward")
      game_level = debug_level
      obstacle_list.clear()
      for i in range(len(all_box_x_lists[game_level])):
          obstacle_list.append(Obstacle(all_box_x_lists[game_level][i], all_box_y_lists[game_level][i], tile_width, tile_height))
      for i in range(int(len(all_elemental_lists[game_level]) / 3)):
          current_elementals_list.append(AirElemental(all_elemental_lists[game_level][i * 3], all_elemental_lists[game_level][i * 3 + 1], all_elemental_lists[game_level][i * 3 + 2]))
          print(f"made a new elemental with {all_elemental_lists[game_level][i*3]} x, {all_elemental_lists[game_level][(i*3) + 1]} y, {all_elemental_lists[game_level][(i*3) + 2]} target x.")
      flag_rect.x = flag_x_list[game_level]
      flag_rect.y = flag_y_list[game_level]
  if keys[pygame.K_u]:
      print(current_elementals_list[1].elemental_rect.y)
  if keys[pygame.K_b]:
      if len(current_lightning) < 1:
          boss_anim_state = 1
          boss_anim_frame2 = 0
          boss_target_x = player_rect.x
          boss_target_y = player_rect.y
  if keys[pygame.K_n] and boss_anim_state != 2:
      boss_anim_state = 2
      boss_fireball_counter = 0
      boss_anim_frame3 = 0 #issue: might be immediately increased after this
      boss_rect.y += 100
      #Dived into three equal sections where the player could be. If in middle section, move wizard to either end of screen
      #if in either end sections, but wizard in middle
      if player_rect.x < 400 or player_rect.x > 800:
          boss_rect.x = 600 #puts boss in middle
      else:
          if player_rect.x > 600:
              boss_rect.x = 0
          else:
              boss_rect.x = 1100
  if keys[pygame.K_m] and boss_anim_state != 3:
      boss_anim_state = 3
      boss_anim_frame4 = 0
  if keys[pygame.K_o]:
      boss_random_attack_cd = 1000000
  if keys[pygame.K_p]:
      boss_random_attack_cd = 5
  if keys[pygame.K_z] and game_level == 6:
      tutorial_closed = True
      boss_random_attack_cd = 100
  print(boss_random_attack_cd)
  # if player presses space create new instance of LaserProjectile at player x and y
  # in at the angle of gun
  if keys[pygame.K_SPACE] or keys[pygame.K_q]:
      if gun_cooldown <= 0:
        laser_projectiles.append(LaserProjectile(player_rect.x, player_rect.y, player_gun_dir))
        gun_cooldown = 25
  # loops consistantly
  if last_time_comped != round(time.time(), 2):
      # handles physics
      plyr_coli_rect = pygame.Rect(player_rect.x, player_rect.y, 50, 50)
      player_rect.y -= y_velocity
      if player_rect.y > 550:
          player_rect.y = 550
          y_velocity = 0
          can_jump = True
      else:
          y_velocity -= 0.1

      player_rect.x += x_velocity
      if x_velocity > 0:
          x_velocity -= 0.1
      elif x_velocity < 0:
          x_velocity += 0.1
      # handles collisions
      for i in range(len(obstacle_list)):
        if plyr_coli_rect.colliderect(obstacle_list[i].tile_coli_rect):
            if player_rect.y > obstacle_list[i].tile_rect.y + 0 + 7:
                player_rect.y = obstacle_list[i].tile_rect.y + 20 + 7
                y_velocity = 0
                print("plyr hit bottom")
            elif player_rect.y > obstacle_list[i].tile_rect.y - 30 - 7:
                player_rect.y = obstacle_list[i].tile_rect.y - 30 - 7
                y_velocity = 0
                print("plyr fell too far")
            else:
                y_velocity = 0
                can_jump = True

      if plyr_coli_rect.colliderect(flag_rect):
          if player_rect.y < flag_rect.y + 5 and player_rect.y > flag_rect.y - 50:
            print("coli with flag")
            game_level += 1
            obstacle_list.clear()
            for i in range(len(all_box_x_lists[game_level])):
                obstacle_list.append(Obstacle(all_box_x_lists[game_level][i], all_box_y_lists[game_level][i], tile_width, tile_height))
            for i in range(int(len(all_elemental_lists[game_level]) / 3)):
                current_elementals_list.append(AirElemental(all_elemental_lists[game_level][i * 3], all_elemental_lists[game_level][i * 3 + 1], all_elemental_lists[game_level][i * 3 + 2]))
                print(f"made a new elemental with {all_elemental_lists[game_level][i*3]} x, {all_elemental_lists[game_level][(i*3) + 1]} y, {all_elemental_lists[game_level][(i*3) + 2]} target x.")
            y_velocity -= 10
            flag_rect.x = flag_x_list[game_level]
            flag_rect.y = flag_y_list[game_level]
      for i in range(len(laser_projectiles)):
          for o in range(len(current_elementals_list)):
              if laser_projectiles[i].projectile_rect.colliderect(current_elementals_list[o].elemental_rect):
                  print("you hit the air elemental!")
                  if current_elementals_list[o].hpcd < 1:
                      if current_elementals_list[o].hp > 0:
                        current_elementals_list[o].hp -= 1
                        current_elementals_list[o].hpcd = 60
                      else:
                          del current_elementals_list[o]
                          break
      #handles animation frame and cooldown counting
      if player_dmg_cd > 0:
          player_dmg_cd -= 1
      lightning_frame += 1
      if lightning_frame == 5:
        for i in range(len(current_lightning)):
            current_lightning[i].frame_num += 1
        lightning_frame = 0
      if gun_cooldown > 0:
        gun_cooldown -= 1
      if air_anim_counter < 10:
          air_anim_counter += 1
      else:
          air_anim_counter = 0 
          air_anim_frame += 1
          boss_anim_frame1 += 1
          boss_anim_frame2 += 1
          boss_anim_frame3 += 1
          boss_anim_frame4 += 1
          fireball_anim_frame += 1
          if air_anim_frame == 6:
              air_anim_frame = 0
          if boss_anim_frame1 == 7:
              boss_anim_frame1 = 0
          if boss_anim_frame2 == 9:
              boss_anim_frame2 = 0
          if fireball_anim_frame == 4:
              fireball_anim_frame = 0  
          if boss_anim_frame3 == 5:
              boss_anim_frame3 = 0
          if boss_anim_frame4 == 55:
              boss_anim_frame4 = 0
      for i in range(len(current_elementals_list)):
          if current_elementals_list[i].hpcd > 0:
              current_elementals_list[i].hpcd -= 1
      # for loop that handles most elemental things
      for i in range(int(len(current_elementals_list))):
          if not current_elementals_list[i].chasing:
              if not current_elementals_list[i].elemental_rect.x == current_elementals_list[i].target_desti:
                  if current_elementals_list[i].target_desti - current_elementals_list[i].origin_x > 0:
                      current_elementals_list[i].elemental_rect.x += 1
                      current_elementals_list[i].current_direction = 1
                  else:
                      current_elementals_list[i].elemental_rect.x -= 1
                      current_elementals_list[i].current_direction = -1
              else:
                  temp_var = current_elementals_list[i].origin_x
                  current_elementals_list[i].origin_x = current_elementals_list[i].target_desti
                  current_elementals_list[i].target_desti = temp_var
          current_elementals_list[i].dist_to_plyr = math.sqrt((abs(current_elementals_list[i].elemental_rect.x - player_rect.x - 20) ** 2) + (abs(current_elementals_list[i].elemental_rect.y - player_rect.y - 25) ** 2))
          if current_elementals_list[i].dist_to_plyr < 215:
              print("air elemental sees you!")
              current_elementals_list[i].chasing = True
          if current_elementals_list[i].chasing:
              temp_var1 = ((current_elementals_list[i].elemental_rect.x - player_rect.x) ** 2 + (current_elementals_list[i].elemental_rect.y - player_rect.y) ** 2) / 15 ** 2 + 0.001
              current_elementals_list[i].elemental_rect.x -= (current_elementals_list[i].elemental_rect.x - player_rect.x) / temp_var1
              current_elementals_list[i].elemental_rect.y -= (current_elementals_list[i].elemental_rect.y - player_rect.y) / temp_var1
              if current_elementals_list[i].dist_to_plyr < 60:
                  print("the elemental got you")
                  if game_level == 6:
                      if player_dmg_cd == 0:
                          player_health -= 1
                          player_dmg_cd = 100
                  else:
                      game_level -= 1
                      obstacle_list.clear()
                      for i in range(len(all_box_x_lists[game_level])):
                          obstacle_list.append(Obstacle(all_box_x_lists[game_level][i], all_box_y_lists[game_level][i], tile_width, tile_height))
                      for i in range(int(len(all_elemental_lists[game_level]) / 3)):
                          current_elementals_list.append(AirElemental(all_elemental_lists[game_level][i * 3], all_elemental_lists[game_level][(i * 3) + 1], all_elemental_lists[game_level][(i * 3) + 2]))
                      flag_rect.x = flag_x_list[game_level]
                      flag_rect.y = flag_y_list[game_level]
                      current_elementals_list.clear()
                      break
      #boss logic(some of it)
      if boss_hp_cd > 0:
          boss_hp_cd -= 1
      if boss_rect.y > 600:
          boss_rect.y = 300
      if boss_random_attack_cd > 0 and game_level == 6:
          boss_random_attack_cd -= 1
      if boss_random_attack_cd == 0:
          boss_anim_state = random.randint(1, 3)
          boss_random_attack_cd = 1000
          if boss_anim_state == 1:
              boss_anim_frame2 = 0
              boss_target_x = player_rect.x
              boss_target_y = player_rect.y
          elif boss_anim_state == 2:
              boss_fireball_counter = 0
              boss_anim_frame3 = 0 #issue: might be immediately increased after this
              boss_rect.y += 100
              #Dived into three equal sections where the player could be. If in middle section, move wizard to either end of screen
              #if in either end sections, but wizard in middle
              if player_rect.x < 400 or player_rect.x > 800:
                  boss_rect.x = 600 #puts boss in middle
              else:
                  if player_rect.x > 600:
                      boss_rect.x = 0
                  else:
                      boss_rect.x = 1100
          elif boss_anim_state == 3:
              boss_anim_frame4 = 0
      boss_player_distance = math.sqrt((abs(boss_rect.x - player_rect.x - 0) ** 2) + (abs(boss_rect.y - player_rect.y - 0) ** 2))
      boss_movement_var = ((boss_rect.x - player_rect.x) ** 2 + (boss_rect.y - player_rect.y) ** 2) / 45 ** 2
      if boss_player_distance > 400 and boss_anim_state == 0:
          boss_rect.x -= (boss_rect.x - player_rect.x) / boss_movement_var
          boss_rect.y -= (boss_rect.y - player_rect.y) / boss_movement_var
      if boss_player_distance < 200 and boss_anim_state == 0:
          boss_rect.x += (boss_rect.x - player_rect.x) / boss_movement_var
          boss_rect.y += (boss_rect.y - player_rect.y) / boss_movement_var
      if abs((boss_rect.x - player_rect.x) / boss_movement_var) == ((boss_rect.x - player_rect.x) / boss_movement_var):
          boss_direction = 2 #left
      else:
          boss_direction = 1 # right
      #doges bullets 
      for i in range(len(laser_projectiles)):
          #doges bullets
          if math.sqrt((abs(boss_rect.x - laser_projectiles[i].projectile_rect.x - 0) ** 2) + (abs(boss_rect.y - laser_projectiles[i].projectile_rect.y - 0) ** 2)) < 100:
              if boss_anim_state == 3:
                  if boss_hp_cd == 0:
                      boss_hp -= 1
                      boss_hp_cd = 75
              else:
                  boss_rect.x += random.randint(-200, 200)
                  boss_rect.y -= random.randint(-200, 200)
          laser_projectiles[i].boss_distance = math.sqrt((abs(boss_rect.x - laser_projectiles[i].projectile_rect.x - 0) ** 2) + (abs(boss_rect.y - laser_projectiles[i].projectile_rect.y - 0) ** 2))
      for i in range(len(current_lightning)):
          if current_lightning[i].lightning_rect.x + 25 > player_rect.x and current_lightning[i].lightning_rect.x - 25 < player_rect.x:
              if player_dmg_cd == 0:
                  player_health -= 1
                  player_dmg_cd = 100
              
      last_time_comped = round(time.time(), 2)
    #removes a laser projectile if it is too far away
  for i in range(len(laser_projectiles)):
      if abs(laser_projectiles[i].projectile_rect.x) + abs(laser_projectiles[i].projectile_rect.y) > 1800:
          del laser_projectiles[i]
          break
  # handles fireballs and lasers
  for i in range(len(current_fireballs)):
      if current_fireballs[i].angle == 2:
          current_fireballs[i].fireball_rect.x += 4
      elif current_fireballs[i].angle == 6:
          current_fireballs[i].fireball_rect.x -= 4
  for i in range(len(laser_projectiles)):
      if laser_projectiles[i].angle == 0:
          laser_projectiles[i].projectile_rect.y -= 10
      if laser_projectiles[i].angle == 1:
          laser_projectiles[i].projectile_rect.y -= 5
          laser_projectiles[i].projectile_rect.x += 5
      if laser_projectiles[i].angle == 2:
          laser_projectiles[i].projectile_rect.x += 10
      if laser_projectiles[i].angle == 3:
          laser_projectiles[i].projectile_rect.y += 5
          laser_projectiles[i].projectile_rect.x += 5
      if laser_projectiles[i].angle == 5:
          laser_projectiles[i].projectile_rect.y += 5
          laser_projectiles[i].projectile_rect.x -= 5
      if laser_projectiles[i].angle == 6:
          laser_projectiles[i].projectile_rect.x -= 10
      if laser_projectiles[i].angle == 7:
          laser_projectiles[i].projectile_rect.y -= 5
          laser_projectiles[i].projectile_rect.x -= 5
  for i in range(len(current_fireballs)):
      if player_rect.x < current_fireballs[i].fireball_rect.x + 75 and player_rect.x > current_fireballs[i].fireball_rect.x - 75:
          if player_rect.y < current_fireballs[i].fireball_rect.y + 25 and player_rect.y > current_fireballs[i].fireball_rect.y - 25:
              if player_dmg_cd == 0:
                  player_dmg_cd = 100
                  player_health -= 1
  if player_health == 0:
      print("You died L")
  screen.fill((0, 0, 0)) 
  #drawing everything on the screen
  frame_start_time = time.time()
  screen.blit(player, player_rect)
  for i in range(len(current_elementals_list)):
      if current_elementals_list[i].current_direction == 1:
          screen.blit(current_elementals_list[i].air_elemental_idle_right_frames[air_anim_frame], (current_elementals_list[i].elemental_rect.x, current_elementals_list[i].elemental_rect.y))
      else:
          screen.blit(current_elementals_list[i].air_elemental_idle_left_frames[air_anim_frame], (current_elementals_list[i].elemental_rect.x, current_elementals_list[i].elemental_rect.y))
  for i in range(len(obstacle_list)):
    screen.blit(obstacle_list[i].tile, (obstacle_list[i].tile_rect.x, obstacle_list[i].tile_rect.y))
  if player_gun_dir == 0:
      screen.blit(gun_up, (player_rect.x + 5, player_rect.y - 33))
  if player_gun_dir == 1:
      screen.blit(gun_right_up, (player_rect.x + 15, player_rect.y - 25))
  if player_gun_dir == 2:
      screen.blit(gun_right, (player_rect.x + 21, player_rect.y))
  if player_gun_dir == 3:
      screen.blit(gun_right_down, (player_rect.x + 13, player_rect.y + 15))
  if player_gun_dir == 5:
      screen.blit(gun_left_down, (player_rect.x - 28, player_rect.y + 15))
  if player_gun_dir == 6:
      screen.blit(gun_left, (player_rect.x - 32, player_rect.y))
  if player_gun_dir == 7:
      screen.blit(gun_left_up, (player_rect.x - 17, player_rect.y - 27))
  for i in range(len(laser_projectiles)):
      screen.blit(laser_projectiles[i].projectile, (laser_projectiles[i].projectile_rect.x, laser_projectiles[i].projectile_rect.y))
  screen.blit(flag, (flag_rect.x + 16, flag_rect.y - 79))
  #the rest of boss logic
  if boss_hp <= 0 and not boss_fight_done:
      print("you win! YAYY")
      game_level = 7
      obstacle_list.clear()
      for i in range(len(all_box_x_lists[game_level])):
          obstacle_list.append(Obstacle(all_box_x_lists[game_level][i], all_box_y_lists[game_level][i], tile_width, tile_height))
      for i in range(int(len(all_elemental_lists[game_level]) / 3)):
          current_elementals_list.append(AirElemental(all_elemental_lists[game_level][i * 3], all_elemental_lists[game_level][i * 3 + 1], all_elemental_lists[game_level][i * 3 + 2]))
          print(f"made a new elemental with {all_elemental_lists[game_level][i*3]} x, {all_elemental_lists[game_level][(i*3) + 1]} y, {all_elemental_lists[game_level][(i*3) + 2]} target x.")
      y_velocity -= 10
      flag_rect.x = flag_x_list[game_level]
      flag_rect.y = flag_y_list[game_level]
      boss_fight_done = True
  if game_level == 6:
      if boss_anim_state == 0:
          if boss_direction == 1:
              screen.blit(boss_walk_right_frames[boss_anim_frame1], boss_rect)
          elif boss_direction == 2:
              screen.blit(boss_walk_left_frames[boss_anim_frame1], boss_rect)
          elif boss_direction == 0:
              screen.blit(boss_walk_right_frames[0], boss_rect)
      elif boss_anim_state == 1:
          if boss_anim_frame2 == 8:
              boss_anim_frame2 = 0
              boss_anim_state = 0
              current_lightning.append(LightningAttack(boss_target_x, boss_target_y))
          else:
              if boss_direction == 1:
                  screen.blit(boss_l_atck_frames[boss_anim_frame2], boss_rect)
              if boss_direction == 2:
                  screen.blit(boss_l_atck_frames_left[boss_anim_frame2], boss_rect)
      elif boss_anim_state == 2:
          if boss_direction == 1:
              screen.blit(boss_p_atck_right_frames[boss_anim_frame3], boss_rect)
          elif boss_direction == 2:
              screen.blit(boss_p_atck_left_frames[boss_anim_frame3], boss_rect)
          if boss_fireball_counter == 0:
              if boss_anim_frame3 == 4:
                  if boss_direction == 1:
                      current_fireballs.append(Fireball(boss_rect.x, boss_rect.y, 2))
                  elif boss_direction == 2:
                      current_fireballs.append(Fireball(boss_rect.x, boss_rect.y, 6))
                  boss_fireball_counter = 0.5
                  boss_rect.y -= 50
          if boss_fireball_counter == 0.5 and boss_anim_frame3 == 0:
              boss_fireball_counter = 1
          if boss_fireball_counter == 1:
              if boss_anim_frame3 == 4:
                  if boss_direction == 1:
                      current_fireballs.append(Fireball(boss_rect.x, boss_rect.y, 2))
                  elif boss_direction == 2:
                      current_fireballs.append(Fireball(boss_rect.x, boss_rect.y, 6))
                  boss_fireball_counter = 1.5
                  boss_rect.y -= 50
          if boss_fireball_counter == 1.5 and boss_anim_frame3 == 0:
              boss_fireball_counter = 2
          if boss_fireball_counter == 2:
              if boss_anim_frame3 == 4:
                  if boss_direction == 1:
                      current_fireballs.append(Fireball(boss_rect.x, boss_rect.y, 2))
                  elif boss_direction == 2:
                      current_fireballs.append(Fireball(boss_rect.x, boss_rect.y, 6))
                  boss_fireball_counter = 2.5
                  boss_rect.y -= 50
          if boss_fireball_counter == 2.5 and boss_anim_frame3 == 0:
              boss_fireball_counter = 3
          if boss_fireball_counter == 3:
              if boss_anim_frame3 == 4:
                  if boss_direction == 1:
                      current_fireballs.append(Fireball(boss_rect.x, boss_rect.y, 2))
                  elif boss_direction == 2:
                      current_fireballs.append(Fireball(boss_rect.x, boss_rect.y, 6))
                  boss_fireball_counter = 3.5
                  boss_rect.y -= 50
          if boss_fireball_counter == 3.5 and boss_anim_frame3 == 0:
              boss_fireball_counter = 4
          if boss_fireball_counter == 4:
              if boss_anim_frame3 == 4:
                  if boss_direction == 1:
                      current_fireballs.append(Fireball(boss_rect.x, boss_rect.y, 2))
                  elif boss_direction == 2:
                      current_fireballs.append(Fireball(boss_rect.x, boss_rect.y, 6))
                  boss_fireball_counter = 0
                  boss_anim_state = 0
      if boss_anim_state == 3:
          if boss_anim_frame4 > 15:
              screen.blit(boss_s_atck_right_frames[15], boss_rect)
          else:
              screen.blit(boss_s_atck_right_frames[boss_anim_frame4], boss_rect)
          if boss_anim_frame4 == 11 and temp_elemental_count == 0:
              current_elementals_list.append(AirElemental(player_rect.x - 220, player_rect.y, player_rect.x))
              temp_elemental_count += 1
          if boss_anim_frame4 == 12 and temp_elemental_count == 1:
              current_elementals_list.append(AirElemental(player_rect.x - 220, player_rect.y, player_rect.x))
              temp_elemental_count = 0
          if boss_anim_frame4 == 54:
              boss_anim_state = 0
      screen.blit(bossbarbg, (300, -100))
      screen.blit(bossbar_list[boss_hp + 1], (300, -100))
  for i in range(len(current_lightning)):
      if current_lightning[i].frame_num > 4:
          del current_lightning[0]
          break
      screen.blit(current_lightning[i].frames[current_lightning[i].frame_num], (current_lightning[i].lightning_rect.x - 10, current_lightning[i].lightning_rect.y - 300))
  for i in range(len(current_fireballs)):
      screen.blit(current_fireballs[i].fireball_frames[fireball_anim_frame], current_fireballs[i].fireball_rect)
  if not tutorial_closed and game_level == 6:
      screen.blit(tutorial, (0, 0))
  if player_health >= 5:
      screen.blit(heart, (1150, 550))
  if player_health >= 4:
      screen.blit(heart, (1100, 550))
  if player_health >= 3:
      screen.blit(heart, (1050, 550))
  if player_health >= 2:
      screen.blit(heart, (1000, 550))
  if player_health >= 1:
      screen.blit(heart, (950, 550))
  if game_level == 6 and player_health == 0:
      running = False
  frame_time = time.time() - frame_start_time
  if frame_time < time_per_frame:
    time.sleep(time_per_frame - frame_time)
 # Update the display
  pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()


# credits:
# Heroes of might and magic 3 for the wizard and air elemental animations
# Minecraft for heart png
# Metal Slug 3 for fireball
# Romance of the Three Kingdoms VIII for lightning animation
# ChatGPT for basic pygame initializing setting up both loops
# Sawyer for help with code
# Chris, Chris, Aditya and everyone else for playtesting