
import pygame 
from pygame import image
import math
import random


images = {"Resistor":"symbol image\Resistor.png","Cell":"symbol image\Cell.png","LED":"symbol image\LED.png","Capacitor":"symbol image\Capacitor.png"} 
pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Interactive components")
BLACK = (0,0,0)
components = []
current_component_index = -1 
circuits = []
running = True 
mouse_pressed = False
mouse_pressed = False
component_selected = "Resistor"



class component():
    def __init__(self,component_type,resistance=0,voltage=0,current=0,circuit="",startend=[(0,0),(0,0)] ): 
        self.component_type = component_type
        self.resistance = resistance
        self.voltage = voltage 
        self.current = current 
        self.symbol = image.load(images[component_type]) #image.load(images[component_type])
        self.connection = "None"
        self.circuit = circuit
        self.startend = startend 

    def calculate(self): #This will calculate the current for using the current of the entire circuit
        self.current = self.circuit.current
        self.voltage = self.resistance * self.current 

    def draw(self): #This draws the component on the screen
        pygame.draw.line(screen, BLACK, self.startend[0], self.startend[1], 2)
        pygame.draw.circle(screen,(0,0,255),self.startend[0], 10)
        pygame.draw.circle(screen,(0,0,255),(self.startend[1]), 10)
        screen.blit(self.symbol,(round(((self.startend[0][0]+self.startend[1][0]))/2),round(((self.startend[0][1]+self.startend[1][1]))/2)))
        

class battery(component): 
    def __init__(self,component_type,supplied_voltage=0,resistance=0,voltage=0,current=0,circuit="",startend=[(0,0),(0,0)]):  
        super().__init__(component_type,resistance,voltage,current,circuit,startend)
        self.supplied_voltage = supplied_voltage
        self.connection = ""

class capacitor(component):
    def __init__(self,component_type,resistance=0,voltage=0,current=0,circuit="",startend=[(0,0),(0,0)],capacitance=0,stored_voltage=0,total_resistance=0):  
        super().__init__(component_type,resistance,voltage,current,circuit,startend)
        self.connection = ""
        self.stored_voltage = stored_voltage
        self.total_resistance = total_resistance
        self.capacitance = capacitance


    def calculate(self,time_step):  # This calculates how the voltage in a capacitor will change as time moves on 
        if self.circuit.voltage > self.stored_voltage: #If the voltage in the circuit is lower than the voltage in the capacitor than it will start to discharge 
            self.stored_voltage = self.stored_voltage*math.e**(-1*time_step/(self.resistance*self.capacitance))
            
        if self.circuit.voltage < self.stored_voltage:# if the voltage in the circuit is higher than the voltage in the capacitor than it will start to charge 
            self.stored_voltage = self.stored_voltage*(1-math.e**(-1*time_step/(self.resistance*self.capacitance)))

class circuit(): 
    def __init__(self,components): 
        self.components = components
        self.voltage = 0
        self.current = 0
        self.resistance = 0

    def Calculate(self): #This calculates, wow!  
        for component in self.components: 
            if component.component_type == "Cell": 
                self.voltage += component.supplied_voltage
            self.resistance += component.resistance

        self.current = self.voltage / self.resistance
        
        for component in self.components: 
            if component.component_type == "capacitor": 
                component.resistance = self.resistance
            component.calculate(self.current)
                   
def find_distance(point1,point2):
    distance = ( (point1[0]-point2[0])**2 + (point1[1]-point2[1])**2 )**0.5 
    return distance
         
def checkandconnect(line1,lines):      
    for line2 in lines: 

        #line 1 is the current line being drawn line 2 is the line to be drawn
        if line1 == line2 or line1.startend[0] == line1.startend[1] : 
                return "this is the same line/This line starts and ends in the same place dimwit "
        # distances is in the format start2start, start2end, end2start, end2end 
        
        #This loops through each one of the components and checks if the distance is under 20 units, if it is the components snap together and form a circuit 
        for index, value in enumerate(line1.startend): 
                for index2, value2  in enumerate(line2.startend): 
                    distance = find_distance(value,value2) 

                    if distance < 20: 
                            line1.startend[index] = line2.startend[index2]
                            if index == 0: 
                                 line1.connection = line2
                            if index == 1: 
                                 line2.connection = line1
                                 
                            
        
# This finds all circuits in the program 
def find(graph,node=None,visited=None): 
    
    if len(graph) == 1: 
         return graph
    
    else: 
         if node == None: 
            node = graph[0]
         if visited == None: 
                visited = []
        
         if node.connection == "None": 
            visited.append(node)
            return visited
         
            
            
         if node not in visited:
                visited.append(node)
                find(graph,node.connection,visited)

                if visited[-2] != "None": 
                     circuits.append()
                     

                return visited




#Gameloop 
while running:
    screen.fill((255, 255, 255))
    mouse_position = pygame.mouse.get_pos()
    

    for event in pygame.event.get():  #loops through all of the events in the game
                if event.type == pygame.QUIT:
                    running = False

                #This makes it so if the user clicks a key it causes the next component to be created to be the corresponding component
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_c: 
                        component_selected = "Capacitor"
                    
                    elif event.key == pygame.K_r: 
                        component_selected = "Resistor"
                    
                    elif event.key == pygame.K_b: 
                        component_selected = "Cell"
                    
                    elif event.key == pygame.K_l: 
                        component_selected = "LED"
                
                if event.type == pygame.MOUSEBUTTONDOWN:  #If you left click a component is created and added to the components list adn the current component index is updates
                    if event.button == 1:
                        mouse_pressed = True
                        end_position = (mouse_position[0]+1,mouse_position[1]+1 )
                        if component_selected == "Capacitor":
                             components.append(capacitor(component_selected,startend=[mouse_position,end_position]))     

                        elif component_selected == "Cell": 
                            components.append(battery(component_selected,startend=[mouse_position,end_position]))

                        else:
                            components.append(component(component_selected,startend=[mouse_position,end_position]))
                        current_component_index += 1

                elif event.type == pygame.MOUSEBUTTONUP: # When the user lets go of the left mouse button it updates the mouse button to that 
                    if event.button == 1: 
                        if components[current_component_index].startend[0] != components[current_component_index].startend[1]:

                            start2startDist = 1000000
                            start2endDist = 1000000
                            end2startDist = 1000000
                            end2endDist = 1000000   
                          
                            
                            checkandconnect(components[current_component_index],components[:-1])
                            print("connected! ")
                                
                            print(f"find components (func call){find(components)}")
                            
                           

                            mouse_pressed = False
                       
                elif event.type == pygame.MOUSEMOTION: #When the user moves their mouse it updates the position the component currently being drawn
                        if  mouse_pressed: 
                             components[current_component_index].startend[0] = mouse_position 
                             
    #This draws the components the if statements serve as input validations                         
    if components:
        for item in components: 
            if mouse_position:
                item.draw() 

    pygame.display.flip()