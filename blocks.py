import turtle


# Draw Title
class Title(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.ht()
        self.penup()
        self.setposition(-350, 275)
        self.write("PIZZA RUNNERS: Done by Yeo Sheen Hern, DIT/FT/2B/11", font=("Arial", 16, "normal"))


class Options(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.ht()
        self.penup()
        self.setposition(-300, -300)
        self.write("Press '1' for free play, '2' for Left-Hand Rule, '3' for Breadth-First Search", font=("Arial", 12, "normal"))


class Counter(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.counter_pen = turtle.Pen()
        self.counter_pen.ht()
        self.counter_pen.penup()
        self.counter_pen.setposition(500, 275)
        self.counter_pen.color('red')
        self.counter_pen.write("Count:", font=('Arial', 14, 'normal'))

        self.count_pen = turtle.Pen()
        self.count_pen.ht()
        self.count_pen.penup()
        self.count_pen.setposition(580, 275)
        self.count_pen.color('red')
        self.count_pen.write("0", font=('Arial', 14, 'normal'))

    def update(self, new_no):
        self.count_pen.clear()
        self.count_pen.write(str(new_no), font=('Arial', 14, 'normal'))


# Class for the Turtle Walls (white squares)
class Maze(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.ht()
        self.penup()
        self.shape("square")
        self.color("black")
        self.penup()
        self.speed(0)


class MapBoundary(Maze):
    def __init__(self):
        Maze.__init__(self)
        self.color("brown")


class Green(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.ht()
        self.shape("square")
        self.color("green")
        self.penup()
        self.speed(0)


class Yellow(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.ht()
        self.penup()
        self.shape("square")
        self.color("yellow")
        self.penup()
        self.speed(0)


