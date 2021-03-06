from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
import time
import random 

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            #Increases the speed of the ball on every hit
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        print('ball', self.pos)
        # Position of the ball 


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    count = 0
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

            
        # went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
            
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y
            

    def move_rnd(self, dt):
        global game
        self.player1.center_y = self.player1.center_y+random.randint(-50, 50) 
        self.player2.center_y = self.player2.center_y+random.randint(-50, 50)
        game.export_to_png('frames\canva{}.png'.format(self.count))  #export a picture of the full canvas
        self.count+=1
        if self.count == 5: self.count=0
        print('P1', self.player1.center_y)
        print('P2', self.player2.center_y)

class action_model():
    def __init__(self, model):
        self.model = model

    def load_frames(self,):
        #This function needs to np.load the 4 frames 
        #make them grey scale
        #sandwhich the 4 frames into a 3D matrix
        return #return a numpy or tensor of the 4 frames together


    def predict_q(self,):
        #Uses self.model to predict the Q values
        return #argmax(Q)

    def action(self,):
        #will have several if statements
        #ex: if action=="up": move the paddle up 1
        return

    def back_prop(self,):
        #update the loss of self.model
        #mean squared error
        return

class PongApp(App):
    def build(self):
        global game #needed to globally define the whole canvas on the application
        game = PongGame()
        model = 1 #make function build_model()
        agent = action_model(model)
        game.serve_ball()

        #PongGame will run every 0.1 seconds
        Clock.schedule_interval(game.update, 1.0 / 10.0)
        Clock.schedule_interval(game.move_rnd, 1.0 / 10.0)

        
        return game


if __name__ == '__main__':
    PongApp().run()