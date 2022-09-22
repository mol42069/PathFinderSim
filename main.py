# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------- imports ------------------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


import pygame


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------ global variables -------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


grey = (30, 30, 30)
pygame.init()
x = 1920
y = 1080
screen_size = (x, y)
display = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
display.fill(grey)

# ----------------------------------------------------- images ------------------------------------------------------- #

starting_img = pygame.image.load('images/grey.png').convert_alpha()
exit_img = pygame.image.load('images/exit.png').convert_alpha()
exit_clicked_img = pygame.image.load('images/exit_clicked.png').convert_alpha()
exit_hover_img = pygame.image.load('images/exit_hover.png').convert_alpha()
click_img = pygame.image.load('images/click.png').convert_alpha()
white_start_img = pygame.image.load('images/starting.png').convert_alpha()
border_img = pygame.image.load('images/border.png').convert_alpha()
transform1_img = pygame.image.load('images/transform_1.png').convert_alpha()
transform2_img = pygame.image.load('images/transform_2.png').convert_alpha()


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------- button which can move and changes on click and hover ------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


class Button:

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


class ButtonCaM:

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

    def __init__(self, white_image, transform_img1, transform_img2, wall_img):          # later also start and finish...
        self.white_image = white_image
        self.transform_img1 = transform_img1
        self.transform_img2 = transform_img2
        self.wall_img = wall_img

        white_image_width = white_image.get_width()
        white_image_height = white_image.get_height()

        transform_img1_width = transform_img1.get_width()
        transform_img1_height = transform_img1.get_height()

        transform_img2_width = transform_img2.get_width()
        transform_img2_height = transform_img2.get_height()

        wall_img_width = wall_img.get_width()
        wall_img_height = wall_img.get_height()

        self.rect = white_image.get_rect()

        self.start = False
        self.finish = False
        self.wall = False
        self.left_click = False
        self.right_click = False

# ------------------------------------------------- draw function ---------------------------------------------------- #

    def draw(self, bx=0, by=0):
        self.rect.topleft = (bx, by)

        display.blit(self.white_image, (self.rect.x, self.rect.y))

# -------------------------------------- draw if mouse on rectangle function ----------------------------------------- #

    def mouse_rectangle(self, pos):

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.left_click:
                self.left_click = True
                self.wall = True
                display.blit(self.wall_img, (self.rect.x, self.rect.y))

            elif pygame.mouse.get_pressed()[0] != 1:
                self.left_click = False

            if pygame.mouse.get_pressed()[2] == 1 and not self.right_click:
                self.right_click = True
                self.wall = False
                display.blit(self.white_image, (self.rect.x, self.rect.y))

            elif pygame.mouse.get_pressed()[2] != 1:
                self.right_click = False

# -------------------------------------- draw if mouse on rectangle function ----------------------------------------- #

    def transform(self):
        
        pass

# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------- drop-down menu --------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


class DropDown:

    def __init__(self):
        pass


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- functions ----------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


def follow_cursor(rect):
    pos = pygame.mouse.get_pos()
    rect.draw_moving_clicking(pos)


# ------------------------------------------- initialize screen function --------------------------------------------- #


def init_screen():
    rectangles = []
    for i in range(0, 35):
        new_rectangle = []
        for o in range(0, 64):
            new_rectangle.append(Rectangle(white_start_img, transform1_img, transform2_img, border_img))
            new_rectangle[o].draw(o * 30, i * 30 + 30)
        rectangles.append(new_rectangle)

    return rectangles


# ------------------------------------- checks if any rectangle is clicked on ---------------------------------------- #


def rectangle_clicked(rectangles):
    pos = pygame.mouse.get_pos()
    for i in range(0, 35):
        for o in range(0, 64):
            rectangles[i][o].mouse_rectangle(pos)


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------- main ------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


def main():

    running = True
    clock = pygame.time.Clock()
    # pos = pygame.mouse.get_pos()
    # rect = ButtonCaM(pos[0], pos[1], starting_img, click_img, 0.2, 0.2)
    exit_button = Button(1920 - 70 * 0.4, 0, exit_img, exit_clicked_img, exit_hover_img, 0.4, 0.3)
    i = 0
    rectangles = init_screen()
    while running:
        clock.tick(144)
        # follow_cursor(rect)
        rectangle_clicked(rectangles)
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
