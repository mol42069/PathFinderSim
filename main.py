# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------- imports ------------------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


import pygame
import sys
import threading


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------ global variables -------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


grey = (30, 30, 30)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (100, 100, 100)
start = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
pygame.init()
x = 1920
y = 1080
screen_size = (x, y)
display = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
display.fill(grey)
visit = []
road = []
road_f = []
visited_tf = []
is_finished = False

# ----------------------------------------------------- images ------------------------------------------------------- #


exit_normal_img = pygame.image.load('images/EXIT_normal.png').convert_alpha()
exit_clicked_img = pygame.image.load('images/EXIT_clicked.png').convert_alpha()
exit_hover_img = pygame.image.load('images/EXIT_hover.png').convert_alpha()
click_img = pygame.image.load('images/click.png').convert_alpha()
dfs_img = pygame.image.load('images/DFS.png').convert_alpha()
dfs_clicked_img = pygame.image.load('images/DFS_clicked.png').convert_alpha()
dfs_hover_img = pygame.image.load('images/DFS_hover.png').convert_alpha()
bfs_normal_img = pygame.image.load('images/BFS_normal.png').convert_alpha()
bfs_clicked_img = pygame.image.load('images/BFS_clicked.png').convert_alpha()
bfs_hover_img = pygame.image.load('images/BFS_hover.png').convert_alpha()
astar_hover_img = pygame.image.load('images/Astar_hover.png').convert_alpha()
astar_clicked_img = pygame.image.load('images/Astar_clicked.png').convert_alpha()
astar_normal_img = pygame.image.load('images/Astar_normal.png').convert_alpha()
start_img = pygame.image.load('images/starting.png').convert_alpha()
clear_img = pygame.image.load('images/clear.png').convert_alpha()
clear_clicked_img = pygame.image.load('images/clear_clicked.png').convert_alpha()
clear_hover_img = pygame.image.load('images/clear_hover.png').convert_alpha()
greed_img = pygame.image.load('images/greed.png').convert_alpha()
greed_hover_img = pygame.image.load('images/greed_hover.png').convert_alpha()
greed_clicked_img = pygame.image.load('images/greed_clicked.png').convert_alpha()
wall_img = pygame.image.load('images/wall.png').convert_alpha()
wall_hover_img = pygame.image.load('images/wall_hover.png').convert_alpha()
wall_clicked_img = pygame.image.load('images/wall_clicked.png').convert_alpha()
start_b_img = pygame.image.load('images/start.png').convert_alpha()
start_b_hover_img = pygame.image.load('images/start_hover.png').convert_alpha()
start_b_clicked_img = pygame.image.load('images/start_clicked.png').convert_alpha()
finish_img = pygame.image.load('images/finish.png').convert_alpha()
finish_hover_img = pygame.image.load('images/finish_hover.png').convert_alpha()
finish_clicked_img = pygame.image.load('images/finish_clicked.png').convert_alpha()


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------- Background rectangles ----------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


class Rectangle:

    def __init__(self, starting_img):               # this function initializes a rectangle with all needed variables
        self.starting_img = starting_img
        self.value = 0
        self.rect = starting_img.get_rect()
        self.t1_i = 0
        self.t2_i = 0
        self.is_transforming = False
        self.start = False
        self.finish = False
        self.wall = False
        self.wall_building = False
        self.wall_disassembly = False
        self.wall_built = False
        self.w_b = 0
        self.left_click = False
        self.right_click = False

# ------------------------------------------------- draw function ---------------------------------------------------- #

    def draw(self, bx, by):                         # here we draw the starting rectangle --> grey
        self.rect.topleft = (bx, by)
        display.blit(self.starting_img, (self.rect.x, self.rect.y))

