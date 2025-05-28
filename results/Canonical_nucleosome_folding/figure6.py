from graphviz import Graph

# Read pathways and percentages from file
def read_pathways_with_percentages(filename):
    pathways = []
    with open(filename, 'r') as file:
        for line in file:
            pathway, percentage = line.strip().split()
            pathways.append((pathway.split(','), int(percentage)))
    return pathways

# Read states and probabilities from file
def read_states_with_probabilities(filename):
    states = {}
    with open(filename, 'r') as file:
        for line in file:
            state, probability = line.strip().split(',')
            states[state] = float(probability)
    return states

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
state_number_to_name = {
    '1': 'HR2',
    '2': 'HR3',
    '3': 'T',
    '4': 'HL',
    '6': 'T1',
    '7': 'T2',
    '9': 'HR',
    '10': 'N',
}

# Provide the filenames of your files containing pathways, probabilities, and colors
pathways_file = 'pathways.txt'  # Change this to your pathways file name
probabilities_file = 'prob_nuc.txt'  # Change this to your probabilities file name
colors_file = 'colors.txt'  # Change this to your colors file name

# Read pathways and percentages from file
pathways_with_percentages = read_pathways_with_percentages(pathways_file)

# Read states and probabilities from file
states_with_probabilities = read_states_with_probabilities(probabilities_file)

# Read state numbers and colors from file
states_with_colors = read_states_with_colors(colors_file)

# Initialize Graphviz Graph with circo layout
dot = Graph(engine='circo')

# Add nodes to the graph with colors and size based on probabilities
for state, probability in states_with_probabilities.items():
    color = states_with_colors.get(state, 'black')  # Use black color if state color is not specified
    # Set shape='circle' to ensure the nodes are strictly circular
    width1 = "{:.2f}".format((1/probability)*1.5)
    print (width1)
    dot.node(state, label=state_number_to_name[state], style='filled', fillcolor=color,fixedsize='true', shape='circle', width=str(width1))
    #dot.edge(to_symbol, from_symbol, penwidth=str(max_percentage / 9), len='1.0', minlen='1.0', dir='back', color='blue')

# Track the edges added to the graph
added_edges = set()

# Find the pathway with maximum flux
max_flux_pathway = max(pathways_with_percentages, key=lambda x: x[1])

# Add transitions for each pathway with weighted arrows
for pathway, percentage in pathways_with_percentages:
    for i in range(len(pathway) - 1):
        from_symbol = pathway[i]
        to_symbol = pathway[i + 1]
        edge = (from_symbol, to_symbol)
        if edge not in added_edges:
            added_edges.add(edge)
            color = 'red' if pathway == max_flux_pathway[0] else 'black'
            dot.edge(from_symbol, to_symbol, penwidth=str(percentage / 9), len='1.0', minlen='1.0', dir='forward', color=color)
            dot.edge(from_symbol, to_symbol, penwidth=str(percentage / 9), len='1.0', minlen='1.0', dir='back', color=color)

            

# Save and render the graph
dot.render('transition_graph_custom_colors_and_size_with_labels', format='png', view=True)
