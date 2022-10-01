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
pygame.init()
x = 1920
y = 1080
screen_size = (x, y)
display = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
display.fill(grey)
visit = []

# ----------------------------------------------------- images ------------------------------------------------------- #


exit_img = pygame.image.load('images/exit.png').convert_alpha()
exit_clicked_img = pygame.image.load('images/exit_clicked.png').convert_alpha()
exit_hover_img = pygame.image.load('images/exit_hover.png').convert_alpha()
click_img = pygame.image.load('images/click.png').convert_alpha()
dfs_img = pygame.image.load('images/DFS.png').convert_alpha()
dfs_clicked_img = pygame.image.load('images/DFS_clicked.png').convert_alpha()
dfs_hover_img = pygame.image.load('images/DFS_hover.png').convert_alpha()
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


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------- button which can move and changes on click and hover ------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


class Button:                                   # is the EXIT-Button

    def __init__(self, bx, by, image, cimage, h_image, scale_x=0.9, scale_y=0.9):

        self.scale_x = scale_x
        self.scale_y = scale_y

        width = image.get_width()
        height = image.get_height()

        c_width = cimage.get_width()
        c_height = cimage.get_height()

        h_width = h_image.get_width()
        h_height = h_image.get_height()

        self.image = pygame.transform.scale(image, (int(width * scale_x), int(height * scale_y)))
        self.clicked_img = pygame.transform.scale(cimage, (int(c_width * scale_x), int(c_height * scale_y)))
        self.hover_img = pygame.transform.scale(h_image, (int(h_width * scale_x), int(h_height * scale_y)))

        self.rect = image.get_rect()
        self.rect.topleft = (bx, by)
        self.clicked = False

# -------------------------------------------------- draw function --------------------------------------------------- #

    def draw(self):

        is_hovering = False
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

            else:
                is_hovering = self.mouse_hover()

        else:
            action = False
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            action = False
            self.clicked = False

        if not is_hovering:
            display.blit(self.image, (self.rect.x, self.rect.y))

        return action

# ---------------------------------------------- draw moving function ------------------------------------------------ #

    def draw_moving(self, pos):

        action = False
        if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            action = True
            self.clicked = True

        if pygame.mouse.get_pressed()[0] == 1:
            display.blit(self.clicked_img, (pos[0] - 5, pos[1] - 5))

        if pygame.mouse.get_pressed()[0] == 0:
            display.fill(grey)
            display.blit(self.image, (pos[0] - 5, pos[1] - 5))
            action = False
            self.clicked = False

        return action

# ----------------------------------------- draw a different image function ------------------------------------------ #

    def draw_different_img(self, choice=True):

        if choice:
            display.blit(self.clicked_img, (self.rect.x, self.rect.y))

        else:
            display.blit(self.image, (self.rect.x, self.rect.y))

# ---------------------------------------------- mouse-hover function ------------------------------------------------ #

    def mouse_hover(self):

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 0:
            display.blit(self.hover_img, (self.rect.x, self.rect.y))
            return True

        else:
            display.blit(self.image, (self.rect.x, self.rect.y))
            return False


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------ button which can move and changes on click ------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


class ButtonCaM:                                # USELESS

    def __init__(self, bx, by, image, cimage, scale_x=0.9, scale_y=0.9):

        self.scale_x = scale_x
        self.scale_y = scale_y

        width = image.get_width()
        height = image.get_height()
        c_width = cimage.get_width()
        c_height = cimage.get_height()

        self.image = pygame.transform.scale(image, (int(width * scale_x), int(height * scale_y)))
        self.clicked_img = pygame.transform.scale(cimage, (int(c_width * scale_x), int(c_height * scale_y)))

        self.rect = image.get_rect()
        self.rect.topleft = (bx, by)
        self.clicked = False

# ---------------------------------------------- draw moving function ------------------------------------------------ #

    def draw_moving_clicking(self, pos):

        action = False

        if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            action = True
            self.clicked = True

        if pygame.mouse.get_pressed()[0] == 1:
            display.blit(self.clicked_img, (pos[0] - 5, pos[1] - 5))

        if pygame.mouse.get_pressed()[0] == 0:
            display.fill(grey)
            display.blit(self.image, (pos[0] - 5, pos[1] - 5))
            action = False
            self.clicked = False

        return action


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------- Background rectangles ----------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


