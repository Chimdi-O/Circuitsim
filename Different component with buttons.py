
import pygame 
from pygame import image
import math
import numpy
import sys
images = {"Resistor":"symbol image\Resistor.jpg","Cell":"symbol image\Cell.jpg","LED":"symbol image\LED.jpg","Capacitor":"symbol image\Capacitor.jpg"} 

pygame.init()
# This initialises the program 

screen = pygame.display.set_mode((500,500))
#This creates a window which as the width 1280 and height 720 

buttonscreen2 =pygame.display.set_mode((500,500))

pygame.display.set_caption("Interactive components")
#This sets the name of the display to "interactive components"



button = pygame.button

mouse_pressed = False
#This tells the program if the mouse is currently being pressed 

class component():
# defines the component class
    def __init__(self,identifier=0,connections=0,component_type=0,resistance=0,voltage=0,current=0,circuit="",start_pos=(0,0),end_pos=(0,0)): 
        
        self.id = identifier
        # A unique identifier for each one of the components

        self.component_type = component_type
        # Stores type of component which the component is e.g battery, cell

        self.resistance = resistance 
        # Stores the resistance of component

        self.voltage = voltage 
        # Stores the voltage of the component

        self.current = current 
        # Stores the current of the component

        #self.symbol = image.load(images[component_type])
        # Stores the image that will be displayed when the component is placed

        self.connections = connections
        # A list which stores which components the things are connected to

        self.circuit = circuit
        # Stores the circuit class which this component is in 

        self.start_pos = start_pos
        # Stores the start position of the component 

        self.end_pos = end_pos
        # Stores the end position of the component


    
    def calculate(self): 
    #This will calculate the current for using the current of the entire circuit
        
        self.current = self.circuit.current
        #This will update the current in the current in the component using the current in the circuit

        self.voltage = self.resistance * self.current 
        #Using the current and the resistance it will find the voltage

    def draw(self): 
         
         pygame.draw.line(screen, BLACK, self.start_pos, self.end_pos, 2)
         ##pygame.draw.line(screen,(20,20,20),pygame.mouse.get_pos(),comp.start_pos,2 )
         ##pygame.draw.line(screen,(0,20,20),pygame.mouse.get_pos(),comp.end_pos,2 )

         """print(comp.find_distance(pygame.mouse.get_pos()))"""
         


    """ def find_distance(self,mouse_position): 
        # this will find the distance between the mouse and the wire using trig 
            
            gradient = (self.start_pos[1]-self.end_pos[1])/(self.start_pos[0]-self.end_pos[0])
            
            equation_of_start2end =  numpy.polyfit(self.start_pos,self.end_pos,1)
            equation_of_mouse2line = numpy.array()
            numpy.linalg.solve(equation_of_start2end,) """


BLACK = (0,0,0)
# This initialised the value Black which will be used later in the program

components = []
#This is a list which stores all of the classes for the circuits currently in the program

current_component_index = -1 
#This stores the index of the component currently being placed it is -1 as it is incremented each time the program is run 

running = True 
#Stores if the program is running or not 

mouse_pressed = False
#This stores if the mouse is currently being pressed 

current_component = False
#This stores the current component class being drawn

def gameloop():
#Gameloop 
    
    screen.fill((255, 255, 255))
    #Makes the screen white

    mouse_position = pygame.mouse.get_pos()
    # sets the mouse position to where the mouse is 

    for event in pygame.event.get():
    #loops through all of the events in the game

                if event.type == pygame.QUIT:
                # If your press the quit button then QUIT!
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                #If you left click a component is created and added to the components list adn the current component index is updates 

                        mouse_pressed = True
                        
                        current_component = component(start_pos=mouse_position,end_pos=mouse_position)
                            
                elif event.type == pygame.MOUSEBUTTONUP: 
                    if event.button == 1: 
                # When the user lets go of the left mouse button it updates the mouse button to that 
                        if current_component.start_pos != current_component.end_pos: 

                            components.append(current_component)
                            current_component_index += 1
                            mouse_pressed = False
                       

                elif event.type == pygame.MOUSEMOTION: 
                        if  mouse_pressed: 
                #When the user moves their mouse it updates the position the component currently being drawn

                             current_component.end_pos = mouse_position 
            

         
    if current_component:
                for  comp in components: 
                    
                    if mouse_position:
                                
                        comp.draw()


  
            #if the mouse is pressed and the left mouse button is pressed then register the mouse being clicked as true and change start position to the mouse position


    pygame.display.flip()
    #This updates the dispay
