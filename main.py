import pygame
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


class Button:

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

    def draw(self, hover):
        self.hover = hover
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

    def draw_moving(self):

        action = False
        pos = pygame.mouse.get_pos()
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
            display.blit(self.hover, (self.rect.x, self.rect.y))
            return True
        else:
            display.blit(self.image, (self.rect.x, self.rect.y))
            return False


class Rectangles:

    def __init__(self, x, y, image, scale_x=1.0, scale_y=1.0):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale_x), int(height * scale_y)))
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        pass


def follow_cursor(rect):
    rect.draw_moving()


def main():

    running = True
    clock = pygame.time.Clock()
    pos = pygame.mouse.get_pos()
    rect = Button(pos[0], pos[1], starting_img, click_img, 0.2, 0.2)
    exit_hover = pygame.transform.scale(exit_hover_img, (0.4, 0.3))
    exit_button = Button(1920 - 70 * 0.4, 0, exit_img, exit_clicked_img, 0.4, 0.3)
    i = 0

    while running:
        clock.tick(144)
        follow_cursor(rect)
        if exit_button.draw(exit_hover):
            i += 1
            exit_button.draw_different_img()
            if i > 0:
                running = False



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()


def initialize():

    pass


main()
