from graphviz import Graph

# Read pathways and percentages from file
def read_pathways_with_percentages(filename):
    pathways = []
    with open(filename, 'r') as file:
        for line in file:
            pathway, percentage = line.strip().split()
            pathways.append((pathway.split(','), float(percentage)))
    return pathways

# Read states and probabilities from file


def read_states_with_probabilities(filename):
    states = {}
    with open(filename, 'r') as file:
        for line in file:
            state, probability = line.strip().split(',')
            states[state] = float(probability)
    return states

# Read transition probabilities from the DOT file
def read_transition_probabilities_from_dot(filename):
    probabilities = {}
    with open(filename, 'r') as file:
        for line in file:
            if '->' in line:
                parts = line.split('[', 1)
                if len(parts) < 2:
                    continue  # Skip if there are no attributes
                edge = parts[0].strip()
                label_part = parts[1].split(']')[0]
                label_parts = label_part.split('"')
                if len(label_parts) < 2:
                    continue  # Skip if there is no label
                probability = float(label_parts[1].strip())
                probabilities[edge] = probability
    return probabilities
# Read state numbers and colors from file
def read_states_with_colors(filename):
    states = {}
    with open(filename, 'r') as file:
        for line in file:
            state, color = line.strip().split(',')
            color = color.strip()  # Remove any leading or trailing whitespace
            states[state] = color
    return states

# Map state numbers to their respective names

# Provide the filenames of your files containing pathways, probabilities, colors, and transition probabilities
pathways_file = 'pathways.txt'  # Change this to your pathways file name
probabilities_file = 'probabilities.txt'  # Change this to your probabilities file name
colors_file = 'colors.txt'  # Change this to your colors file name
transition_probabilities_dot_file = 'new1.dot'  # Change this to your DOT file name

state_number_to_name = {
  #  '0':'HR2',
    '1': 'T',
   # '2': 'HL',
    '3': 'T2',
    '4': 'HR',
    '5': 'HL',
    '6': 'T3',
    #'7': 'HL1',
    '8': 'T1',
    '9': 'N',
    '10': 'HR1',
}
# Read pathways and percentages from file
pathways_with_percentages = read_pathways_with_percentages(pathways_file)
print (pathways_with_percentages)
# Read states and probabilities from file
states_with_probabilities = read_states_with_probabilities(probabilities_file)

# Read state numbers and colors from file
states_with_colors = read_states_with_colors(colors_file)

# Read transition probabilities from the DOT file
transition_probabilities = read_transition_probabilities_from_dot(transition_probabilities_dot_file)

print (transition_probabilities)



# Initialize Graphviz Graph with circo layout
dot = Graph(engine='circo')

# Add nodes to the graph with colors and size based on probabilities
for state, probability in states_with_probabilities.items():
    color = states_with_colors.get(state, 'black')  # Use black color if state color is not specified
    width = "{:.2f}".format((1 / probability) * 1.5)
    dot.node(state, label=state_number_to_name[state], style='filled', fillcolor=color, fixedsize='true', shape='circle', width=str(width))

# Track the edges added to the graph
added_edges = set()

print (added_edges)


print (len(transition_probabilities))
# Find the pathway with maximum flux
max_flux_pathway = max(pathways_with_percentages, key=lambda x: x[1])

# Add transitions for each pathway with weighted arrows
for pathway, percentage in pathways_with_percentages:
    for i in range(len(pathway) - 1):
        from_symbol = pathway[i]
        print (from_symbol)
        to_symbol = pathway[i + 1]
        edge = (from_symbol, to_symbol)
        #print (edge)
       # forward_probability = ""
        #backward_probability =""
       # if str(edge[0]) + " -> " + str(edge[1]) in transition_probabilities: 
       #     print (edge) 
       #     forward_probability = transition_probabilities[str(edge[0]) + " -> " + str(edge[1])]
       # if str(edge[1]) + " -> " + str(edge[0]) in transition_probabilities: 
       #     forward_probability = transition_probabilities[str(edge[1]) + " -> " + str(edge[0])]
    
        #if str(edge[1]) + " -> " + str(edge[0]) in transition_probabilities:
          #  print (edge)
         #   backward_probability = transition_probabilities[str(edge[1]) + " -> " + str(edge[0])]
        if edge not in added_edges:
            added_edges.add(edge)
            #color = 'red' if pathway == max_flux_pathway[0] else 'black'
            if pathway == max_flux_pathway[0]:
                color = 'red'
                key1 = [str(from_symbol)+ " -> " + str(to_symbol)]
                key2 = [str(to_symbol)+ " -> " + str(from_symbol)]
                dot.edge(from_symbol, to_symbol, label=str("{:.3f}".format([transition_probabilities[key] for key in key1 if key in transition_probabilities][0])), penwidth=str(percentage / 10), fontsize="12", len='1.0', minlen='1.0', dir='forward', color=color, labelfloat='true')

                dot.edge(from_symbol, to_symbol, label=str("{:.3f}".format([transition_probabilities[key] for key in key2 if key in transition_probabilities][0])), penwidth=str(percentage / 10), fontsize="12", len='1.0', minlen='1.0', dir='back', color=color, labelfloat='true')

            else:
                dot.edge(from_symbol, to_symbol, penwidth=str(percentage / 9), len='1.0', minlen='1.0', dir='forward', color='black')



# Save and render the graph
dot.render('transition_graph_custom_colors_and_size_with_labels', format='png', view=True)
