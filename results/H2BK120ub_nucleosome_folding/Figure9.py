import numpy as np
from graphviz import Digraph

def normalize_probabilities(probabilities, min_size=0.1, max_size=1.0):
    ''' Normalize probabilities to a range between min_size and max_size
    '''
    # Calculate the sum of probabilities
    total = np.sum(probabilities)
    # Normalize probabilities to the range [min_size, max_size]
    normalized = (probabilities / total) * (max_size - min_size) + min_size
    return normalized

def render_transition_graph_with_probabilities(transition_matrix_file, state_probabilities_file, state_labels, cutoff):
    ''' Render the transition network using Graphviz with node sizes determined by state probabilities
    '''
    # Read transition matrix from file
    transition_matrix = np.loadtxt(transition_matrix_file)

    # Read state probabilities from file
    state_probabilities = np.loadtxt(state_probabilities_file)

    # Initialize a new Digraph
    g = Digraph(format='png')

    # Normalize state probabilities to determine node sizes
   # node_sizes = normalize_probabilities(state_probabilities, min_size=0.1, max_size=1.0)

    # Add nodes with labels and sizes based on state probabilities
    for i, label in enumerate(state_labels):
        node_size = (1/state_probabilities[i])
        print (node_size)
        g.node(str(i), label=label, width=str(node_size), height=str(node_size))

    # Add edges with weights
    for i in range(len(state_labels)):
        for j in range(len(state_labels)):
            weight = transition_matrix[i, j]
            if i != j and weight > cutoff:  # Exclude self-transitions and transitions below the cutoff
                # Reduce connection length and display transition values in scientific notation
               connection_length = 1 / weight
               print (connection_length)
               g.edge(str(i), str(j), label='%.2e' % weight, len=str(connection_length-1.00))

    # Render and save the graph
    g.render('transition_graph_with_probabilities', view=True)

# Define state labels
#state_labels = ['State 0', 'State 1', 'State 2', 'State 3', 'State 4', 'State 5', 'State 6', 'State 7', 'State 8', 'State 9', 'State 10']
state_labels=["HR", "HR1", "HL" , "N", "T1", "T2", "T", "T3", "T4", "Part_T", "T5"]
# File containing transition matrix
transition_matrix_file = 'transition_matrix_hb1.txt'

# File containing state probabilities
state_probabilities_file = 'prob_hb1.txt'

# Cut-off for transition rate
transition_cutoff = 5.39e-12

# Render the transition network with probabilities
render_transition_graph_with_probabilities(transition_matrix_file, state_probabilities_file, state_labels, transition_cutoff)