# -------------------------------------- draw if mouse on rectangle function ----------------------------------------- #

    def mouse_rectangle(self, pos, choice="WALL"):  # this function checks if a button is pressed as well as in which
        match choice:                               # mode we are currently in. If pressed we change the color of the
            case "WALL":                            # rectangle in the way the current mode tells us
                if self.rect.collidepoint(pos):
                    if pygame.mouse.get_pressed()[0] == 1 and not self.left_click:
                        self.left_click = True
                        self.wall = True
                        self.wall_building = True

                    elif pygame.mouse.get_pressed()[0] != 1:
                        self.left_click = False

                    if pygame.mouse.get_pressed()[2] == 1 and not self.right_click:
                        self.right_click = True
                        self.wall = False
                        self.wall_disassembly = True

                    elif pygame.mouse.get_pressed()[2] != 1:
                        self.right_click = False

                if self.wall_building and not self.wall_built:
                    if self.w_b < 10:
                        w_h = self.w_b * 3

                        self.rect = pygame.draw.rect(display, black, pygame.Rect(self.rect.x, self.rect.y, w_h, w_h))
                        pygame.display.flip()
                        self.w_b += 1

                    else:
                        self.w_b = 0
                        self.wall_building = False
                        self.wall_built = True

                elif self.wall_disassembly and self.wall_built:
                    if self.w_b < 10:
                        w_h = self.w_b * 3
                        self.rect = pygame.draw.rect(display, white, pygame.Rect(self.rect.x, self.rect.y, w_h, w_h))
                        pygame.display.flip()
                        self.w_b += 1

                    else:
                        self.w_b = 0
                        self.wall_disassembly = False
                        self.wall_built = False

            case "START":

                if self.rect.collidepoint(pos):
                    if pygame.mouse.get_pressed()[0] == 1 and not self.left_click:
                        self.left_click = True
                        self.start = True
                        rec = pygame.Rect(self.rect.x, self.rect.y, 9 * 3, 9 * 3)
                        self.rect = pygame.draw.rect(display, start, rec)
                        pygame.display.flip()
                        return True

                    elif pygame.mouse.get_pressed()[0] != 1:
                        self.left_click = False

                    return None

            case "START_DEL":

                if pygame.mouse.get_pressed()[0] == 1 and not self.left_click:
                    self.left_click = True
                    self.start = False
                    self.rect = pygame.draw.rect(display, white, pygame.Rect(self.rect.x, self.rect.y, 30, 30))
                    pygame.display.flip()
                    return False

                elif pygame.mouse.get_pressed()[0] != 1:
                    self.left_click = False

                return None

            case "FINISH":
                if self.rect.collidepoint(pos):
                    if pygame.mouse.get_pressed()[0] == 1 and not self.left_click:
                        self.left_click = True
                        self.finish = True
                        rec = pygame.Rect(self.rect.x, self.rect.y, 9*3, 9 * 3)
                        self.rect = pygame.draw.rect(display, red, rec)
                        pygame.display.flip()
                        return True

                    elif pygame.mouse.get_pressed()[0] != 1:
                        self.left_click = False

                    return None

            case "CLEAR":
                self.t1_i = 0
                self.t2_i = 0
                self.is_transforming = False
                self.start = False
                self.finish = False
                self.wall = False
                self.wall_building = False
                self.wall_disassembly = False
                self.wall_built = False
                self.w_b = 0
                self.left_click = False
                self.right_click = False
                display.blit(self.starting_img, (self.rect.x, self.rect.y))

# -------------------------------------- draw if mouse on rectangle function ----------------------------------------- #

    def transform_is_checking(self):                # here we transform the rectangle into a green one with a little
        while self.t1_i < 10:                       # animation where self.t1_i will increase which makes the rectangle
            w_h = self.t1_i * 3                     # get bigger
            pygame.draw.rect(display, green, pygame.Rect(self.rect.x, self.rect.y, w_h, w_h))
            pygame.display.flip()
            self.t1_i += 1

        self.t1_i = 0                               # reset the self.t1_i to 0, so we could if we want transform again

# -------------------------------------- draw if mouse on rectangle function ----------------------------------------- #

    def transform_is_checked(self):                 # here we transform the rectangle into a blue one with a little
        while self.t2_i < 10:                       # animation where self.t2_i will increase which makes the rectangle
            w_h = self.t2_i * 3                     # get bigger
            pygame.draw.rect(display, blue, pygame.Rect(self.rect.x, self.rect.y, w_h, w_h))
            pygame.display.flip()
            self.t2_i += 1

        self.t2_i = 0                               # reset the self.t2_i to 0, so we could if we want transform again

# --------------------------------------- returns if the rectangle is a wall ----------------------------------------- #

    def is_wall(self):
        return self.wall

# ------------------------------------- returns if the rectangle is the finish --------------------------------------- #

    def is_finish(self):
        return self.finish

