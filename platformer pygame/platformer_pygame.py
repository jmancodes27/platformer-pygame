import pygame
import sys
import time
import math
# part of the code was written with chatgpt
start_time = time.time()
game_time = 0

# Initialize Pygame
pygame.init()
def update_time():
    game_time = time.time() - start_time

# Screen dimensions
WIDTH, HEIGHT = 1200, 600

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

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
class Flag:
    def __init__(self, x, y):
        self.flag = pygame.image.load("flag.png")
        self.flag = pygame.transform.scale(self.flag, (int(self.flag.get_width() * 0.15), int(self.flag.get_height() * 0.15)))
        self.flag_rect = self.flag.get_rect()
        self.flag_rect.x = x
        self.flag_rect.y = y
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
        self.target_desti = target_destination
        if x < target_destination:
            self.current_direction = 1
        else:
            self.current_direction = -1
        
# Load the player sprite (yellow box) and scale it down
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

air_elemental_idle_right1 = pygame.image.load("AirElementalIdle/air_idle_right0.png")
air_elemental_idle_right2 = pygame.image.load("AirElementalIdle/air_idle_right1.png")
air_elemental_idle_right3 = pygame.image.load("AirElementalIdle/air_idle_right2.png")
air_elemental_idle_right4 = pygame.image.load("AirElementalIdle/air_idle_right3.png")
air_elemental_idle_right5 = pygame.image.load("AirElementalIdle/air_idle_right4.png")
air_elemental_idle_right6 = pygame.image.load("AirElementalIdle/air_idle_right5.png")
air_elemental_idle_right_frames = [air_elemental_idle_right1, air_elemental_idle_right2, air_elemental_idle_right3,
air_elemental_idle_right4, air_elemental_idle_right5, air_elemental_idle_right6]

air_elemental_idle_left1 = pygame.image.load("AirElementalIdle/air_idle_left/air_idle_left0.png")
air_elemental_idle_left2 = pygame.image.load("AirElementalIdle/air_idle_left/air_idle_left1.png")
air_elemental_idle_left3 = pygame.image.load("AirElementalIdle/air_idle_left/air_idle_left2.png")
air_elemental_idle_left4 = pygame.image.load("AirElementalIdle/air_idle_left/air_idle_left3.png")
air_elemental_idle_left5 = pygame.image.load("AirElementalIdle/air_idle_left/air_idle_left4.png")
air_elemental_idle_left6 = pygame.image.load("AirElementalIdle/air_idle_left/air_idle_left5.png")
air_elemental_idle_left_frames = [air_elemental_idle_left1, air_elemental_idle_left2, air_elemental_idle_left3,
air_elemental_idle_left4, air_elemental_idle_left5, air_elemental_idle_left6]


# loads the flag ito surface
flag = pygame.image.load("flag.png")
flag = pygame.transform.scale(flag, (int(flag.get_width() * 0.15), int(flag.get_height() * 0.15)))
flag_rect = flag.get_rect()
flag_rect.x = 200
flag_rect.y = 100
# tile width and height gotten from original width / 10
tile_width = 38
tile_height = 38
player_rect = player.get_rect()
player_rect.center = (1000, 400)
can_jump = True
game_level = 0
frame_rate = 180
time_per_frame = 1 / frame_rate
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

# I wish python had arrays :sobbing:
# box 1 : 1000, 500
# box 2 : 800, 400
# box 3 : 
box_x_list1 = [1000, 800, 600, 400, 200]
box_y_list1 = [ 500, 400, 300, 200, 100]

box_x_list2 = [1000, 750, 500, 250]
box_y_list2 = [ 400, 450, 500, 550]

box_x_list3 = [200, 250, 350, 400, 750, 800, 650]
box_y_list3 = [500, 500, 450, 450, 400, 400, 250]

box_x_list4 = [200, 400, 200, 400, 800, 850]
box_y_list4 = [450, 300, 150,  50, 400, 400]

