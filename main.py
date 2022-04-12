import pygame
from pygame.locals import *
import sys
import os
import json
import logging

logging.basicConfig(level=logging.DEBUG, filename="errorlog.txt", format="%(asctime)s : %(levelname)s : %(message)s")

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
BLUE = (0, 0, 255)
RED = (200, 30, 30)
GREEN = (0, 255, 0)
BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
SPEED = 4
MAX_SPEED = 15
JUMP_SPEED = 20
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
blocks = pygame.sprite.Group()

def game_loop():
    pygame.init()
    levelX, levelY = 0, 0
    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    FPS = 60
    FramePerSec = pygame.time.Clock()
    pygame.display.set_caption("fun")
    pygame.key.set_repeat(500, 500)
    player = Player()
    levelImport(levelX, levelY)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if pygame.key.get_pressed()[K_ESCAPE]:
                pygame.quit()
                sys.exit()
            if pygame.key.get_pressed()[K_SPACE]:
                player.shoot(bullets)

        DISPLAYSURF.fill(WHITE)
        direction = player.move()
        if direction:
            logging.debug("Direction Reached")
            if direction == "left":
                levelX -= 1
            elif direction == "right":
                levelX += 1
            elif direction == "bottom":
                levelY += 1
            elif direction == "top":
                levelY -= 1
            levelImport(levelX, levelY)
            direction = None
        bullets.update()
        dead = pygame.sprite.groupcollide(enemies, bullets, True, False)
        for i in blocks:
            box = i.get_rect()
            if player.rect.colliderect(box):
                player.wallCollision(box)
        for i in dead.values():
            for k in i:
                k.kill()
        for bullet in bullets:
            DISPLAYSURF.blit(bullet.surf, bullet.rect)
        for i in enemies:
            DISPLAYSURF.blit(i.surf, i.rect)
        for i in blocks:
            DISPLAYSURF.blit(i.surf, i.rect)
        DISPLAYSURF.blit(player.surf, player.rect)
        pygame.display.update()
        FramePerSec.tick(FPS)
    
