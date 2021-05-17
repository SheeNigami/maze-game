import turtle                    # import turtle library
import time
from collections import deque
from blocks import *

# Initiate Turtle Screen
wn = turtle.Screen()
wn.bgcolor("white")
# Screen Size
wn.setup(1300, 700)

MAP = 'example.txt'


class Sprite(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("turtle")
        self.color("red")
        self.setheading(270)
        self.penup()
        self.speed(0)

        # Counter
        self.count = 0
        self.counter = Counter()

    # Update the counter
    def update_counter(self):
        self.counter.update(self.count)

    # To move sprite in free play
    def move_up(self):
        self.check_finish()
        self.setheading(90)
        self.move_if_free(90)

    def move_down(self):
        self.check_finish()
        self.setheading(270)
        self.move_if_free(270)

    def move_left(self):
        self.check_finish()
        self.setheading(180)
        self.move_if_free(180)

    def move_right(self):
        self.check_finish()
        self.setheading(0)
        self.move_if_free(0)

    # Only move to cell if not a wall
    def move_if_free(self, heading):
        x_walls = round(self.xcor(), 0)
        y_walls = round(self.ycor(), 0)
        to_check = {
            0: (x_walls+24, y_walls),
            90: (x_walls, y_walls+24),
            180: (x_walls-24, y_walls),
            270: (x_walls, y_walls-24)
        }
        if to_check[heading] not in walls:
            self.forward(24)
            self.count += 1
            self.counter.update(self.count)

    # To find a wall before starting left hand rule
    def find_left_wall(self):
        x_walls = round(self.xcor(), 0)
        y_walls = round(self.ycor(), 0)
        wall_orientation = {
            0: [(x_walls, y_walls+24), (x_walls+24, y_walls)],
            90: [(x_walls-24, y_walls), (x_walls, y_walls+24)],
            180: [(x_walls, y_walls-24), (x_walls-24, y_walls)],
            270: [(x_walls+24, y_walls), (x_walls, y_walls-24)]
        }

        left_front_walls = wall_orientation[int(self.heading())]
        if left_front_walls[0] in walls or left_front_walls[1] in walls:
            self.right(90)
            return True
        self.forward(24)
        return False

    # Orientate and gets the required cells for left hand rule
    def assign_walls(self):
        x_walls = round(self.xcor(), 0)
        y_walls = round(self.ycor(), 0)
        wall_orientation = {
            0: [(x_walls, y_walls+24), (x_walls+24, y_walls)],
            90: [(x_walls-24, y_walls), (x_walls, y_walls+24)],
            180: [(x_walls, y_walls-24), (x_walls-24, y_walls)],
            270: [(x_walls+24, y_walls), (x_walls, y_walls-24)]
        }
        left_front_walls = wall_orientation[int(self.heading())]
        return self.left_hand_rule(left_front_walls[0], left_front_walls[1])

    # Left Hand Rule
    def left_hand_rule(self, left_cell, front_cell):
        if left_cell in walls:
            if front_cell not in walls:
                self.forward(24)
                return True
            else:
                self.right(90)
                return False
        else:
            self.left(90)
            self.forward(24)
            return True

    def check_finish(self):
        # check turtle coordinates are at the finish line
        if (round(self.xcor(), 0), round(self.ycor(), 0)) == (end_x, end_y):
            time.sleep(2)
            reset()
            # Listen for other algorithms
            wn.onkey(start_freeplay, '1')
            wn.onkey(start_lhr, '2')
            wn.onkey(start_bfs, '3')
            wn.listen()
            return True


class BFS:
    def __init__(self):
        self.green = Green()
        self.frontier = deque()
        self.visited = set()
        self.solution = {}

        self.frontier.append((start_x, start_y))
        self.solution[start_x, start_y] = start_x, start_y

    def search(self):
        while len(self.frontier) > 0:
            # time.sleep(0.01)
            x_current, y_current = self.frontier.popleft()
            current = x_current, y_current

            # check all 4 directions
            self.check_cell((x_current - 24, y_current), current)
            self.check_cell((x_current, y_current - 24), current)
            self.check_cell((x_current + 24, y_current), current)
            self.check_cell((x_current, y_current + 24), current)

            # Visualise BFS
            if current == (end_x, end_y):
                self.green.goto(x_current, y_current)
                self.green.stamp()
                time.sleep(0.05)
                yellow = Yellow()
                yellow.goto(end_x, end_y)
                yellow.stamp()
            else:
                if current != (start_x, start_y):
                    self.green.goto(x_current, y_current)
                    self.green.stamp()

    # Check if cell is path and not visited, add to frontier/visited
    def check_cell(self, cell, current):
        if cell in path and cell not in self.visited:
            self.solution[cell] = current
            self.frontier.append(cell)
            self.visited.add(cell)

    # Retrieve the shortest path back
    def backtrace(self):
        x, y = end_x, end_y
        yellow = Yellow()
        yellow.goto(x, y)
        yellow.stamp()

        answer = []
        while (x, y) != (start_x, start_y):
            answer.insert(0, (x, y))
            yellow.goto(self.solution[x, y])
            yellow.stamp()
            x, y = self.solution[x, y]
            time.sleep(0.05)

        return answer


# Setup/Draw the Maze
def setup_maze(file_name):
    maze = Maze()
    # Read Map File
    f = open(file_name, "r")
    grid = f.readlines()

    # Starting x/y coordinates for map
    screen_startx = -((len(grid[0]) / 2) * 24)
    screen_starty = ((len(grid) / 2 + 1) * 24)

    # Create Map Boundaries
    for y in range(len(grid)+2):
        for x in range(len(grid[0])+1):
            if (y == 0 or y == len(grid)+1) or (x == 0 or x == len(grid[0])):
                screen_x = screen_startx + (x * 24)
                screen_y = screen_starty - (y * 24)
                boundary = MapBoundary()
                boundary.goto(screen_x, screen_y)
                boundary.stamp()
                walls.append((screen_x, screen_y))

    # Global start and end
    global start_x, start_y, end_x, end_y

    # Each line
    for y in range(len(grid)):
        # Each Character
        for x in range(len(grid[y])):
            # Set starting coordinate of each character to be drawn
            character = grid[y][x]
            screen_x = screen_startx + 24 + (x * 24)
            screen_y = screen_starty - 24 - (y * 24)

            # Draw Each Cell based on map text file
            if character == "X":
                maze.goto(screen_x, screen_y)
                maze.stamp()
                walls.append((screen_x, screen_y))

            if character == '.' or character == 'e':
                path.append((screen_x, screen_y))

            if character == "e":
                yellow = Yellow()
                yellow.goto(screen_x, screen_y)
                yellow.stamp()
                end_x, end_y = screen_x, screen_y

            if character == "s":
                start_x, start_y = screen_x, screen_y


# Resets screen
def reset():
    wn.clearscreen()
    Title()
    Options()
    walls.clear()
    path.clear()


def start_freeplay():
    reset()

    # Set sprite starting and path tracking
    sprite = Sprite()
    setup_maze('./maps/' + MAP)
    sprite.goto(start_x, start_y)
    sprite.pendown()

    # Free play, listen for moves
    wn.onkey(sprite.move_up, 'Up')
    wn.onkey(sprite.move_left, 'Left')
    wn.onkey(sprite.move_right, 'Right')
    wn.onkey(sprite.move_down, 'Down')

    # Listen for other algorithms
    wn.onkey(start_freeplay, '1')
    wn.onkey(start_lhr, '2')
    wn.onkey(start_bfs, '3')

    wn.listen()


def start_lhr():
    reset()

    # Set sprite starting and path tracking
    sprite = Sprite()
    setup_maze('./maps/' + MAP)
    sprite.goto(start_x, start_y)
    sprite.pendown()

    # Listen for other algorithms
    wn.onkey(start_freeplay, '1')
    wn.onkey(start_lhr, '2')
    wn.onkey(start_bfs, '3')
    wn.listen()

    while True:
        # if not is_paused:
        if sprite.find_left_wall() or sprite.count >= 1000:
            break
        sprite.count += 1
        sprite.update_counter()

    while True:
        # if not is_paused:
        if sprite.check_finish() or sprite.count >= 1000:
            break
        else:
            should_add = sprite.assign_walls()

        if should_add:
            sprite.count += 1
            sprite.update_counter()

        time.sleep(0.01)


def start_bfs():
    reset()

    sprite = Sprite()
    setup_maze('./maps/' + MAP)

    # Set sprite starting and path tracking
    sprite.shape = 'square'
    sprite.goto(start_x, start_y)
    sprite.pendown()

    # Listen for other algorithms
    wn.onkey(start_freeplay, '1')
    wn.onkey(start_lhr, '2')
    wn.onkey(start_bfs, '3')
    wn.listen()

    # Run BFS
    bfs = BFS()
    bfs.search()
    answer = bfs.backtrace()

    # Move Sprite with shortest path
    for cell in answer:
        sprite.goto(cell[0], cell[1])
        sprite.count += 1
        sprite.counter.count_pen.clear()
        sprite.update_counter()
        time.sleep(0.05)


# ############ main program starts here  ######################
Title()
Options()
walls = []
path = []
is_paused = False

# Launch algorithms
wn.onkey(start_freeplay, '1')
wn.onkey(start_lhr, '2')
wn.onkey(start_bfs, '3')
wn.onkey(reset, 'Escape')

wn.listen()
wn.mainloop()
