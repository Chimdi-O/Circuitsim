import random

# Dictionaries which represent classes
Component1 = {"name": "battery", "t1": "wire"}
Component2 = {"name": "wire", "t1": "resistor"}
Component3 = {"name": "resistor", "t1": "battery"}

nodes = [Component1, Component2, Component3]  # The components are abstracted as a graph and therefore are called nodes
visited = []  # Holds the visited nodes
unvisited = nodes  # Holds the nodes which have not been visited yet which at the start of the program is all of them
all_circuit = []  # Holds all the circuits in the program
circuit = []  # Holds the circuit currently being produced

#finds all of the circuits in program
def find(circuit):
    current_component = ""

    #loops through the process below till there are no more unvisited components
    while unvisited: 
        
        # if there is not component selected then it sets the start point to a random node
        if not current_component:  
            current_component = random.choice(unvisited)


        circuit.append(current_component)
        unvisited_names = [i["name"] for i in unvisited]
        
        #if the next component up has not been visited move to it
        if current_component in unvisited:  
            current_component_index = unvisited_names.index(current_component["t1"]) #Move on to the next component using connections 
            current_component = unvisited[current_component_index]
            visited.append(unvisited.pop(current_component_index))

        #If the next up component is explored then the circuit is finished and it's done
        if current_component not in unvisited:  
            all_circuit.append(circuit)
            circuit = []
            current_component = ""
        

    return print( f"we may have done it...\n\n lets check!\n\nthese are the unvisited components {unvisited}\n\n and these are the visited {visited}\n\n and these are the circuits {all_circuit} ")


find(circuit)