def levelImport(mapX, mapY):
    blocks.empty()
    enemies.empty()
    levelBlocks = [[]]
    levelEnemies = [[]]
    levelName = (f"level {mapX} {mapY}.json")
    try:
        with open(os.path.join("Levels", levelName), "r") as phrasesDictionary:
            file = (json.loads(phrasesDictionary.read()))
            count = -1
            for i in file["Level"]:
                count += 1
                for j in i:
                    if j == "x":
                        levelBlocks[count].append(1)
                        levelEnemies[count].append(0)
                    elif j == "e":
                        levelEnemies[count].append(1)
                        levelBlocks[count].append(0)
                    else:
                        levelEnemies[count].append(0)
                        levelBlocks[count].append(0)
                if count != 9:
                    levelBlocks.append([])
                    levelEnemies.append([])
        for i in range(len(levelBlocks)):
            for j in range(len(levelBlocks[i])):
                if levelBlocks[i][j] == True:
                    Block(j, i)
                elif levelEnemies[i][j] == True:
                    Enemy(j, i)
    except FileNotFoundError:
        print("You Win")
        pygame.quit()
        sys.exit()


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        # Print statement purely for testing
        print("Player active")
        # Sets up the player sprite
        self.surf = pygame.Surface((30, 50))
        self.surf.fill(RED)
        # Defines the are the sprite is in for collision and motion
        self.rect = self.surf.get_rect()
        # Sets the sprites position
        self.rect.y = 725
        self.rect.x = 25
        # Sets up some variables for the motion later
        # Self.x_motion is defined outside of the game loop so it won't be reset by accident
        self.x_motion = 0
        # Self.y_motion is defined outside of the game loop for the same reason
        self.y_motion = -JUMP_SPEED
        # Self.jumping and self.supported are set to their starting positions
        # Self.jumping should be true whenever gravity should be applying to the player
        self.jumping = False
        # Self.supported should be true whenever ther's no need to check if gravity should be applying to the player.
        # If self.supported is false, and the player isnt already jumping, then it will make them have gravity apply to them.
        self.supported = True
        self.direction = "right"

    def move(self):
        # Recieves all of the key presses
        pressed_keys = pygame.key.get_pressed()
        # This is the current motion system. It is bigger. It should take into account all of the objects that the player is curently colliding with
        # which are being fed into it from the main game loop.
        # If the player wants to jump, pressing the up key will put them into the jump state, which will put them into a pre-set jump
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            # Sets self.jumping to be true
            self.jumping = True
        # If you press the left key, it will add that to your self.x_motion
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            # This subtracts the set speed from self.x_motion, becuase that would move you to the left with pygames coordinates system
            if self.jumping == False:
                self.x_motion -= SPEED
            else:
                self.x_motion -= SPEED/2
            self.direction = "left"
        # This is the same as the left key, but for the right
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            # Again, ditto for the left, but positive becuase it is now moving to the right
            if self.jumping == False:
                self.x_motion += SPEED
            else:
                self.x_motion += SPEED/2
            self.direction = "right"
        if (pressed_keys[K_DOWN] or pressed_keys[K_s]):
            self.jumping = True
            self.supported = True
            self.y_motion = 5
        # This now checks that self.x_motion isn't above the max speed in either direction, and if it is it sets it to the max
        if self.x_motion > MAX_SPEED:
            self.x_motion = MAX_SPEED
        if self.x_motion < -MAX_SPEED:
            self.x_motion = -MAX_SPEED
        # This now adjusts the speed to apply friction, so that the player will slow down if they don't keep on holding the correct key down
        if self.x_motion < 0:
            self.x_motion += -self.x_motion/5
        if self.x_motion > 0:
            self.x_motion -= self.x_motion/5
        # This is used to ensure that when the speed gets low enough, it is just set to 0. Otherwise it will keep on getting closer to zero
        # forever, but never reach it, becuase the amount t slows down is dependant on how fast it is going
        if self.x_motion > -0.5 and self.x_motion < 0.5:
            self.x_motion = 0
        self.rect.move_ip(self.x_motion, 0)
        # If the player is jumping, or falling, then it gets more complex
        if self.jumping == True:
            self.rect.move_ip(0, self.y_motion)
            # Then, the y motion is increased to max speed, from the negative max speed it will always start at. This is to achieve a simple parabolic jump
            if self.y_motion < JUMP_SPEED:
                self.y_motion += 1
        # After the jumping and motion is done, the player could be anywhere, so simple collision detection is ran to check if they've left the screen
        # If they have, it will move them back onto the screen and set their motion to zero
        if self.rect.left <= 0:
            x = self.rect.centerx
            x = SCREEN_WIDTH - x
            self.rect.center = (x, self.rect.centery)
            if self.rect.right >= SCREEN_WIDTH:
                self.rect.move_ip((SCREEN_WIDTH - self.rect.right), 0)
            return("left")
        if self.rect.right >= SCREEN_WIDTH:
            x = self.rect.centerx
            x = SCREEN_WIDTH - x
            self.rect.center = (x, self.rect.centery)
            if self.rect.left <= 0:
                self.rect.move_ip(-self.rect.left, 0)
            return("right")
        if self.rect.bottom >= SCREEN_HEIGHT:
            y = self.rect.centery
            y = SCREEN_HEIGHT - y
            if self.rect.top <= 0:
                self.rect.move_ip(0, -self.rect.top)
            self.rect.center = (self.rect.centerx, y)
            return("bottom")
        if self.rect.top <= 0:
            y = self.rect.centery
            y = SCREEN_HEIGHT - y
            self.rect.center = (self.rect.centerx, y)
            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.move_ip(0, -(self.rect.bottom - SCREEN_HEIGHT))
            return("top")
        # If both self.supported is false and self.jumping is false, then the player should probably be falling, so self.y_motion is set to 0, to prevent gaining height
        # and self.jumping is set to true, so that only the falling is activated. Self.supported is also set to true to ensure the booleans work out.
        if self.supported == False and self.jumping == False:
            self.y_motion = 0
            self.jumping = True
            self.supported = True
        # At the end of this section of code, this is before the collision detection is being run on other objects on the screen, so if self.supported isn't set to false
        # then it's unlikely that it will ever be caught that the block should be falling.
        if self.jumping == False:
            self.supported = False
        return None

    # This function handles collisions with other objects on the screen
    # It takes self (for obvious reasons) and box. Box is whatever box has collided with the player object

    def wallCollision(self, box):
        if self.rect.right > box.left and self.rect.left < box.right:
            if self.rect.bottom > box.top and self.rect.top < box.top:
                self.rect.move_ip(0, box.top - self.rect.bottom)
                self.jumping = False
                self.supported = True
                self.y_motion = -JUMP_SPEED
            if self.rect.top < box.bottom and self.rect.bottom > box.bottom:
                if self.rect.centery > box.bottom:
                    self.rect.move_ip(0, box.bottom - self.rect.top)
                    self.y_motion = -self.y_motion
                    self.jumping = True
        if self.rect.bottom > box.top and self.rect.top < box.bottom:
            if self.rect.left <= box.right and self.rect.right > box.right:
                self.rect.move_ip(box.right - self.rect.left, 0)
                self.x_motion = 0
            if self.rect.right >= box.left and self.rect.left < box.left:
                self.rect.move_ip(box.left - self.rect.right, 0)
                self.x_motion = 0

    def shoot(self, bullets):
        Bullet(self.direction, self.rect.x, self.rect.y + 20)
        return bullets

    def get_location(self):
        return(self.rect.x, self.rect.y)

    def draw(self, surface):
        surface.blit(self.surf, self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, direction, x, y):
        pygame.sprite.Sprite.__init__(self, bullets)
        self.surf = pygame.Surface((15, 10))
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y
        if direction == "left":
            self.x_motion = -MAX_SPEED - 5
        elif direction == "right":
            self.x_motion = MAX_SPEED + 5
        else:
            self.kill()

    def update(self):
        self.rect.move_ip(self.x_motion, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
        if self.rect.right < 0:
            self.kill()

    def draw(self, surface):
        surface.blit(self.surf, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, enemies)
        self.surf = pygame.Surface((50, 50))
        self.rect = self.surf.get_rect()
        self.rect.x = x * 100 - 50
        self.rect.y = y * 100 - 50

    def draw(self, surface):
        surface.blit(self.surf, self.rect)
    

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, blocks)
        self.surf = pygame.Surface((100, 100))
        self.rect = self.surf.get_rect()
        self.rect.x = x * 100
        self.rect.y = y * 100
    
    def draw(self, surface):
        surface.blit(self.surf, self.rect)
    
    def get_rect(self):
        return self.rect



def main():
    pass


if __name__ == "__main__":
    game_loop()
