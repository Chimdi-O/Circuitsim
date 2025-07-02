

import pygame 


#This initialises the pygame window
pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Interactive Wires")

mouse_pressed = False #This tells the program if the mouse is currently being pressed 

#Wire class which stores the start and end coordinates of the wire 
class Wire(): 
    def __init__(self,start_pos=(0,0),end_pos=(0,0)): 
        self.start_pos = start_pos
        self.end_pos = end_pos

BLACK = (0,0,0) #This initialises the value Black which will be used later in the program
wires = [] #This is a list which stores all of the classes for the wires  currently in the program
current_wire_index = -1 #This stores the index of the component currently being placed it is -1 as it is incremented each time the program is run 
running = True #Stores if the program is running or not 
mouse_pressed = False#This stores if the mouse is currently being pressed 
current_wire = None#This stores the current wire class being drawn

#Gameloop 
while running:
    #Makes the screen white
    screen.fill((255, 255, 255)) 

    mouse_position = pygame.mouse.get_pos() #Sets the mouse position to where the mouse is 

    #Loops through all of the events in the program
    for event in pygame.event.get():
    
                #If your press the quit button then quit the program
                if event.type == pygame.QUIT:
                    running = False
                
                #If you left click a wire is created and added to the wires list adn the current wire index is updates
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pressed = True
                        
                        current_wire = Wire()

                        current_wire.start_pos = mouse_position
                        current_wire.end_pos = mouse_position
                
                        wires.append(current_wire)
                        current_wire_index += 1
                        

                # When the user lets go of the left mouse button it updates the mouse_pressed to False
                elif event.type == pygame.MOUSEBUTTONUP: 
                    if event.button == 1: 
                        mouse_pressed = False
                       
                #When the user moves their mouse it updates the position the wire currently being drawn
                elif event.type == pygame.MOUSEMOTION: 
                        if  mouse_pressed: 
                             current_wire.end_pos = mouse_position 

                #Draws the current line the other if statements serve as input validation
                elif current_wire != None:
                    if current_wire.start_pos is not None and current_wire.end_pos is not None:
                                 pygame.draw.line(screen, BLACK, current_wire.start_pos, current_wire.end_pos, 2)
                    
    #Draws every wire in the list 
    for wire in wires: 
        pygame.draw.line(screen, BLACK, wire.start_pos, wire.end_pos,2)

    #This updates the dispay
    pygame.display.flip()
    