# ------------------------------------- returns if the rectangle is the finish --------------------------------------- #

    def set_value(self, value):
        self.value = value

# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------- Choice ------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


class Choice:                                        # here we have the buttons on top

    def __init__(self, normal_img, clicked_img, hover_img, choice):
        self.choice1_img = normal_img                # here we get the images for the buttons as well as which button
        self.choice2_img = clicked_img               # the current instance is e.g. "WALL", "START", "DFS, ...
        self.hover_img = hover_img

        self.rect = self.choice1_img.get_rect()

        self.clicked = True
        self.choice = str(choice)

# ------------------------------------------------- draw function ---------------------------------------------------- #

    def draw(self, bx, by, pos):                        # here we draw these buttons on the given positions
        self.rect.topleft = (bx, by)                    # and change the button-images if clicked or hovered
        if self.rect.collidepoint(pos):                 # also it returns what this button is when clicked otherwise
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:  # it will return "NULL"
                self.clicked = True
                display.blit(self.choice2_img, (self.rect.x, self.rect.y))
                return self.choice

            elif pygame.mouse.get_pressed()[0] != 1:
                self.clicked = False
                display.blit(self.hover_img, (self.rect.x, self.rect.y))

        else:
            display.blit(self.choice1_img, (self.rect.x, self.rect.y))

        return "NULL"


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------- DFS -------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

class DFS:

    def __init__(self):
        self.reached_finish = False
        self.finish = (-1, -1)
        self.stop = False

# --------------------------------------------------- find finish ---------------------------------------------------- #

    def find_finish(self, rectangles, graph, current):          # here we write the oder of the rectangles into visit
        if rectangles[current[0]][current[1]].is_finish():      # for DFS and check if the rectangle is a wall
            self.reached_finish = True
            self.finish = current
            for o in visit:
                visited_tf.append(o)

        if current not in visit:
            visit.append(current)
            key = (current[0], current[1])
            for neighbor in graph[key]:
                if not rectangles[neighbor[0]][neighbor[1]].is_wall():
                    self.find_finish(rectangles, graph, neighbor)

# ---------------------------------------------------- find path ----------------------------------------------------- #

    def find_path_optimal(self, graph, starting_rectangle):
        if self.finish != (-1, -1):                             # we check that we have a finish
            path = []
            temp_path = []
            index = len(visited_tf)                             # we set the starting index to the last possible index
            current = self.finish                               # we set the current to the finish position
            while index >= 0:
                curr_best = (index, current)                    # we create the curr best to remember the best so far
                for neighbor in graph[current]:                 # we go through all neighbors for the current rectangle
                    if neighbor in visited_tf:
                        if curr_best[0] > visited_tf.index(neighbor):   # check if the index of the neighbor is smaller
                            temp_index = visited_tf.index(neighbor)
                            if index < temp_index:
                                temp_path.append(neighbor)
                            else:
                                temp_path.insert(0, neighbor)

                            index = visited_tf.index(neighbor)
                            curr_best = (index, neighbor)

                    current = curr_best[1]
                if len(temp_path) != 0:
                    path.append(temp_path[0])

                else:
                    r_path = []
                    for rec in path:
                        if starting_rectangle != rec:
                            r_path.insert(0, rec)

                    return r_path

                temp_path.clear()

        return None


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------- DFS -------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


class BFS:

    def __init__(self, graph):
        self.graph = graph
        self.visited = []
        self.queue = []
        self.finish = (-1, -1)
        self.finished = False

# --------------------------------------------------- find finish ---------------------------------------------------- #

    def find_finish(self, starting_rec, rectangles):
        self.visited.append(starting_rec)
        self.queue.append(starting_rec)

        while self.queue and not self.finished:               # Creating loop to visit each node
            m = self.queue.pop(0)
            for neighbour in self.graph[m]:
                if neighbour not in self.visited and not rectangles[neighbour[0]][neighbour[1]].is_wall():
                    if rectangles[neighbour[0]][neighbour[1]].is_finish():
                        self.finish = neighbour
                        self.finished = True
                        return self.visited
                    self.visited.append(neighbour)
                    self.queue.append(neighbour)
        return self.visited

