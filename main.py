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
starting_img = pygame.image.load('grey.png').convert_alpha()
exit_img = pygame.image.load('exit.png').convert_alpha()
exit_clicked_img = pygame.image.load('exit_clicked.png').convert_alpha()
exit_hover_img = pygame.image.load('exit_hover.png').convert_alpha()
click_img = pygame.image.load('click.png').convert_alpha()


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------- button which can move and changes on click and hover ------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


class Button:

    def __init__(self, x, y, image, cimage, himage, scale_x=1, scale_y=1):
        self.scale_x = scale_x
        self.scale_y = scale_y
        width = image.get_width()
        height = image.get_height()
        c_width = cimage.get_width()
        c_height = cimage.get_height()
        h_width = himage.get_width()
        h_height = himage.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale_x), int(height * scale_y)))
        self.clicked_img = pygame.transform.scale(cimage, (int(c_width * scale_x), int(c_height * scale_y)))
        self.hover_img = pygame.transform.scale(himage, (int(h_width * scale_x), int(h_height * scale_y)))
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, ):
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

    def draw_different_img(self, choice=True):
        if choice:
            display.blit(self.clicked_img, (self.rect.x, self.rect.y))
        else:
            display.blit(self.image, (self.rect.x, self.rect.y))

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

    def __init__(self, x, y, image, cimage, scale_x=1, scale_y=1):
        self.scale_x = scale_x
        self.scale_y = scale_y
        width = image.get_width()
        height = image.get_height()
        c_width = cimage.get_width()
        c_height = cimage.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale_x), int(height * scale_y)))
        self.clicked_img = pygame.transform.scale(cimage, (int(c_width * scale_x), int(c_height * scale_y)))
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

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
# ---------------------------------------------------- functions ----------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


def follow_cursor(rect):
    pos = pygame.mouse.get_pos()
    rect.draw_moving_clicking(pos)


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------- main ------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


def main():

    running = True
    clock = pygame.time.Clock()
    pos = pygame.mouse.get_pos()
    rect = ButtonCaM(pos[0], pos[1], starting_img, click_img, 0.2, 0.2)
    exit_button = Button(1920 - 70 * 0.4, 0, exit_img, exit_clicked_img, exit_hover_img, 0.4, 0.3)
    i = 0

    while running:
        clock.tick(144)
        follow_cursor(rect)
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
