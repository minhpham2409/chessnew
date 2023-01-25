import pygame
import pygame_gui

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

s1 = pygame.Surface((400, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((800, 600))

hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (100, 50)),
                                            text='Say Hello',
                                            manager=manager)

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == hello_button:
                hello_button.set_text("11")

        manager.process_events(event)

    manager.update(time_delta)
    s1.fill((0, 255, 0))
    manager.draw_ui(s1)
    window_surface.blit(s1, (0, 0))

    pygame.display.update()
