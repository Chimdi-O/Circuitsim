import tkinter as tk
from tkinter import filedialog
import re 


root = tk.Tk()
root.title("Circuit sim")
root.canvas = tk.Canvas(root,  bg="white", height=300)
root.canvas.pack(expand =True, fill=tk.BOTH)


class Controller(): 
     def __init__(self): 
        self.components = []
        self.componentsinrange = []
        self.current_component_features = [] 
        self.mouse_position = (0,0)
        self.selected_component = ""
        self.type_selected = ""
        self.current_mouse_event = None
        self.creating_component = False
        self.editing = False      
        
     #
     def set_component(self,label): 
      global whatprogramdoin
      whatprogramdoin.config(text="creating_components")
      self.type_selected = label 
      component_features = []

      
      
      if self.type_selected == "Resistor": 
            inputwindow = tk.Tk() 
            root.title("Input Window") 
           
            def submit(): 
                
                component_features.append(int(input_1.get()))
                inputwindow.destroy()
      
            label_1 = tk.Label(inputwindow,text="Resistance")
            input_1 = tk.Entry(inputwindow)
            submit_button = tk.Button(inputwindow,text="input",command=submit)

            label_1.pack()
            input_1.pack()
            submit_button.pack() 
 
      elif self.type_selected == "Wire": 
           
        component_features.append(0)

      elif self.type_selected == "Capacitor": 
           inputwindow = tk.Tk() 
           root.title("Input Window") 

           def submit(): 
                
                component_features.append(int(input_1.get()))
                inputwindow.destroy()
      
           label_1 = tk.Label(inputwindow,text="Capacitance")
           input_1 = tk.Entry(inputwindow)
           submit_button = tk.Button(inputwindow,text="input",command=submit)

           label_1.pack()
           input_1.pack()
           submit_button.pack() 
            
      elif self.type_selected == "Battery": 
           inputwindow = tk.Tk() 
           root.title("Input Window") 
         
           def submit(): 
                component_features.append(int(input_1.get()))
                component_features.append(int(input_2.get()))
                inputwindow.destroy()
      
           label_1 = tk.Label(inputwindow,text="Supplied voltage")
           input_1 = tk.Entry(inputwindow)  
           label_2 = tk.Label(inputwindow,text="Resistance")
           input_2 = tk.Entry(inputwindow) 
           submit_button = tk.Button(inputwindow,text="input",command=submit)

           label_1.pack()
           input_1.pack()
           label_2.pack()
           input_2.pack()
           submit_button.pack() 
            
      elif self.type_selected == "LED": 
           component_features.append(0)

      if self.type_selected != "":
          self.current_component_features = component_features
          self.creating_component = True
      
     def create_component(self,component_features,mode): 
        global Resistor, Wire, Capacitor, Battery, Led

        if self.type_selected == "Resistor": 
            component = Resistor(component_features) 
        
        elif self.type_selected == "Wire": 
            component = Wire() 

        elif self.type_selected == "Capacitor": 
            component = Capacitor(component_features)
        
        elif self.type_selected == "Battery": 
            component = Battery(component_features)
        
        elif self.type_selected == "LED": 
            component = Led() 

        component.start_pos = self.mouse_position
        component.end_pos = self.mouse_position
        
        controller.components.append(component)
        
        component.draw_line()

        self.selected_component = component

       
     def checkandconnect(self): 
          
          for i in self.components[:-1]:
               distances = [
                    ((i.start_pos[0]-self.components[-1].start_pos[0])**2 + (i.start_pos[1]-self.components[-1].start_pos[1])**2)**0.5 ,
                    ((i.end_pos[0]-self.components[-1].start_pos[0])**2 + (i.end_pos[1]-self.components[-1].start_pos[1])**2)**0.5,
                    ((i.start_pos[0]-self.components[-1].end_pos[0])**2 + (i.start_pos[1]-self.components[-1].end_pos[1])**2)**0.5,
                    ((i.end_pos[0]-self.components[-1].end_pos[0])**2 + (i.end_pos[1]-self.components[-1].end_pos[1])**2)**0.5  
                    ]
     
               if distances[0] < 15: 
                         self.components[-1].start_pos = i.start_pos
                         self.components[-1].connections[0] = i
                         i.connections[0] = self.components[-1]

               if distances[1] < 15: 
                         self.components[-1].start_pos = i.end_pos  
                         self.components[-1].connections[0] = i
                         i.connections[1] = self.components[-1] 

               if distances[2] < 15: 
                    self.components[-1].end_pos = i.start_pos
                    self.components[-1].connections[1] = i
                    i.connections[0] = self.components[-1]

               if distances[3] < 15: 
                         self.components[-1].end_pos = i.end_pos
                         self.components[-1].connections[1] = i
                         i.connections[1] = self.components[-1]
               
               self.selected_component.move_line()
        
     def create_circuit(self): 
         global Circuit 

         circuit = Circuit()
         circuit.calculate()
    
     def save(self): 
         
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                circuit_data = "component,[startx,starty,endx,endy],[circle at start_pos  stuff],[circle at end_pos stuff]\n"
                component_type_encoder = {"Resistor":"r","Capacitor":"c","Battery":"b","Led":"l"}

                for component in self.components:
                    circuit_data += component_type_encoder[component.type]
                    circuit_data += f",{root.canvas.coords(component.geometry[0])}"
                    if component.type == "Capacitor": 
                         circuit_data += "," + str(component.capacitance)

                    if component.type == "Resistor": 
                         circuit_data += "," + str(component.resistance)         

                    if component.type == "Battery": 
                         circuit_data += "," + str(component.resistance)
                         circuit_data+= "," + str(component.supplied_voltage)

                    
                    circuit_data += "\n"     
                
                     
                file.write(circuit_data)

     def load(self): 
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path , "r") as file: 
                 component_type_decoder = {"r":"Resistor","c":"Capacitor","b":"Battery","l":"Led"}
                 circuit_data = file.read()
                 circuit_data = circuit_data.split("\n")
                 circuit_data = circuit_data[1:-1]
     
                 for component_data in circuit_data: 
                      component_data = re.findall(r'\[.*?\]|[^,]+', component_data)
                      component_data[1] = component_data[1].strip("[]")
                      component_data[1] =[ float(x) for x in component_data[1].split(",")]
                      
                      for i in range(2,len(component_data[2:])+2):
                           component_data[i] = float(component_data[i])
                           

                      self.selected_component = component_type_decoder[component_data[0]]
                           

                      self.create_component(
                           component_data[1][0],
                           component_data[1][1],
                           component_data[1][2],
                           component_data[1][3],
                           component_data[2:],
                           True
                           )
     
     def clear_canvas(self): 
         root.canvas.delete("all")
     
     def find_distances(self): 
          for component in self.components: 
               component.mouse2start = ((self.mouse_position[0]-component.start_pos[0])**2 + (self.mouse_position[1]-component.start_pos[1])**2)**0.5
               component.mouse2end = ((self.mouse_position[0]-component.end_pos[0])**2 + (self.mouse_position[1]-component.end_pos[1])**2)**0.5
               
          
     def edit(self):
          global whatprogramdoin
          whatprogramdoin.config(text="editing")
          self.creating_component = False
          self.editing = True     
          
          for component in self.components: 
               
               if component.mouse2start < 20: 
                    component.start_pos = self.mouse_position

               if component.mouse2end < 20: 
                    component.end_pos = self.mouse_position
                    
               component.move_line() 



     def handle_mouse_event (self,event,event_type):
          self.mouse_position = [event.x,event.y]
          
          self.current_mouse_event = event_type

          
          if self.current_mouse_event == "<Button-1>": 
               if self.creating_component == True: 
                    self.create_component(self.current_component_features,"create")  

               

          if self.current_mouse_event == "<B1-Motion>": 
             
               if self.creating_component == True: 
                    self.selected_component.move_line(endx=self.mouse_position[0],endy=self.mouse_position[1])
                    self.checkandconnect()

               elif self.editing == True: 
                    self.edit()
                    


          if self.current_mouse_event == "<Motion>": 
             self.find_distances()
             pass
            

          if self.current_mouse_event == "<ButtonRelease-1>":
               if self.creating_component == True: 
                    self.components.append(self.selected_component)
                    self.selected_component = ""

      
