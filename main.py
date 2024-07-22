import turtle
import winsound
import os
import math
import random

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
PLAYER_SPEED = 15
BULLET_SPEED = 20
ENEMY_SPEED = 2
NUMBER_OF_ENEMIES = 5

# Game class to encapsulate game logic and state
class SpaceInvadersGame:
    def __init__(self):
        self.screen = self.setup_screen()
        self.border_pen = self.draw_border()
        self.score = 0
        self.score_pen = self.create_score_pen()
        self.player = self.create_player()
        self.bullet = self.create_bullet()
        self.enemies = self.create_enemies(NUMBER_OF_ENEMIES)
        self.bullet_state = "ready"
        self.enemy_speed = ENEMY_SPEED
        self.setup_key_bindings()
        self.main_game_loop()

    def setup_screen(self):
        wn = turtle.Screen()
        wn.bgcolor("black")
        wn.title("Space Invaders by Aayansh Singh")
        return wn

    def draw_border(self):
        border_pen = turtle.Turtle()
        border_pen.speed(0)
        border_pen.color("white")
        border_pen.penup()
        border_pen.setposition(-300, -300)
        border_pen.pendown()
        border_pen.pensize(3)
        for side in range(4):
            border_pen.fd(600)
            border_pen.lt(90)
        border_pen.hideturtle()
        return border_pen

    def create_score_pen(self):
        score_pen = turtle.Turtle()
        score_pen.speed(0)
        score_pen.color("white")
        score_pen.penup()
        score_pen.setposition(-290, 280)
        score_pen.write("Score: 0", False, align="left", font=("Arial", 14, "normal"))
        score_pen.hideturtle()
        return score_pen

    def update_score(self):
        score_string = "Score: %s" % self.score
        self.score_pen.clear()
        self.score_pen.write(score_string, False, align="left", font=("Arial", 14, "normal"))

    def create_player(self):
        player = turtle.Turtle()
        player.color("blue")
        player.shape("triangle")
        player.penup()
        player.speed(0)
        player.setposition(0, -250)
        player.setheading(90)
        return player

    def create_bullet(self):
        bullet = turtle.Turtle()
        bullet.color("yellow")
        bullet.shape("triangle")
        bullet.penup()
        bullet.speed(0)
        bullet.setheading(90)
        bullet.shapesize(0.5, 0.5)
        bullet.hideturtle()
        return bullet

    def create_enemies(self, number_of_enemies):
        enemies = []
        for _ in range(number_of_enemies):
            enemy = turtle.Turtle()
            enemy.color("red")
            enemy.shape("circle")
            enemy.penup()
            enemy.speed(0)
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)
            enemies.append(enemy)
        return enemies

    def move_left(self):
        x = self.player.xcor()
        x -= PLAYER_SPEED
        if x < -280:
            x = -280
        self.player.setx(x)

    def move_right(self):
        x = self.player.xcor()
        x += PLAYER_SPEED
        if x > 280:
            x = 280
        self.player.setx(x)

    def fire_bullet(self):
        if self.bullet_state == "ready":
            self.bullet_state = "fire"
            winsound.PlaySound("laser.wav", winsound.SND_ASYNC)
            x = self.player.xcor()
            y = self.player.ycor() + 10
            self.bullet.setposition(x, y)
            self.bullet.showturtle()

    def is_collision(self, t1, t2, distance_threshold):
        distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
        return distance < distance_threshold

    def setup_key_bindings(self):
        turtle.listen()
        turtle.onkey(self.move_left, "Left")
        turtle.onkey(self.move_right, "Right")
        turtle.onkey(self.fire_bullet, "space")

    def reset_bullet(self):
        self.bullet.hideturtle()
        self.bullet_state = "ready"
        self.bullet.setposition(0, -400)

    def reset_enemy(self, enemy):
        x = random.randint(-200, 200)
        y = random.randint(100, 250)
        enemy.setposition(x, y)

    def game_over(self):
        self.player.hideturtle()
        for enemy in self.enemies:
            enemy.hideturtle()
        self.screen.bgcolor("black")
        self.display_game_over_message()
        turtle.done()

    def display_game_over_message(self):
        game_over_pen = turtle.Turtle()
        game_over_pen.speed(0)
        game_over_pen.color("white")
        game_over_pen.penup()
        game_over_pen.setposition(0, 0)
        game_over_pen.write("GAME OVER", align="center", font=("Arial", 24, "normal"))
        game_over_pen.hideturtle()

    def main_game_loop(self):
        while True:
            for enemy in self.enemies:
                x = enemy.xcor()
                x += self.enemy_speed
                enemy.setx(x)

                if enemy.xcor() > 270 or enemy.xcor() < -270:
                    self.enemy_speed *= -1
                    for e in self.enemies:
                        y = e.ycor()
                        y -= 40
                        e.sety(y)

                if self.is_collision(self.bullet, enemy, 25):
                    winsound.PlaySound("explosion-e+b.wav", winsound.SND_ASYNC)
                    self.reset_bullet()
                    self.reset_enemy(enemy)
                    self.score += 10
                    self.update_score()

                if self.is_collision(self.player, enemy, 40):
                    winsound.PlaySound("explosion-e+p.wav", winsound.SND_ASYNC)
                    self.game_over()
                    return

            if self.bullet_state == "fire":
                y = self.bullet.ycor()
                y += BULLET_SPEED
                self.bullet.sety(y)

                if self.bullet.ycor() > 275:
                    self.reset_bullet()

if __name__ == "__main__":
    game = SpaceInvadersGame()