# ---------------------------------------------------- find path ----------------------------------------------------- #

    def find_path_optimal(self, starting_rectangle):
        if self.finish != (-1, -1):                             # we check that we have a finish
            path = []
            temp_path = []
            index = len(self.visited) - 1                       # we set the starting index to the last possible index
            current = self.finish                               # we set the current to the finish position
            while index >= 0:
                curr_best = (index, current)                    # we create the curr best to remember the best so far
                for neighbor in self.graph[current]:            # we go through neighbors for the current rectangle
                    if neighbor in self.visited:
                        if curr_best[0] > self.visited.index(neighbor):  # check if the index of the neighbor is smaller
                            temp_index = self.visited.index(neighbor)
                            if index < temp_index:
                                temp_path.append(neighbor)
                            else:
                                temp_path.insert(0, neighbor)

                            index = self.visited.index(neighbor)
                            curr_best = (index, neighbor)

                    current = curr_best[1]
                if len(temp_path) != 0:
                    path.append(temp_path[0])

                else:
                    r_path = []
                    for rec in path:
                        if starting_rectangle != rec:
                            r_path.insert(0, rec)
                    return r_path

                temp_path.clear()

        return None


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------- A-star ------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


class Astar:

    def __init__(self, rectangles, start_rec):
        self.is_finish = False
        self.is_start = False
        self.start = start_rec
        self.rec = rectangles
        self.graph = generate_neighbors_astar()
        self.visited = []
        self.filtered_v = []
        self.counter = 0

# --------------------------------------------------- find finish ---------------------------------------------------- #

    def find_finish(self, cur_xy):
        while not self.is_finish and self.counter < 3000:
            self.counter += 1
            n_value = 10000                                        # set the next value to 10000 to find the next lowest
            temp_next = (-1, -1)
            for neighbor in self.graph[cur_xy]:
                if neighbor not in self.visited:
                    if self.rec[neighbor[0]][neighbor[1]].is_finish():  # check if it is finished
                        self.is_finish = True
                        return

                    if self.rec[neighbor[0]][neighbor[1]].start:  # check if it is finished
                        continue

                    elif self.rec[neighbor[0]][neighbor[1]].is_wall():  # check if wall
                        self.graph[cur_xy].remove(neighbor)        # removing the next out of the graph for this node
                        self.visited.append(neighbor)
                        continue

                    elif self.rec[neighbor[0]][neighbor[1]].value < n_value:    # we check if value is lower
                        n_value = self.rec[neighbor[0]][neighbor[1]].value
                        temp_next = (neighbor[0], neighbor[1])

            if temp_next != (-1, -1):
                self.visited.append(temp_next)
                self.filtered_v.append(temp_next)
                self.graph[cur_xy].remove(temp_next)                # removing the next out of the graph for this node
                cur_xy = temp_next                                  # so it cant be repeated.
                temp_next = (-1, -1)                                # reset temp_next, so it can get into here again
                n_value = 10000                                     # reset value to high for this to not stop.
                self.find_finish(cur_xy)
        return
# --------------------------------------------------- find finish ---------------------------------------------------- #

    def give_values(self, finish):
        for i, yy in enumerate(self.rec):
            for o, xx in enumerate(yy):
                if xx.wall:                                     # setting the wall to a high number, so it will not be
                    temp_value = [9000, 0]                      # considered
                else:
                    temp_value = [finish[0] - o, finish[1] - i]
                    if temp_value[0] < 0:
                        temp_value[0] = temp_value[0] * -1

                    if temp_value[1] < 0:
                        temp_value[1] = temp_value[1] * -1

                self.rec[i][o].set_value(temp_value[0] + temp_value[1])

        return self.rec
        # just testing :
        # for yy, o in enumerate(self.rec):
        #     for xx, i in enumerate(o):
        #         print(self.rec[yy][xx].value)

# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- functions ----------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

# ----------------------------------------------- generate neighbors ------------------------------------------------- #