class Rectangle:

    # TODO: add the finish

    def __init__(self, starting_img):               # this function initializes a rectangle with all needed variables
        self.starting_img = starting_img
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

    # TODO: add the finish

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

            case "END":
                pass

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
# ---------------------------------------------------- algorithm ----------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


def dfs(rectangles, graph, current):                        # here we write the oder of the rectangles into visit
    if current not in visit:                                # for DFS and check if the rectangle is a wall
        visit.append(current)                               # TODO: when finish is added need to check if algorithm
        key = (current[0], current[1])                      # TODO: is finished and make it stop as well as print the
        for neighbor in graph[key]:                         # TODO: path which was calculated by the DFS
            if not rectangles[neighbor[0]][neighbor[1]].is_wall():
                dfs(rectangles, graph, neighbor)


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
                        graph.update({(o, i): [(o + 1, i), (o, i + 1)]})

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
    for i in range(0, len(choices)):
        current = choices[i].draw(60 + i * 60, 1, pos)

        if current != "NULL":
            return current
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
    sys.setrecursionlimit(3000)
    running = True
    clock = pygame.time.Clock()

    choices = [Choice(dfs_img, dfs_clicked_img, dfs_hover_img, "DFS"),
               Choice(greed_img, greed_clicked_img, greed_hover_img, "GREEDY"),
               Choice(wall_img, wall_clicked_img, wall_hover_img, "WALL"),
               Choice(start_b_img, start_b_clicked_img, start_b_hover_img, "START"),
               Choice(clear_img, clear_clicked_img, clear_hover_img, "CLEAR")
               ]

    exit_button = Button(1920 - 70 * 0.4, 0, exit_img, exit_clicked_img, exit_hover_img, 0.4, 0.3)
    i = 0
    rectangles = init_screen()
    algorithm_choice = "WALL"
    start_exists = False
    coordinates = (0, 0)
    graph = generate_neighbors()
    z = 1
    c = 1
    current_rectangle = (0, 0)
    threads = []
    for o in range(0, 35):
        trd = []
        for i in range(0, 62):
            trd.append(threading.Thread(target=transformation_checking, args=(rectangles[o][i],)))
        threads.append(trd)

    while running:
        pos = pygame.mouse.get_pos()
        clock.tick()
        current_choice = get_choices(pos, choices)

        if current_choice != "NULL":
            algorithm_choice = current_choice

        match algorithm_choice:                                                     # here the algorithms will be used
            case "DFS":
                if z == 0:
                    dfs(rectangles, graph, current_rectangle)
                    print("is here")
                    c = 0
                    z += 1

                if len(visit) != 0 and c == 0:
                    c = 1
                    for o in visit:
                        if o != current_rectangle:
                            threads[o[0]][o[1]].start()
                            pygame.time.delay(2)

                    threads = []
                    for o in range(0, 35):
                        trd = []
                        for i in range(0, 62):
                            trd.append(threading.Thread(target=transformation_checking, args=(rectangles[o][i],)))
                        threads.append(trd)

            case "GREEDY":
                pass

            case "WALL":
                rectangle_clicked(pos, rectangles, algorithm_choice)

            case "CLEAR":
                rectangles = init_screen()
                algorithm_choice = "WALL"
                z = 1
                c = 1
                start_exists = False
                visit.clear()

            case "START":
                if start_exists:
                    starting_coordinates = start_rectangle(pos, rectangles, "START_DEL", start_exists)

                else:
                    starting_coordinates = start_rectangle(pos, rectangles, algorithm_choice, start_exists)
                    if starting_coordinates is not None:
                        current_rectangle = starting_coordinates
                        z = 0

                if starting_coordinates is None:
                    starting_coordinates = coordinates

                if starting_coordinates == (-1, -1):
                    start_exists = False

                else:
                    start_exists = True
                    coordinates = starting_coordinates

        if exit_button.draw():
            i += 1
            exit_button.draw_different_img()
            if i > 0:
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
