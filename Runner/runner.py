import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
   def __init__(self):
      super().__init__()
      player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
      player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
      self.player_walk = [player_walk_1, player_walk_2]
      self.player_index = 0
      self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

      self.image = self.player_walk[self.player_index]
      self.rect = self.image.get_rect(midbottom=(200, 300))
      self.gravity = 0

      self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
      self.jump_sound.set_volume(0.1)
   def player_input(self):
      keys = pygame.key.get_pressed()
      if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
         self.gravity = -20
         self.jump_sound.play()

   def apply_gravity(self):
      self.gravity += 1
      self.rect.y += self.gravity
      if self.rect.bottom >= 300:
         self.rect.bottom = 300

   def animation_state(self):
      if self.rect.bottom < 300:
         self.image = self.player_jump
      else:
         self.player_index += 0.1
         if self.player_index >= len(self.player_walk):
            self.player_index = 0
         self.image = self.player_walk[int(self.player_index)]

   def update(self):
      self.player_input()
      self.apply_gravity()
      self.animation_state()

class Obstacle(pygame.sprite.Sprite):
   def __init__(self,type):
      super().__init__()

      if type == 'fly':
         fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
         fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
         self.frames = [fly_1, fly_2]
         y_pos = 210
      else:
         snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
         snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
         self.frames = [snail_1, snail_2]
         y_pos  = 300

      self.animation_index = 0
      self.image = self.frames[self.animation_index]
      self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

   def animation_state(self):
      self.animation_index += 0.1
      if self.animation_index >= len(self.frames):
         self.animation_index = 0
      self.image = self.frames[int(self.animation_index)]

   def update(self):
      self.animation_state()
      self.rect.x -= 6
      self.destroy()
   
   def destroy(self):
      if self.rect.x <= -100:
         self.kill()
      
      
def display_score():
   # subtract start_time for current time to display score
   # slow timer by dividing by 1000 to get to seconds
   current_time = int(pygame.time.get_ticks() / 1000) - start_time 
   score_surf = score_font.render(f'Score: {current_time}', False, (64,64,64))
   score_rect = score_surf.get_rect(center = (400,50))
   screen.blit(score_surf, score_rect)
   return current_time

# create a list of obstacle rectangles. check if the list is empty
# if it isnt empty, iterate through each rectangle and move it 5 pixels to the left. after moving, attach the snail surface to the rectangle and return.
# otherwise return empty list
def obstacle_movement(obstacle_lst):
   if obstacle_lst:
      for obstacle_rect in obstacle_lst:
         obstacle_rect.x -= 5

         if obstacle_rect.bottom == 300:
            screen.blit(snail_surf, obstacle_rect)
         else:
            screen.blit(fly_surf, obstacle_rect)

      #only copy existing item in the list if x is greater than 0
      obstacle_lst = [obstacle for obstacle in obstacle_lst if obstacle.x > -100]

      return obstacle_lst
   else: return []

def collisions(player, obstacles):
   if obstacles:
      for obstacle_rect in obstacles:
         if player.colliderect(obstacle_rect):
            return False
   return True

def collision_sprite():
   if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
      obstacle_group.empty() # remove all obstacles from the group
      return False
   else: return True

def player_animation():
   global player_surf, player_index

   if player_rect.bottom < 300:
      player_surf = player_jump #display jump if player pos is greater than 300
   else:
      player_index += 0.1 # increment player_index to animate the player
      if player_index >= len(player_walk): player_index = 0 # reset player_index to 0 when it reaches the end of the animation list
      player_surf = player_walk[int(player_index)]
   # play walking animation if the player is on the ground
   # display jump surface when player is not on the ground

pygame.init() # initialize pygame
screen = pygame.display.set_mode((800,400)) # set width and height of display
pygame.display.set_caption('Pixel Runner') # set the game title
clock = pygame.time.Clock() # create a clock object to help control framerate
score_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops = -1)

# groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# import images as surface and create score surface
sky_surf = pygame.image.load('graphics/Sky.png').convert() 
ground_surf = pygame.image.load('graphics/ground.png').convert()

# snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# fly
fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_lst = []

player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk1, player_walk2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0 # set gravity of player

# intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2) 
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = score_font.render('Pixel Runner', False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = score_font.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,340))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

# check for input with an event loop (such as exit)
while True:
   for event in pygame.event.get(): 
      if event.type == pygame.QUIT:
         pygame.quit()
         exit()

      if game_active:
         # check for collision with mouse on player character
         if event.type == pygame.MOUSEBUTTONDOWN: #press mouse button to jump
            if player_rect.collidepoint(event.pos):  
               player_gravity = -20
         # press space to jump. dont allow jumping unless the player at the floor
         if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE and player_rect.bottom >= 300: 
               player_gravity = -20
      else:
         if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE:
               game_active = True
               #restart score timer on game restart
               start_time = int(pygame.time.get_ticks() / 1000)

      # set snale position randomly between 900 and 1100 using random number generator
      if game_active:
         if event.type == obstacle_timer:
            obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
            
         # snail timer
         if event.type == snail_animation_timer:
            if snail_frame_index == 0:
               snail_frame_index = 1
            else:
               snail_frame_index = 0
            snail_surf = snail_frames[snail_frame_index]
         # fly timer
         if event.type == fly_animation_timer:
            if fly_frame_index == 0:
               fly_frame_index = 1
            else:
               fly_frame_index = 0
            fly_surf = fly_frames[fly_frame_index]

   if game_active:
      # place surfaces at set positions (left, top)
      screen.blit(sky_surf,(0,0)) 
      screen.blit(ground_surf,(0,300))
      score = display_score()

      player.draw(screen)
      player.update()

      obstacle_group.draw(screen)
      obstacle_group.update()

      # collision
      game_active = collision_sprite()

   else:
      screen.fill((94,129,162))
      screen.blit(player_stand,player_stand_rect)
      obstacle_rect_lst.clear()
      player_rect.midbottom = (80,300)
      player_gravity = 0

      score_message = score_font.render(f'Your score: {score}',False,(111,196,169))
      score_message_rect = score_message.get_rect(center = (400,330))
      screen.blit(game_name,game_name_rect)
      if score == 0:
         screen.blit(game_message,game_message_rect)
      else:
         screen.blit(score_message,score_message_rect)

   pygame.display.update() # draw all of the elements and update everything
   clock.tick(60) # set the framerate to 60 frames per second (60 Hz)