def generate_neighbors():                                   # generates a dictionary which tells us what the neighbors
    graph = {}                                              # of any given rectangle is and returns this dictionary
    for o in range(0, 35):
        for i in range(0, 62):

            if o == 0 or o == 34:
                if o == 0:
                    if i == 0:
                        graph.update({(o, i): [(o, i + 1), (o + 1, i)]})

                    elif i == 61:
                        graph.update({(o, i): [(o + 1, i), (o, i - 1)]})

                    else:
                        graph.update({(o, i): [(o + 1, i), (o, i + 1), (o, i - 1)]})
                elif o == 34:
                    if i == 0:
                        graph.update({(o, i): [(o - 1, i), (o, i + 1)]})

                    elif i == 61:
                        graph.update({(o, i): [(o - 1, i), (o, i - 1)]})

                    else:
                        graph.update({(o, i): [(o - 1, i), (o, i + 1), (o, i - 1)]})

            elif i == 0 or i == 61:
                if i == 0:
                    graph.update({(o, i): [(o + 1, i), (o - 1, i), (o, i + 1)]})

                if i == 61:
                    graph.update({(o, i): [(o + 1, i), (o - 1, i), (o, i - 1)]})

            else:
                graph.update({(o, i): [(o + 1, i), (o - 1, i), (o, i + 1), (o, i - 1)]})

    return graph


# ----------------------------------------------- generate neighbors ------------------------------------------------- #


def generate_neighbors_astar():                             # generates a dictionary which tells us what the neighbors
    graph = {}                                              # of any given rectangle is and returns this dictionary
    for o in range(0, 35):
        for i in range(0, 62):

            if o == 0 or o == 34:
                if o == 0:
                    if i == 0:
                        graph.update({(o, i): [(o, i + 1), (o + 1, i), (o + 1, i + 1)]})

                    elif i == 61:
                        graph.update({(o, i): [(o + 1, i), (o, i - 1), (o + 1, i - 1)]})

                    else:
                        graph.update({(o, i): [(o + 1, i), (o, i + 1), (o, i - 1), (o + 1, i + 1), (o + 1, i - 1)]})
                elif o == 34:
                    if i == 0:
                        graph.update({(o, i): [(o - 1, i), (o, i + 1), (o - 1, i + 1)]})

                    elif i == 61:
                        graph.update({(o, i): [(o - 1, i), (o, i - 1), (o - 1, i - 1)]})

                    else:
                        graph.update({(o, i): [(o - 1, i), (o, i + 1), (o, i - 1), (o - 1, i - 1), (o - 1, i + 1)]})

            elif i == 0 or i == 61:
                if i == 0:
                    graph.update({(o, i): [(o + 1, i), (o - 1, i), (o, i + 1), (o + 1, i + 1), (o + 1, i - 1)]})

                if i == 61:
                    graph.update({(o, i): [(o + 1, i), (o - 1, i), (o, i - 1), (o + 1, i - 1), (o - 1, i + 1)]})

            else:
                graph.update({(o, i): [(o + 1, i), (o - 1, i), (o, i + 1), (o, i - 1), (o + 1, i + 1), (o + 1, i - 1),
                                       (o - 1, i + 1), (o - 1, i - 1)]})

    return graph


# --------------------------------------------- follow cursor function ----------------------------------------------- #


def follow_cursor(pos, rect):
    rect.draw_moving_clicking(pos)


# ------------------------------------------- initialize screen function --------------------------------------------- #


def init_screen():                                          # initializes the screen.
    rectangles = []                                         # calls the __init__ function from Rectangle with the
    for i in range(0, 35):                                  # starting image for every rectangle which will be on screen
        new_rectangle = []                                  # and also calls for each of them the draw function as well
        for o in range(0, 62):                              # as add them sorted into an array within an array which
            new_rectangle.append(Rectangle(start_img))      # represent: ---------------- [row][column] ----------------
            new_rectangle[o].draw(o * 30, i * 30 + 30)
        rectangles.append(new_rectangle)

    return rectangles


# ------------------------------------- checks if any rectangle is clicked on ---------------------------------------- #


def rectangle_clicked(pos, rectangles, choice):
    for i in range(0, 35):
        for o in range(0, 62):
            rectangles[i][o].mouse_rectangle(pos, choice)


# -------------------------------------- transforms if its currently checked ----------------------------------------- #


def transformation_checking(rectangle):
    rectangle.transform_is_checking()


# --------------------------------------- transforms if its already checked ------------------------------------------ #


def transformation_checked(rectangle):
    rectangle.transform_is_checked()


# ------------------------------------- gives back which algorithm was chosen ---------------------------------------- #


def get_choices(pos, choices):
    r_this = ["WALL", 1, 0]
    for i in range(0, len(choices)):
        if choices[i].choice == "EXIT":
            r_this[0] = choices[i].draw(1920 - 60, 1, pos)
        else:
            r_this[0] = choices[i].draw(i * 60, 1, pos)

        if r_this[0] != "NULL":
            return r_this
    return "NULL"


