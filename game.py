# Alexa Gomez, apg2hv and Evan Magnusson, eam7cf
# Game: a player jumps over moving blocks of different heights using the space bar.
# The moving blocks slowly speed up.


# Optional Features: 1) Animation: the player is an animation of Trump 2) Timer, a timer
# will be counting up, the longer the player is in the game, the greater the time and
# the score. 3) Health Meter: The player will have 3 lives and a life will be lost when
# the player touches the right or the left of the obstacle 4) Collectibles, there will be a dark blue block
# randomly appearing, representing a life
# If the player jumps and touches the dark blue block, the player gains lives

# Game inspired by Temple Run


import pygame
import gamebox
import random

camera = gamebox.Camera(800, 600)

sheet1 = gamebox.load_sprite_sheet(
   "https://3.bp.blogspot.com/-_NVjscKbE7Q/WLB4GtYM6PI/AAAAAAAAIyk/iGm67QmaiV0v0VKNSnG5pzenizWGsbvyQCLcB/s1600/trump_run.png",
   4, 6)

sheet1 = [
sheet1[6],
sheet1[7],
sheet1[8],
sheet1[9],
sheet1[10],
sheet1[11],
]

sheet2_pre = gamebox.load_sprite_sheet(
   'http://www.usboundary.com/Downloads/Maps/StateSprites/states_sprites_image_orange_64x64.png', 7, 9
)

sheet2 = []

for i in range(2, 45):
   sheet2.append(sheet2_pre[i])

sheet3_pre = gamebox.load_sprite_sheet(
   'http://www.usboundary.com/Downloads/Maps/StateSprites/states_sprites_image_blue_64x64.png', 7, 9
)

for i in range(2, 45):
   sheet2.append(sheet3_pre[i])


floor = gamebox.from_color(camera.left, 600, "brown", 560000000, 40)

obstacles = [
# gamebox.from_color(70, 585, 'brown', 20, 70),
# gamebox.from_color(200, 585, 'brown', 20, 90),
# gamebox.from_color(350, 585, 'brown', 20, 110),
# gamebox.from_color(camera.right - 250, 585, 'brown', 20, 40),
gamebox.from_color(camera.right - 100, 585, 'brown', 20, 200),
]

collectible = [gamebox.from_image(camera.right - 5, 350, sheet2[random.randrange(0, 86)])]
player = gamebox.from_image(camera.right - 500, 585, sheet1[0])
touched = []

scroller = 0
game_on = False
score = 0
timer_move = 50
minutes_int = 0
seconds_int = 0
frac_float = 0.0
live_move = 50
heart_move = 50
lives_int = 3


def tick(keys):
   global game_on
   global score
   global scroller
   global timer_move
   global live_move
   global heart_move
   global minutes_int
   global seconds_int
   global lives_int
   global frac_float
   global floor
   global obstacles
   global collectible

   title = gamebox.from_text(camera.right-400, 200, "Republican Run", 60, "red", True)
   start = gamebox.from_text(camera.right-400, 300, "PRESS THE SPACE BAR TO BEGIN", 30, "red")
   name = gamebox.from_text(camera.right-400, 450, "Alexa Gomez, apg2hv and Evan Magnusson, eam7cf", 30, "red")
   instructions1 = gamebox.from_text(camera.right-400, 500,
                                     "Jump over the obstacles and try to stay in the game as long as possible!", 25,
                                     "white")
   instructions2 = gamebox.from_text(camera.right-400, 540,
                                     "If you fail to jump over the obstacles and run out of lives, the game is over ):",
                                     25, "white")
   instructions3 = gamebox.from_text(camera.right-400, 520,
                                     "Catch the blue blocks to gain extra lives!", 25,
                                     "white")
   scroller += 1

   camera.clear('black')
   camera.draw(title)
   camera.draw(name)
   camera.draw(instructions1)
   camera.draw(instructions2)
   camera.draw(instructions3)
   camera.draw(start)

   if pygame.K_SPACE in keys:
       game_on = True

   if game_on:
       camera.clear("cyan")
       player.image = sheet1[(scroller // 3) % len(sheet1)]
       camera.draw(player)
       camera.draw(floor)

       x = 1.5

       camera.x += 2*x

       player.speedx = 3.15
       player.speedy += 1
       player.speedx *= 0.95
       player.speedy *= 0.95
       player.move_speed()

       player.move_to_stop_overlapping(floor)

       if scroller % 50 == 0:
           platform = gamebox.from_color(
               random.randrange(camera.right-300, camera.right),
               camera.bottom,
               'brown',
               20, random.randrange(150, 250)
               )
           obstacles.append(platform)
       if scroller % 150 == 0:
           platform2 = gamebox.from_image(
            random.randrange(camera.left, camera.right),
            camera.top + random.randrange(225, 375),
            sheet2[random.randrange(0, 86)]
           )
           collectible.append(platform2)
       for blocks in collectible:
           camera.draw(blocks)

       for obs in obstacles:
           camera.draw(obs)

       for blocks in collectible:
           if scroller % 73 == 0:
               blocks.image = sheet2[random.randrange(0, 86)]
           if player.touches(blocks) and blocks not in touched:
               lives_int += 1
               collectible.remove(blocks)
       for obs in obstacles:
           player.move_to_stop_overlapping(obs)
           if player.right_touches(obs) and obs not in touched:
               lives_int -= 1
               touched.append(obs)
#               how to move the animation back or get rid of the obstacle
       if player.left < camera.left:
           lives_int -= 1
       if lives_int == 0:
           gamebox.pause()
           game_over = gamebox.from_text(camera.right - 400, 100, "Game Over!", 40, "red", True)
           total_time = 60 * minutes_int + seconds_int + frac_float
           time_string = "Total Time: " + str(total_time)
           score_label = gamebox.from_text(camera.right - 400, 200, time_string, 30, "red")
           camera.draw(game_over)
           camera.draw(score_label)

       score += 1
       if pygame.K_SPACE in keys and scroller % 5 == 0:
           if player.bottom_touches(floor):
               player.speedx += 7
               player.speedy += -20
           for obs in obstacles:
               if player.bottom_touches(obs):
                   player.speedx += 7
                   player.speedy += -22
                   # obstacles.remove(obs)
       frac_float = round((score % ticks_per_second) / ticks_per_second, 1)
       frac = str(int(frac_float * 10))
       seconds_int = int((score / ticks_per_second) % 60)
       seconds = str(seconds_int).zfill(2)
       minutes_int = int((score / ticks_per_second) / 60)
       minutes = str(minutes_int)

       timer_move += 3
       timer = gamebox.from_text(timer_move, 50, minutes + ':' + seconds + '.' + frac, 24, 'white')
       live_move += 3
       live_label = gamebox.from_text(live_move, 70, "Lives: "+str(lives_int), 24, 'red')

       camera.draw(timer)
       camera.draw(live_label)

   for blocks in collectible:
       if blocks.right < camera.left:
           collectible.remove(blocks)

   for obs in obstacles:
       if obs.right < camera.left:
           obstacles.remove(obs)

   camera.display()


ticks_per_second = 60

gamebox.timer_loop(ticks_per_second, tick)






