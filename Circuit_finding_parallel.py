# Import necessary modules
import tkinter as tk
from tkinter import filedialog
import re 

# Create the main Tkinter window
root = tk.Tk()
root.title("Circuit sim")

# Create a canvas to draw components on
root.canvas = tk.Canvas(root, bg="white", height=300)
root.canvas.pack(expand=True, fill=tk.BOTH)

# Controller class to manage components and interactions
class Controller(): 
    def __init__(self): 
        # Initialize lists to store components and their connections
        self.components = []
        self.componentsinrange = []
        self.current_component_features = [] 
        self.mouse_position = (0,0)
        self.selected_component = ""
        self.type_selected = ""
        self.current_mouse_event = None
        self.creating_component = False
        self.editing = False      
        
    # Method to set the type of component to create
    def set_component(self, label): 
        global whatprogramdoin
        whatprogramdoin.config(text="creating_components")
        self.type_selected = label 
        component_features = []

        # Display input window based on selected component type
        if self.type_selected == "Resistor": 
            inputwindow = tk.Tk() 
            root.title("Input Window") 
           
            def submit(): 
                component_features.append(int(input_1.get()))
                inputwindow.destroy()
      
            label_1 = tk.Label(inputwindow, text="Resistance")
            input_1 = tk.Entry(inputwindow)
            submit_button = tk.Button(inputwindow, text="input", command=submit)

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
      
            label_1 = tk.Label(inputwindow, text="Capacitance")
            input_1 = tk.Entry(inputwindow)
            submit_button = tk.Button(inputwindow, text="input", command=submit)

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
      
            label_1 = tk.Label(inputwindow, text="Supplied voltage")
            input_1 = tk.Entry(inputwindow)  
            label_2 = tk.Label(inputwindow, text="Resistance")
            input_2 = tk.Entry(inputwindow) 
            submit_button = tk.Button(inputwindow, text="input", command=submit)

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
      
    # Method to create a component based on selected type and features
    def create_component(self, component_features, mode): 
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
        
        # Add component to list and draw it on the canvas
        controller.components.append(component)
        component.draw_line()

        self.selected_component = component

    # Method to check for and establish connections between components
    def checkandconnect(self): 
        for i in self.components[:-1]:
            distances = [
                ((i.start_pos[0] - self.components[-1].start_pos[0])**2 + (i.start_pos[1] - self.components[-1].start_pos[1])**2)**0.5,
                ((i.end_pos[0] - self.components[-1].start_pos[0])**2 + (i.end_pos[1] - self.components[-1].start_pos[1])**2)**0.5,
                ((i.start_pos[0] - self.components[-1].end_pos[0])**2 + (i.start_pos[1] - self.components[-1].end_pos[1])**2)**0.5,
                ((i.end_pos[0] - self.components[-1].end_pos[0])**2 + (i.end_pos[1] - self.components[-1].end_pos[1])**2)**0.5
            ]

            # Check distances to establish connections
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
        
    # Method to create a circuit
    def create_circuit(self): 
        global Circuit 

        circuit = Circuit()
        circuit.calculate()
    
    # Method to save circuit data to a file
    def save(self): 
         
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                circuit_data = "component,[startx,starty,endx,endy],[circle at start_pos  stuff],[circle at end_pos stuff]\n"
                component_type_encoder = {"Resistor": "r", "Capacitor": "c", "Battery": "b", "Led": "l"}

                for component in self.components:
                    circuit_data += component_type_encoder[component.type]
                    circuit_data += f",{root.canvas.coords(component.geometry[0])}"
                    if component.type == "Capacitor": 
                         circuit_data += "," + str(component.capacitance)

                    if component.type == "Resistor": 
                         circuit_data += "," + str(component.resistance)

                    if component.type == "Battery": 
                         circuit_data += "," + str(component.voltage) + "," + str(component.resistance)

                    circuit_data += "," + str(root.canvas.coords(component.geometry[1])) 
                    circuit_data += "\n"

                file.write(circuit_data)
           
    # Method to load circuit data from a file
    def load(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                for line in file:
                    data = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                    component_type_decoder = {"r": "Resistor", "c": "Capacitor", "b": "Battery", "l": "Led"}

                    if data[0] == "r" or data[0] == "c" or data[0] == "b" or data[0] == "l": 
                        component_features = []

                        if data[0] == "c": 
                            component_features.append(float(data[4]))
                            controller.set_component("Capacitor")

                        if data[0] == "r": 
                            component_features.append(float(data[4]))
                            controller.set_component("Resistor")

                        if data[0] == "b": 
                            component_features.append(float(data[4]))
                            component_features.append(float(data[5]))
                            controller.set_component("Battery")

                        if data[0] == "l": 
                            controller.set_component("LED")
                     
                        controller.create_component(component_features, None)

controller = Controller()  # Initialize the controller

# Main menu
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Save", command=controller.save)
filemenu.add_command(label="Load", command=controller.load)
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

# Labels to indicate current program status
whatprogramdoin = tk.Label(root, text="What's the program doing?", bd=1, relief=tk.SUNKEN, anchor=tk.W)
whatprogramdoin.pack(side=tk.BOTTOM, fill=tk.X)

# Event handling for mouse movements and clicks
def handle_mouse_event(event): 
    controller.mouse_position = (event.x, event.y)
    controller.current_mouse_event = event

    if controller.creating_component: 
        controller.create_component(controller.current_component_features, None)
        controller.creating_component = False

    if event.widget == root.canvas: 
        if event.type == "4": 
            controller.checkandconnect()

root.canvas.bind("<Motion>", handle_mouse_event)
root.canvas.bind("<ButtonRelease>", handle_mouse_event)

# Start the Tkinter main loop
root.mainloop()
