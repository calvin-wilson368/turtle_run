import pygame


def coordinates(target):
    from main import WIDTH, screen, font
    lines = [f"x: {target.x:.0f}", f"y: {target.y:.0f}"]

    for i, line in enumerate(lines):
        text = font.render(line, True, "white")
        text_rect = text.get_rect(topright=(WIDTH - 40, 220 + i * 100))
        screen.blit(text, text_rect)
    pygame.display.flip()


def fps():
    from main import WIDTH, screen, font, clock
    text = font.render(f"FPS: {clock.get_fps():.0f}", True, "white")
    text_rect = text.get_rect(topright=(WIDTH - 40, 140))
    screen.blit(text, text_rect)