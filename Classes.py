import pygame
from pygame import image 
import math

images = {"Resistor":"symbol image\Resistor.jpg","Cell":"symbol image\Cell.jpg","LED":"symbol image\LED.jpg","Capacitor":"symbol image\Capacitor.jpg"} #Stores the file path for each component 

#Component class, the class each component will inherit from
class component():
    def __init__(self,identifier,connections,component_type,resistance,voltage=0,current=0,circuit=""): 
        self.id = identifier # a unique id for each component
        self.component_type = component_type 
        self.resistance = resistance 
        self.voltage = voltage 
        self.current = current 
        self.symbol = image.load(images[component_type]) #Holds the image of the component symbol 
        self.connections = connections #Holds the other components this component is connected to 
        self.circuit = circuit

    #calculates the current and voltage of the components 
    def calculate(self): 
        self.current = self.circuit.current
        self.voltage = self.resistance * self.current 

class battery(component): 
    def __init__(self,identifier,component_type,supplied_voltage,resistance,current=0,voltage=0): 
        super().__init__(identifier,component_type,resistance,current,voltage)
        self.supplied_voltage = supplied_voltage #Holds the voltage that the battery will supply 

class capacitor(component):
    def __init__(self,identifier,component_type,capacitance,stored_voltage,total_resistance=0,current=0,voltage=0):
        super().__init__(self,identifier,component_type,current=0,voltage=0)
        self.stored_voltage = stored_voltage
        self.total_resistance = total_resistance #Holds a copy of the total resistance in the circuit
        self.capacitance = capacitance

    # This calculates how the voltage in a capacitor will change as time moves on
    def calculate(self,time_step):  
        #If the voltage in the circuit is lower than the voltage in the capacitor than it will start to discharge 
        if self.circuit.voltage > self.stored_voltage: 
            self.stored_voltage = self.stored_voltage*math.e**(-1*time_step/(self.resistance*self.capacitance))
            
        #if the voltage in the circuit is higher than the voltage in the capacitor than it will start to charge
        if self.circuit.voltage < self.stored_voltage: 
            self.stored_voltage = self.stored_voltage*(1-math.e**(-1*time_step/(self.resistance*self.capacitance)))
                    

class circuit(): 
    def __init__(self,components=[],voltage=0,current=0,resistance=0): 
        self.components = components
        self.voltage = voltage 
        self.current = current
        self.resistance = resistance

    #Calculates the current and voltage in the circuit 
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