controller = Controller()

root.canvas.bind("<B1-Motion>",lambda event: controller.handle_mouse_event(event,"<B1-Motion>"))
root.canvas.bind("<Motion>",lambda event: controller.handle_mouse_event(event,"<Motion>"))
root.canvas.bind("<Button-1>",lambda event: controller.handle_mouse_event(event,"<Button-1>"))
root.canvas.bind("<Button-3>",lambda event: controller.handle_mouse_event(event,"<Button-3>"))
root.canvas.bind("<ButtonRelease-1>",lambda event: controller.handle_mouse_event(event,"<ButtonRelease-1>"))


menubar = tk.Menu(root)

component_menu = tk.Menu(menubar, tearoff=0)
component_menu.add_command(label="Wire", command=lambda: controller.set_component("Wire"))
component_menu.add_command(label="Resistor", command=lambda: controller.set_component("Resistor"))
component_menu.add_command(label="Battery", command=lambda: controller.set_component("Battery"))
component_menu.add_command(label="Capacitor", command=lambda: controller.set_component("Capacitor"))
component_menu.add_command(label="LED", command=lambda: controller.set_component("LED"))

menubar.add_cascade(label="Components", menu=component_menu)
menubar.add_command(label="Calculate", command=controller.create_circuit)
menubar.add_command(label="Save", command=controller.save)
menubar.add_command(label="Load", command=controller.load)
menubar.add_command(label="Clear",command=controller.clear_canvas)
menubar.add_command(label="Edit",command= controller.edit)

root.config(menu=menubar)

