import pygame
import time
import random
from pygame.locals import*              # https://www.pygame.org/docs/ref/locals.html

class Game:
    def __init__(self):
        pygame.init()       #to initialize all imported pygame modules
        pygame.mixer.init()     #this initializes mixer library of pygame used to play sounds
        self.play_background_music()
        self.surface = pygame.display.set_mode((1000, 600))  # creates a display surface as the regular screen
        self.syringe = syringe(self.surface)
        self.syringe.draw()
        self.virus = Virus(self.surface)
        self.virus.draw()

    def bring_game_background(self):
        bgimg = pygame.image.load("Resources/Background.jpg")
        self.surface.blit(bgimg,(0,0))

    def display_score(self):
        font = pygame.font.SysFont('arial',25)
        score = font.render(f"Score: {self.syringe.length*10}",True,(255,255,255))
        self.surface.blit(score,(850,10))


    def play_background_music(self):
        pygame.mixer.music.load("Resources/game audio.mp3")
        pygame.mixer.music.play(-1,0)           #plays the music '-1' denotes music is played all time while playing and '0' denotes music is played from start of the game

    def play_sound(self,sound):
        if sound == "ding":
            sound = pygame.mixer.Sound("Resources/ding sound.mp3")  # loads the audio to variable named 'sound'
        elif sound == "game over":
            sound = pygame.mixer.Sound("Resources/game over sound.mp3")  # loads the audio to variable named 'sound'
        pygame.mixer.Sound.play(sound)  # plays the audio the is saved in variable 'sound'

    def play(self):
        self.bring_game_background()        #draws background of the game
        self.syringe.walk()
        self.virus.draw()
        self.display_score()
        pygame.display.flip()           #we need to call this function whenever we want to display something

        #snake colloiding with virus
        if self.is_collision(self.syringe.block_x[0],self.syringe.block_y[0],self.virus.x,self.virus.y): #check if collision is happened with head
            self.play_sound("ding")
            self.syringe.increase_len()                    #when snake have collision with its food then its length is incremented
            self.virus.move()

        #snake colloiding with itself
        for i in range(2,self.syringe.length):
            if self.is_collision(self.syringe.block_x[0], self.syringe.block_y[0], self.syringe.block_x[i], self.syringe.block_y[i]):
                self.play_sound("game over")
                raise "game over"           #an exception is raised and it will come out of the loop

        #snake colloiding with boundary wall
        if not (1000 >= self.syringe.block_x[0] >= 0  and 600 >= self.syringe.block_y[0] >= 0):
            self.play_sound("game over")
            raise "Hitted the boundry"


    def is_collision(self,x1,y1,x2,y2):             #this function help us determine if collision of snake and food had happended
        if x2 <= x1  and x1  < x2 + size:
            if y2 <= y1 and y1  < y2 + size:
                return True
        return False

    def show_game_is_over(self):
        self.surface.fill((230,0,0))
        pygame.mixer.music.pause()          #pause the music when game over window is shown
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game Over! your score is: {self.syringe.length * 10}", True, (8, 0, 0))
        self.surface.blit(line1, (250, 200))
        line2 = font.render(f"To play again press Enter, to exit press Esc", True, (255, 255, 0))
        self.surface.blit(line2, (250, 250))
        pygame.display.flip()


    def reset(self):
        self.syringe = syringe(self.surface)
        self.virus = Virus(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():  # if an input is detected from mouse keyboard then it brings input command here
                if event.type == KEYDOWN:  # https://www.pygame.org/docs/ref/event.html#module-pygame.event

                    if event.key == K_ESCAPE:  # if i press escape key it should exit the window
                        running = False

                    if event.key == K_RETURN:       #RETURN is ENTER key here, we use this when our game is over and we need to restart the game
                        pygame.mixer.music.unpause()
                        pause = False               #to restart the game the 'pause' key is made false

                    if not pause:                   #this if block will run only if pause if 'False'
                        if event.key == K_UP:
                            self.syringe.move_up()

                        if event.key == K_DOWN:
                            self.syringe.move_down()

                        if event.key == K_LEFT:
                            self.syringe.move_left()

                        if event.key == K_RIGHT:
                            self.syringe.move_right()

                elif event.type == QUIT:
                    running = False  # help us exit the prog when we click cross

            try:
                if not pause:               #we have to play the game only when pause is 'False'
                    self.play()
            except Exception as e:
                self.show_game_is_over()
                pause = True
                self.reset()

            time.sleep(0.1)

class Virus:
    def __init__(self,parent_screen):
        self.x = size*3
        self.y = size*3
        self.image = pygame.image.load("Resources/virus image.jpg").convert()
        self.parent_screen = parent_screen

    def draw(self):
        self.parent_screen.blit(self.image,(self.x,self.y))     #using blit to draw the image at x,y position
        pygame.display.flip()                                   #using flip() is essential here to see the image

    def move(self):
        self.x = random.randint(1,24)*size                      #to reach random 'i'th block we need to multiply i with size of each block
        self.y = random.randint(1, 14)*size





class syringe:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("Resources/bock.jpg").convert()  # loads the image
        self.length = 1
        self.block_x = [size]*self.length
        self.block_y = [size]*self.length
        self.direction = 'right'           #let initially our block was moving right at start of the gam

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.block_x[i], self.block_y[i]))  # blit func draws the bloc        tupple(100,100) defines where to draw
        pygame.display.flip()                               #It allows only a portion of the screen to updated, instead of the entire area
        #we need to call this flip() func when required again and again

    def increase_len(self):
        self.length += 1
        self.block_x.append(-1)
        self.block_y.append(-1)


    def move_up(self):
        if not self.direction == 'down':
            self.direction = 'up'       #using up/down/l/r key we are just changing snake's direction,  while it will move itself

    def move_down(self):
        if not self.direction == 'up':
            self.direction = 'down'

    def move_left(self):
        if not self.direction == 'right':
            self.direction = 'left'


    def move_right(self):
        if not self.direction =='left':
            self.direction = 'right'


    def walk(self):
        for i in range(self.length-1,0,-1):
            self.block_x[i] = self.block_x[i-1]
            self.block_y[i] = self.block_y[i-1]

        if self.direction == 'up':
            self.block_y[0] -= size  # our block will shift to 10 pixels up  #we chose 40 here bcoz our block is of size 40X40 pixels in jpg file

        elif self.direction == 'down':
            self.block_y[0] += size  # same for down key, 10 pix down

        elif self.direction == 'left':
            self.block_x[0] -= size

        elif self.direction == 'right':
            self.block_x[0] += size

        self.draw()  # draw updated block everytime it changes position

if __name__ == '__main__':
    size = 40  #size of our block is 40X40 pixels in jpg format
    game = Game()
    game.run()












