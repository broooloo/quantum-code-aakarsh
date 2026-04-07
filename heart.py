import turtle

screen = turtle.Screen()
screen.bgcolor("black")  
screen.title("Aakarsh's Heart ❤️")  

t = turtle.Turtle()
t.speed(3)
t.pensize(4)
t.color("red", "pink")  

t.penup()
t.goto(0, -120)
t.pendown()

t.begin_fill()

t.left(140)
t.forward(180)

t.circle(-90, 200)
t.left(120)

t.circle(-90, 200)

t.forward(180)

t.end_fill()

t.penup()
t.goto(0, 50)
t.color("white")
t.write("Made by Aakarsh", align="center", font=("Arial", 16, "bold"))

t.hideturtle()

turtle.done()