stop_button_frame =  tk.Frame(root)
stop_button_frame.place(relx=0, rely=0,relwidth=1,relheight=0.05)
whatprogramdoin = tk.Label(stop_button_frame, text="")
whatprogramdoin.pack()

right_click_menu = tk.Menu(root, tearoff = 0) 
right_click_menu.add_command(label ="Edit") 



#wire class lets goo!!!! YEAHHHH!!!! 
class Circuit: 
     def __init__(self): 
        self.resistance = 0 
        self.current = 0 
        self.emf = 0 
        self.components = controller.components
    
     def calculate(self): 
          for text in root.canvas.find_withtag("text"):
             
             root.canvas.delete(text)

          for component in self.components: 
               if component.type == "Resistor" or component.type == "Battery": 
                    self.resistance += component.resistance
                
                    if component.type =="Battery": 
                         self.emf += component.supplied_voltage

          self.current = self.emf / self.resistance 

          for component in self.components:     
                text = ""
                component.current = self.current

                if component.type == "Battery": 
                     component.voltage_taken = component.resistance * component.current
                     text = f"Supplied voltage: {component.supplied_voltage}\nVoltage: {round(component.voltage_taken,2)}\nResistance: {component.resistance}\nCurrent: {round(component.current,2)}"

                if component.type == "Resistor": 
                     component.voltage_taken = component.resistance * component.current
                     text = f"Voltage: {round(component.voltage_taken,2)}\nResistance: {component.resistance}\nCurrent: {round(component.current,2)}"

                if component.type == "Capacitor" or component == "Led": 
                     text = f"Current: {round(component.current,2)}"

                root.canvas.create_text((component.start_pos[0] + component.end_pos[0])/2 ,(component.start_pos[1] + component.end_pos[1])/2 - 50, text =  text)
                
                    

class Wire: 
     def __init__(self): 
            self.start_pos = "EMPTY"
            self.end_pos = "EMPTY"
            self.geometry = "EMPTY"
            self.drawing = False 
            self.symbol = False
            self.connections = ["None","None"] # [start,end] # possibly completely useless 
            self.type = "Wire"
            self.current = 0
            self.mouse2start = 21
            self.mouse2end = 21


     def draw_line(self): 
          self.geometry = [root.canvas.create_line(self.start_pos[0], self.start_pos[1],self.end_pos[0],self.end_pos[1], fill="black", width=3),
                 root.canvas.create_oval(self.start_pos[0] - 10  , self.start_pos[1] - 10, self.start_pos[0] + 10, self.start_pos[1] + 10  ,fill="blue"),
                 root.canvas.create_oval(self.end_pos[0] - 10  , self.end_pos[1] - 10, self.end_pos[0] + 10, self.end_pos[1] + 10  ,fill="blue")]
          if self.symbol: 
                 self.geometry.append(root.canvas.create_image((self.start_pos[0] + self.end_pos[0])/2 ,(self.start_pos[1] + self.end_pos[1])/2, anchor=tk.CENTER, image=self.symbol))
            
     def move_line(self,startx=False,starty=False,endx=False,endy=False):
          if startx and starty: 
               self.start_pos = [startx,starty]
          if endx and endy: 
               self.end_pos = [endx,endy]
          
          root.canvas.coords(self.geometry[0],self.start_pos[0], self.start_pos[1],self.end_pos[0],self.end_pos[1])
          root.canvas.coords(self.geometry[1],self.start_pos[0] - 10  , self.start_pos[1] - 10, self.start_pos[0] + 10, self.start_pos[1] + 10)
          root.canvas.coords(self.geometry[2],self.end_pos[0] - 10  , self.end_pos[1] - 10, self.end_pos[0] + 10, self.end_pos[1] + 10)
          
          if self.symbol: 
               root.canvas.coords(self.geometry[3],(self.start_pos[0] + self.end_pos[0])/2 ,(self.start_pos[1] + self.end_pos[1])/2)

class Resistor(Wire): 
    def __init__(self,component_features): 
          super().__init__() 
          self.symbol = tk.PhotoImage(file ="symbol image\Resistor.png")
          self.resistance = component_features[0]
          self.voltage_taken = 0 
          self.type = "Resistor"
          

class Capacitor(Wire): 
    def __init__(self,component_features): 
          super().__init__() 
          self.symbol = tk.PhotoImage(file="symbol image\Capacitor.png")
          self.capacitance = component_features[0]
          self.voltage_taken = 0 
          self.type = "Capacitor"

class Battery(Wire): 
    def __init__(self,component_features): 
        super().__init__() 
        self.symbol = tk.PhotoImage(file="symbol image\Cell.png")
        self.resistance = component_features[0]
        self.supplied_voltage = component_features[1]
        self.type = "Battery"

class Led(Wire): 
    def __init__(self): 
        super().__init__() 
        self.symbol = tk.PhotoImage(file="symbol image\LED.png")
        self.type = "Led"
        self.voltage_taken = 0 

root.mainloop()