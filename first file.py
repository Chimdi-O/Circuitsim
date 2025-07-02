import sys
import pygame


#This initialises the program setting the size of the window and the name 
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Circuit simulator")

#This stores the RGB values of colors in variables with their name so when they are used later in the program it is more human readable
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


#The wire is the most basic component and so is the one I chose to do first. The idea is that subsequent component types will inherit from this class. 
class Wire:

    def __init__(self, start, end, color=BLACK):
        self.start = start # this stores the coordinates where the wire starts 
        self.end = end # This stores the coordinates where the wire ends
        self.color = color# This stores the color of the wire 

    #This function takes no input apart from self and draws the wire on screen using the aforementioned attributes 
    def draw(self):
        pygame.draw.line(screen, self.color, self.start, self.end, 2)

    #This function takes the current position of the wire as input and returns True if the mouse is within a certain area of the wire and false if not
    #This would of been used so when the user clicks on the wire they would be able to interact with it 
    def is_mouse_over(self, mouse_pos):
        return pygame.Rect(self.start, (self.end[0] - self.start[0], self.end[1] - self.start[1])).collidepoint(mouse_pos)

wires = [] #list that will store all of the wire instances 
coord = [] #temp variable for storing the start position
running = True # This stores if the program is running or not, When the user quits it will be set to false 

#This is the gameloop code within this will run repeatedly while the program is open 
while running:
    #This goes through all of the events that are currently occuring. An event is any way the user interacts with the program e.g clicking, dragging etc
    for event in pygame.event.get():
        #When the user presses the quit button the program will close 
        if event.type == pygame.QUIT:
            running = False
    #makes screen white 
    screen.fill(WHITE)

    #Draws every component that has been created on the screen
    for wire in wires:
        wire.draw()

    #This updates the display so all of the changes made to the screen before this line (wires drawn) will be displayed visually 
    pygame.display.flip()

    #goes through all of the events in the progrma
    for event in pygame.event.get():
        #If the user lets go of their mouse and a component is being drawn it will finish drawing and get added to the wires list
        #coord is being used here as if there is no component currently being drawn it will be empty and will return False
        if event.type == pygame.MOUSEBUTTONUP and coord: 
          wires.append(Wire(coord,(pygame.mouse.get_pos()) ))
          coord = []

        #When the user clicks while not component is currently being created the coord gets set to the mouse's current position
        if event.type == pygame.MOUSEBUTTONDOWN and not coord:
            coord = (pygame.mouse.get_pos())

        
        mouse_pos = pygame.mouse.get_pos() # This variable stores the mouses current position

        #This goes through every wire in the program and if the mouse is over a wire it makes that wire turn from black to red 
        for wire in wires:
            if wire.is_mouse_over(mouse_pos):
                wire.color = RED
                print("Mouse over Wire!")
            else:
                wire.color = BLACK

#Ends the program after the gameloop stops running
pygame.quit()
sys.exit()
