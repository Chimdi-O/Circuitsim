import tkinter as tk
import pygame
from pygame.locals import *

def pygame_loop(surface):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Update Pygame display
        pygame.display.update()
        surface.fill((255, 255, 255))  # Fill the surface with white color

def start_pygame(root):
    pygame.init()
    pygame.display.set_caption("Pygame Window")

    # Create a Pygame surface
    pygame_surface = pygame.display.set_mode((400, 300))

    # Run Pygame loop in a separate thread
    pygame_loop(pygame_surface)

root = tk.Tk()
root.title("Tkinter with Pygame")

# Button to start Pygame
button = tk.Button(root, text="Start Pygame", command=lambda: start_pygame(root))
button.pack()

root.mainloop()