box_x_list5 = [400, 450, 500, 550, 600,  50, 200]
box_y_list5 = [350, 400, 400, 400, 350, 500, 400]
all_box_x_lists = [box_x_list1, box_x_list2, box_x_list3, box_x_list4, box_x_list5]
all_box_y_lists = [box_y_list1, box_y_list2, box_y_list3, box_y_list4, box_y_list5]
obstacle_list = []
for i in range(len(all_box_x_lists[game_level])):
    obstacle_list.append(Obstacle(all_box_x_lists[game_level][i], all_box_y_lists[game_level][i], tile_width, tile_height))

flag_x_list = [200, 1000, 650, 850, 0]
flag_y_list = [100,  400, 250, 400, 9999]

#format: x, y, target
air_elemental_list1 = []
air_elemental_list2 = []
air_elemental_list3 = []
air_elemental_list4 = []
air_elemental_list5 = [400, 300, 550]
all_elemental_lists = [air_elemental_list1, air_elemental_list2, air_elemental_list3, 
air_elemental_list4, air_elemental_list5]
current_elementals_list = []
laser_projectiles = []

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
        print("a is going")
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
          print("pressed")
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
  # if player presses space create new instance of LaserProjectile at player x and y
  # in at the angle of gun
  #BUG1
  if keys[pygame.K_SPACE]:
      if gun_cooldown <= 0:
        laser_projectiles.append(LaserProjectile(player_rect.x, player_rect.y, player_gun_dir))
        gun_cooldown = 25
  
  # loops consistantly
  if last_time_comped != round(time.time(), 2):
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
                current_elementals_list.append(AirElemental(all_elemental_lists[game_level][i], all_elemental_lists[game_level][i + 1], all_elemental_lists[game_level][i + 2]))
            flag_rect.x = flag_x_list[game_level]
            flag_rect.y = flag_y_list[game_level]

      if gun_cooldown > 0:
        gun_cooldown -= 1
      if air_anim_counter < 10:
          air_anim_counter += 1
      else:
          air_anim_counter = 0 
          air_anim_frame += 1
          if air_anim_frame == 6:
              air_anim_frame = 0
      #moves the elementals on the screen to where they should go
      for i in range(int(len(current_elementals_list))):
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
          current_elementals_list[i].dist_to_plyr = math.sqrt((abs(current_elementals_list[i].elemental_rect.x - player_rect.x) ** 2) + (abs(current_elementals_list[i].elemental_rect.y - player_rect.y) ** 2))
          if current_elementals_list[i].dist_to_plyr < 200:
              print("air elemental sees you!")
      last_time_comped = round(time.time(), 2)
    #removes a laser projectile if it is too far away
  for i in range(len(laser_projectiles)):
      if abs(laser_projectiles[i].projectile_rect.x) + abs(laser_projectiles[i].projectile_rect.y) > 1800:
          del laser_projectiles[i]
          break
  for i in range(len(laser_projectiles)):
      if laser_projectiles[i].angle == 0:
          laser_projectiles[i].projectile_rect.y -= 4
      if laser_projectiles[i].angle == 1:
          laser_projectiles[i].projectile_rect.y -= 2
          laser_projectiles[i].projectile_rect.x += 2
      if laser_projectiles[i].angle == 2:
          laser_projectiles[i].projectile_rect.x += 4
      if laser_projectiles[i].angle == 3:
          laser_projectiles[i].projectile_rect.y += 2
          laser_projectiles[i].projectile_rect.x += 2
      if laser_projectiles[i].angle == 5:
          laser_projectiles[i].projectile_rect.y += 2
          laser_projectiles[i].projectile_rect.x -= 2
      if laser_projectiles[i].angle == 6:
          laser_projectiles[i].projectile_rect.x -= 4
      #BUG1
      if laser_projectiles[i].angle == 7:
          laser_projectiles[i].projectile_rect.y -= 1
          laser_projectiles[i].projectile_rect.x -= 1
  # Clear the screen
  screen.fill((0, 0, 0))

  # Draw the player
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


  #if game_level == 4:
    #screen.blit(air_elemental_idle_right1, (400, 300))
    #screen.blit(air_elemental_idle_right_frames[air_anim_frame], (400, 300))
  frame_time = time.time() - frame_start_time
  if frame_time < time_per_frame:
    time.sleep(time_per_frame - frame_time)
 # Update the display
  pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()


