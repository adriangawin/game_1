import pygame
import sys, os
from pygame.math import Vector2


class User(object):
    # User object
    def __init__(self, floors):
        self.position = Vector2(600, 200)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.floors = floors
        self.color = (50, 100, 255)
        self.width = 20
        self.height = 20
        # self.touch_ceiling = False
        # self.touch_floor = False
        self.is_jump = False
        self.is_move = False
        self.max_speed = 10

    def calculate(self):
        self.gravity()
        self.move()
        self.jump()
        self.calculate_position()

        self.is_move = False

    def calculate_position(self):
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration *= 0

    def check_floor(self):
        if self.position.y+self.height >= self.floor.get_up() \
                and self.position.x + self.width > self.floor.get_left() \
                and self.position.x < self.floor.get_right():
            return True
        else:
            return False

    def touch_floor(self):
        if self.position.y + self.height == self.floor.get_up():
            return True
        else:
            return False

    def gravity(self):
        position_bottom = self.position.y + self.height
        for floor in self.floors:
            if position_bottom == floor.get_up():
                self.acceleration.y = -self.velocity.y
            else:
                difference = floor.get_up() - position_bottom
                if difference > self.velocity.y + 3:
                    self.acceleration += Vector2(0, 2)
                elif difference < self.velocity.y:
                    self.velocity.y = difference
                else:
                    print("error in gravity")

    # def gravity(self):
    #     position_bottom = self.position.y + self.height
    #
    #     floo = self.floor.get_up()
    #
    #     if position_bottom == floo:
    #         self.acceleration.y = -self.velocity.y
    #     else:
    #         difference = floo - position_bottom
    #         if difference > self.velocity.y + 1:
    #             self.acceleration += Vector2(0, 2)
    #         elif difference < self.velocity.y:
    #             self.velocity.y = difference
    #         else:
    #             print("error in gravity")

    def move_jump(self):
        if self.touch_floor():
            self.is_jump = True

    def jump(self):
        if self.is_jump:
            self.velocity += Vector2(0, -30)
            self.is_jump = False

    # -- moves --

    def move(self):
        if not self.is_move:
            self.move_stop()

    # def move_right(self):
    #     if self.touch_floor():
    #         self.is_move = True
    #         if not self.velocity.x > self.max_speed:
    #             self.acceleration += Vector2(1, 0)

    def move_right(self):
        self.is_move = True
        if not self.velocity.x > self.max_speed:
            self.acceleration += Vector2(1, 0)

    def move_left(self):
        self.is_move = True
        if not self.velocity.x < -self.max_speed:
            self.acceleration += Vector2(-1, 0)

    def move_stop(self):
        if self.velocity.x > 0:
            self.acceleration += Vector2(-1, 0)
        elif self.velocity.x < 0:
            self.acceleration += Vector2(1, 0)


class Floor(object):
    def __init__(self, left, right, up, down, color=(153, 102, 51)):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.width = self.right - self.left
        self.height = self.down - self.up
        self.color = color

    def get_up(self):
        return self.up

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height


class MyGame(object):
    # my own game with different timer tick
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

        self.screen_size = self.screen.get_size()

        self.floor1 = Floor(0, 620, 700, 720)
        self.floor2 = Floor(200, 600, 400, 420)
        self.floor3 = Floor(700, 1270, 700, 720)
        self.floors = (self.floor1, self.floor2, self.floor3)
        self.user = User(self.floors)

        while True:
            self.clock.tick(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit(0)
                if event.type == pygame.JOYBUTTONDOWN:
                    pass

            self.tick()
            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()

    def tick(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.user.move_jump()
        if pressed[pygame.K_RIGHT]:
            self.user.move_right()
        if pressed[pygame.K_LEFT]:
            self.user.move_left()
        if pressed[pygame.K_SPACE]:
            self.user.move_jump()

    def draw(self):
        self.draw_user()
        self.draw_floor()

    def draw_user(self):
        self.user.calculate()

        usr = pygame.Rect(self.user.position[0], self.user.position[1], self.user.width, self.user.height)
        pygame.draw.rect(self.screen, self.user.color, usr)

    def draw_floor(self):
        for floor in self.floors:
            rect = pygame.Rect(floor.get_left(), floor.get_up(), floor.get_width(), floor.get_height())
            pygame.draw.rect(self.screen, floor.color, rect)


if __name__ == "__main__":
    MyGame()