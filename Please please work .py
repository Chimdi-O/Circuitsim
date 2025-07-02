import random 

class component():
    def __init__(self,name): 
        self.name = name
        self.connection = ""

class circuit(): 
    def __init__(self,components): 
        self.components = components

def look(graph,node):

    def find(graph,node,visited=None): 
        if visited == None: 
            visited = []
        if node not in visited: 
            visited.append(node)
            print(f"the current node is {node.name}")
            find(graph,node.connection,visited)

        return visited 

    visited = [] 
    unvisited = graph 
    while unvisited != []: 
        circuit = find(unvisited,random.choice(unvisited))

        visited.append(circuit)
        for component in circuit: 
            unvisited.remove(component)

    return visited
    
    


components = [component("0"),component("1"),component("2"),component("3"),component("4"),component("5"),component("6"),component("7")]

components[0].connection = components[1]
components[1].connection  = components[2]
components[2].connection = components[3]
components[3].connection = components[0]

components[4].connection = components[5]
components[5].connection  = components[6]
components[6].connection = components[7]
components[7].connection = components[4]

circuit = look(components,random.choice(components))
print(f"the circuit is {circuit}")





    