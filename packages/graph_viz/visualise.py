from graphviz import Graph
import os

# Creates a flowchart diagram of the intersections and connections between them
# Renders and saves the file in the provided fileType (png by default)
def createFlowchart(filename, intersectionData, fileType="png"):
    dot = Graph(comment="Intersection Data", strict=True, format=fileType)
    dot.attr(label="Map of Intersections")

    #Creates all of the ndoes
    for node in list(set(intersectionData)):
        dot.node(str(node), str(node))

    #Adds all of the edges
    for i in range(len(intersectionData) - 1):
        node1 = str(intersectionData[i])
        node2 = str(intersectionData[i+1])
        if node1 == node2:
            # Self loop
            continue
        dot.edge(node1, node2)
    #Removes the generated image file if it exists
    try:
        os.remove(filename+'.{}'.format(fileType))
    except OSError:
        pass
    #generates the image of graph
    dot.render(filename, view=True)

# Intersection data is the list of intersections visited, such that 
# adjacent terms in this list will be connected intersections 
# Example call:
# createFlowchart('intersection', [1,2,3,4,3,5,6,7,4,2,4,3,6,6,6])