# ------------------------------------- gives back which algorithm was chosen ---------------------------------------- #


def start_rectangle(pos, rectangles, choice, current_start):
    if choice == "START":
        if not current_start:
            for i in range(0, 35):
                for o in range(0, 62):
                    jupp = rectangles[i][o].mouse_rectangle(pos, choice)
                    if jupp:
                        coordinates = (i, o)
                        return coordinates

    elif choice == "START_DEL":
        if current_start:
            for i in range(0, 35):
                for o in range(0, 62):
                    jupp = rectangles[i][o].mouse_rectangle(pos, choice)
                    if jupp is None:
                        return None

                    if not jupp:
                        coordinates = (-1, -1)
                        return coordinates

                    else:
                        return None


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------- main ------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


def main():
    # set the maximum recursion depth to 3000
    sys.setrecursionlimit(3000)
    
    # flag for the main loop
    running = True
    
    # create a clock to control the frame rate
    clock = pygame.time.Clock()
    
    # create a list of button choices
    choices = [Choice(dfs_img, dfs_clicked_img, dfs_hover_img, "DFS"),
               Choice(bfs_normal_img, bfs_clicked_img, bfs_hover_img, "BFS"),
               Choice(astar_normal_img, astar_clicked_img, astar_hover_img, "ASTAR"),
               Choice(wall_img, wall_clicked_img, wall_hover_img, "WALL"),
               Choice(start_b_img, start_b_clicked_img, start_b_hover_img, "START"),
               Choice(finish_img, finish_clicked_img, finish_hover_img, "FINISH"),
               Choice(clear_img, clear_clicked_img, clear_hover_img, "CLEAR"),
               Choice(exit_normal_img, exit_clicked_img, exit_hover_img, "EXIT")
               ]
    
    # possible choices for the algorithm
    possible_c = ["DFS", "BFS", "ASTAR", "WALL", "START", "FINISH", "CLEAR", "EXIT"]
    
    # initialize the screen and create rectangles for the grid
    rectangles = init_screen()
    
    # set the default algorithm choice to "WALL"
    algorithm_choice = "WALL"
    
    # flag for whether a start point has been set
    start_exists = False
    
    # coordinates for the current rectangle
    coordinates = (0, 0)
    
    # variable for tracking clicks on the A* algorithm button
    astar_click = 1
    
    # generate the graph of neighboring rectangles
    graph = generate_neighbors()
    
    # variable for tracking the state of the algorithm
    c = 1
    
    # coordinates for the current rectangle
    current_rectangle = (-1, -1)
    
    # flag for whether the algorithm has been drawn on the screen
    alg_drawn = False
    
    # main loop
    while running:
        # get the current mouse position
        pos = pygame.mouse.get_pos()
    
        # tick the clock to control the frame rate
        clock.tick()
    
        # check if the mouse is hovering over any buttons
        curr_c = get_choices(pos, choices)
    
        # get the current button choice and the corresponding button's index
        current_choice = curr_c[0]
        t = curr_c[1]
        z = curr_c[2]
    
        # update the algorithm choice if the current choice is a valid choice
        if current_choice in possible_c:
            algorithm_choice = current_choice
    
        # use a match statement to decide which algorithm to run based on the algorithm_choice variable
        match algorithm_choice:
            case "DFS":
                # create a list of threads to update the rectangles in parallel
                threads = []
                for o in range(0, 35):
                    trd = []
                    for i in range(0, 62):
                        trd.append(threading.Thread(target=transformation_checking, args=(rectangles[o][i],)))
                    threads.append(trd)
                dfs = DFS()
                if z == 0:
                    if alg_drawn:
                        for o in range(0, 35):
                            for i in range(0, 62):
                                if not rectangles[o][i].is_wall() \
                                        and not rectangles[o][i].is_finish() \
                                        and not rectangles[o][i].start:

                                    alg_drawn = False
                                    rectangles[o][i].mouse_rectangle((0, 0), "CLEAR")

                    visited_tf.clear()
                    print(rectangles)
                    dfs.find_finish(rectangles, graph, current_rectangle)
                    c = 0
                    z += 1

                if len(visited_tf) != 0 and c == 0:
                    c = 1
                    for o in visited_tf:
                        if o != current_rectangle:
                            try:
                                threads[o[0]][o[1]].start()
                                alg_drawn = True

                            except RuntimeError:
                                break

                            pygame.time.delay(2)

                    path = dfs.find_path_optimal(graph, current_rectangle)
                    threads = []
                    for o in range(0, 35):
                        trd = []
                        for i in range(0, 62):
                            trd.append(threading.Thread(target=transformation_checked, args=(rectangles[o][i],)))
                        threads.append(trd)

                    if path is not None:
                        for o in path:
                            try:
                                threads[o[0]][o[1]].start()
                            except RuntimeError:
                                break

                            pygame.time.delay(20)

            case "BFS":
                if current_rectangle != (-1, -1):
                    threads = []
                    for o in range(0, 35):
                        trd = []
                        for i in range(0, 62):
                            trd.append(threading.Thread(target=transformation_checking, args=(rectangles[o][i],)))
                        threads.append(trd)
                    bfs = BFS(graph)
                    if t == 1:
                        if alg_drawn:
                            for o in range(0, 35):
                                for i in range(0, 62):
                                    if not rectangles[o][i].is_wall() \
                                            and not rectangles[o][i].is_finish() \
                                            and not rectangles[o][i].start:

                                        alg_drawn = False
                                        rectangles[o][i].mouse_rectangle((0, 0), "CLEAR")

                        visited_bfs = bfs.find_finish(current_rectangle, rectangles)
                        t -= 1
                        for o in visited_bfs:
                            try:
                                if o != current_rectangle:
                                    threads[o[0]][o[1]].start()
                                    alg_drawn = True

                            except RuntimeError:
                                pass

                            pygame.time.delay(2)

                        path = bfs.find_path_optimal(current_rectangle)
                        threads_ff = []
                        for o in range(0, 35):
                            trd_ff = []
                            for i in range(0, 62):
                                trd_ff.append(threading.Thread(target=transformation_checked, args=(rectangles[o][i],)))
                            threads_ff.append(trd_ff)
                        try:
                            for o in path:
                                try:
                                    threads_ff[o[0]][o[1]].start()
                                    pygame.time.delay(20)
                                except RuntimeError:
                                    pass

                        except TypeError:
                            pass

                        visited_bfs.clear()

            case "ASTAR":
                if astar_click == 1:
                    astar_click = 0
                    astar = Astar(rectangles, current_rectangle)
                    finish = (-1, -1)
                    for yy, o in enumerate(rectangles):
                        for xx, i in enumerate(o):
                            if i.is_finish():
                                finish = (xx, yy)

                    rectangles = astar.give_values(finish)
                    astar.find_finish(current_rectangle)
                    v = astar.filtered_v

                    threads = []
                    for o in range(0, 35):
                        trd = []
                        for i in range(0, 62):
                            trd.append(threading.Thread(target=transformation_checking, args=(rectangles[o][i],)))
                        threads.append(trd)

                    for draw in v:
                        threads[draw[0]][draw[1]].start()
                        pygame.time.delay(20)

            case "WALL":
                rectangle_clicked(pos, rectangles, algorithm_choice)

            case "CLEAR":
                for o in range(0, 35):
                    for i in range(0, 62):
                        if not rectangles[o][i].is_wall():
                            rectangles[o][i].mouse_rectangle((0, 0), "CLEAR")
                algorithm_choice = "WALL"
                c = 1
                astar_click = 1
                current_rectangle = (-1, -1)
                start_exists = False
                visit.clear()
                visited_tf.clear()

            case "START":
                if start_exists:
                    starting_coordinates = start_rectangle(pos, rectangles, "START_DEL", start_exists)

                else:
                    starting_coordinates = start_rectangle(pos, rectangles, algorithm_choice, start_exists)
                    if starting_coordinates is not None:
                        current_rectangle = starting_coordinates

                if starting_coordinates is None:
                    starting_coordinates = coordinates

                if starting_coordinates == (-1, -1):
                    start_exists = False

                else:
                    start_exists = True
                    coordinates = starting_coordinates

            case "FINISH":
                rectangle_clicked(pos, rectangles, algorithm_choice)

            case "EXIT":
                running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------- program start --------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


main()


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------- end -------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
