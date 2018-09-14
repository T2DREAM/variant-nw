# Variant Network Visualization Tool 
Variant Network Visualization Tool. Credit for Dash tool @smorabit

# Deployment of Dash Server


Dash App original repository - https://github.com/smorabit/variant-viz
# Variant / Annotation Visualization

A [Dash](https://plot.ly/products/dash/) webapp for visualizing the annotation network of a variant in the Diabetes Epigenome Atlas. Consists of two python scripts, variant_viz.py and dash_visualize.py. [Here](https://dash.plot.ly/getting-started) is a tutorial for getting familiar with Dash. 

## Dependencies 
* [Dash](https://dash.plot.ly/installation) version - 
* [plotly](https://plot.ly/python/getting-started/) version - (Note :)
* Python3

## variant_viz.py

Contains the VariantViz class, which is where the bulk of the code for generating the variant / annotation network graph exists.

* generate_positions()
    - From annotation data, generates x, y coordinates of where text goes on the network graph. These coordinates are later used to draw shapes around the text.
* generate_shapes()
    - Uses x,y coordinates from generate_positions() to draw shapes around annotation text.
* make_graph()
    - A wrapper that calls generate_positions(), generate_shapes(), and various helper functions in order to make a plot.ly graph. 
* The rest of the functions in the VariantViz class are helper functions for the above three functions.

## dash_visualize.py

Script that creates an empty Dash app object, initializes the variant / annotation network graph using variant rs11257655 (as a placeholder for now), and creates some buttons and dropdown menus that enable the user to alter the network graph however the see fit. Refer to the Dash documentation to see what types of html elements can be generated using the Dash framework.



* update_graph() 
    - Re-draws the network graph after the user makes selections using the dropdown menus.
* update_dropdown()
    - Re-populates the dropdown menus if the user has searched for a different variant.


