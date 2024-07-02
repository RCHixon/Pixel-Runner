import pygame
from sys import exit

pygame.init() #initialize pygame
screen = pygame.display.set_mode((800,400)) #set width and height of display
pygame.display.set_caption('Runner') #set the game title
clock = pygame.time.Clock() #create a clock object to help control framerate
score_font = pygame.font.Font('font/Pixeltype.ttf', 50)

#import images as surface and create score surface
sky_surf = pygame.image.load('graphics/Sky.png').convert() 
ground_surf = pygame.image.load('graphics/ground.png').convert()

score_surf = score_font.render('Runner', False, (64,64,64))
score_rect = score_surf.get_rect(center = (400,50))

#create snail
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha() 
snail_rect = snail_surf.get_rect(bottomright = (600,300)) #use a rectangle to precisely place the snail

player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
#use a rectangle to precisely place the player character
player_rect = player_surf.get_rect(midbottom = (80,300)) 

#check for input with an event loop (such as exit)
while True:
   for event in pygame.event.get(): 
      if event.type == pygame.QUIT:
         pygame.quit()
         exit()
      #check for collision with mouse on player character
      if event.type == pygame.MOUSEMOTION:
         if player_rect.collidepoint(event.pos): print('collision')

   #place surfaces at set positions (left, top)
   screen.blit(sky_surf,(0,0)) 
   screen.blit(ground_surf,(0,300))
   pygame.draw.rect(screen, '#c0e8ec', score_rect)
   pygame.draw.rect(screen, '#c0e8ec', score_rect,10)
   screen.blit(score_surf,score_rect)

   snail_rect.left -= 4 #move snail rectangle left by 4 pixels each frame
   #reset snail position when it reaches the left side of the screen
   if snail_rect.right <= 0: snail_rect.left = 800
   screen.blit(snail_surf, snail_rect)
   screen.blit(player_surf, player_rect)

   keys = pygame.key.get_pressed()
   if keys[pygame.K_SPACE]:
      print('jump')
   

   #check for collisions with the snail
   # if player_rect.colliderect(snail_rect):
   #    print('collision')

   #check for mouse collisions
   # mouse_pos = pygame.mouse.get_pos()
   # if player_rect.collidepoint((mouse_pos)):
   #   print(pygame.mouse.get_pressed())
   
   pygame.display.update() #draw all of the elements and update everything
   clock.tick(60) #set the framerate to 60 frames per second (60 Hz)
