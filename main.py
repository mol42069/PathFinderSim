import pygame
grey = (30, 30, 30)
pygame.init()
x = 1920
y = 1080
screen_size = (x, y)
display = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
display.fill(grey)
exit_img = pygame.image.load('exit.png').convert_alpha()
rect_img = pygame.image.load('button.png').convert_alpha()


class Button:

    def __init__(self, x, y, image, scale_x, scale_y):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale_x),int(height * scale_y)))
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            action = False
            self.clicked = False

        display.blit(self.image, (self.rect.x, self.rect.y))

        return action


class rectangles:

     def __init__(self, x, y, image, scale_x = 1, scale_y =1):
        width = image.get_width()
        height = image.get_height() 
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale))
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        pass


def main():

    running = True
    clock = pygame.time.Clock()

    exit_button = Button(1920 - 70 * 0.4, 0, exit_img, 0.4, 0.3)

    while running:
        clock.tick(500)
        if exit_button.draw():
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()


main()

