 

import pygame 
from pygame import image
import math
import numpy
import random
import copy

images = {"Resistor":"symbol image\Resistor.jpg","Cell":"symbol image\Cell.jpg","LED":"symbol image\LED.jpg","Capacitor":"symbol image\Capacitor.jpg"} 
pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Interactive components")
BLACK = (0,0,0)
components = []
current_component_index = -1 
running = True 
mouse_pressed = False
mouse_pressed = False
component_selected = "Resistor"


class component():
    def __init__(self,component_type,connections=0,resistance=0,voltage=0,current=0,circuit="",start_pos=(0,0),end_pos=(0,0)): 
        self.component_type = component_type
        self.resistance = resistance
        self.voltage = voltage 
        self.current = current 
        self.symbol = image.load(images[component_type]) #image.load(images[component_type])
        self.connections = []
        self.circuit = circuit
        self.start_pos = start_pos
        self.end_pos = end_pos

    def calculate(self): #This will calculate the current for using the current of the entire circuit
        self.current = self.circuit.current
        self.voltage = self.resistance * self.current 

    def draw(self): 
        pygame.draw.line(screen, BLACK, self.start_pos, self.end_pos, 2)
        pygame.draw.circle(screen,(0,0,255),self.start_pos, 10)
        pygame.draw.circle(screen,(0,0,255),(self.end_pos), 10)
        screen.blit(self.symbol,(round(((self.start_pos[0]+self.end_pos[0]))/2),round(((self.start_pos[1]+self.end_pos[1]))/2)))
        

class battery(component): 
    def __init__(self,component_type,supplied_voltage=0,connections=0,resistance=0,voltage=0,current=0,circuit="",start_pos=(0,0),end_pos=(0,0)):  
        super().__init__(component_type,connections,resistance,voltage,current,circuit,start_pos,end_pos)
        self.supplied_voltage = supplied_voltage

class capacitor(component):
    def __init__(self,component_type,supplied_voltage=0,connections=0,resistance=0,voltage=0,current=0,circuit="",start_pos=(0,0),end_pos=(0,0),capacitance=0,stored_voltage=0,total_resistance=0):  
        super().__init__(component_type,connections,resistance,voltage,current,circuit,start_pos,end_pos)
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

    def Calculate(self):   
        for component in self.components: 
            if component.component_type == "Cell": 
                self.voltage += component.supplied_voltage
            self.resistance += component.resistance

        self.current = self.voltage / self.resistance
        
        for component in self.components: 
            if component.component_type == "capacitor": 
                component.resistance = self.resistance
            component.calculate(self.current)
                   
          
def checkandconnect(item,current_component):
         start2startDist = ((current_component.start_pos[0]-item.start_pos[0])**2 + (current_component.start_pos[1]-item.start_pos[1])**2)**0.5
         start2endDist = ((current_component.start_pos[0]-item.end_pos[0])**2 + (current_component.start_pos[1]-item.end_pos[1])**2)**0.5
         end2startDist = ((current_component.end_pos[0]-item.start_pos[0])**2 + (current_component.end_pos[1]-item.start_pos[1])**2)**0.5
         end2endDist = ((current_component.end_pos[0]-item.end_pos[0])**2 + (current_component.end_pos[1]-item.end_pos[1])**2)**0.5  

         if start2startDist < 20: 
            components[current_component_index].start_pos = item.start_pos
            components[current_component_index].connections.append(item)
            
         if start2endDist < 20: 
            components[current_component_index].start_pos = item.end_pos
            components[current_component_index].connections.append(item)
            
         if end2startDist < 20: 
            components[current_component_index].end_pos = item.start_pos
            components[current_component_index].connections.append(item)

         if end2endDist < 20: 
            components[current_component_index].end_pos = item.end_pos
            components[current_component_index].connections.append(item)