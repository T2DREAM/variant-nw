import os
import dash
import dash_core_components as dcc 
import dash_html_components as html
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import numpy as np
import requests
import json
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from variant_viz import VariantViz
from dash.dependencies import Input, Output
import urllib.request
import time

#initialize dash app object:
app = dash.Dash()
application = app.server
#initializae VariantViz object:
vv = VariantViz()

#initialize var_data
var_name = "rs11257655"
r1 = requests.get(vv.rsid_url(var_name))
var_data = r1.json()
all_annotations = [key for key in var_data.keys()]
#initialize number of button clicks:
rsid_button_clicks = 0

#dash app layout
app.layout = html.Div(children=[

	html.Div(children=[

		#rsid search bar
		html.Plaintext('search rsid'),
		dcc.Input(
			id='rsid-input',
			value=var_name,
			type="text"
		),

		#update button
		html.Button('update', id='rsid-button'),
		dcc.RadioItems(
			id='expand-radio',
			options = [
				{'label': "more", 'value': "more"},
				{'label': "less", 'value': "less"}
			],
			value = "more",
		),

		#annotation selection dropdown menu
		html.Plaintext('select annotations'),
		dcc.Dropdown(
			id='annotation-dropdown',
			options=[{'label': anno, 'value': anno} for anno in all_annotations],
			value=[key for key in var_data.keys()],
			multi=True
		),

		#biosample selection dropdown menu
		html.Plaintext('select biosamples'),
		dcc.Dropdown(
			id='biosample-dropdown',
			options=[{'label': biosample, 'value': biosample} for biosample in vv.get_biosamples(var_data)],
			value=[biosample for biosample in vv.get_biosamples(var_data)],
			multi=True
		)
	], style={'columnCount': 1}),

	#annotation / variant visualization graph 
	dcc.Graph(id='test-interactivity',figure=vv.make_graph(var_data=var_data, var_name=var_name)),
 
])

#function to update the annotation graph when selections have been changed
@app.callback(
	Output('test-interactivity', 'figure'),
	[Input('annotation-dropdown', 'value'),
	 Input('expand-radio', 'value'),
	 Input('rsid-input', 'value'),
	 Input('rsid-button', 'n_clicks'),
	 Input('biosample-dropdown', 'value')])
def update_graph(annot_value, expand_value, new_rsid, num_clicks, selected_biosamples):
	print("updating graph")
	print("biosamples:", len(selected_biosamples), selected_biosamples)
	global var_name
	global var_data
	global all_annotations
	global rsid_button_clicks
	print("num_clicks:", num_clicks)
	print("rsid_button_clicks", rsid_button_clicks)
	#try to update to new rsid
	if num_clicks is not None and num_clicks == rsid_button_clicks + 1:
		rsid_button_clicks += 1
		if new_rsid != var_name:
			with urllib.request.urlopen(vv.rsid_url(new_rsid)) as url:
				u = url.read()
				if u != bytes():
					var_data = json.loads(u)
					var_name = new_rsid
					#all_annotations = [key for key in var_data.keys()]
					return vv.make_graph(var_data=var_data, var_name=var_name)
				else:
					print("not a valid rsid:", new_rsid)

	#make new dict using only checked values:
	new_data = {key:val for key, val in var_data.items() if key in annot_value}

	if expand_value == "more":
		expanded = True
	else:
		expanded = False

	return vv.make_graph(var_data=var_data, var_name=var_name, subset_data=new_data, expanded=expanded, \
		biosamples=selected_biosamples)

#update menu choices when a new variant has been selected
@app.callback(
	Output('annotation-dropdown', 'options'),
	[Input('rsid-input', 'value'),
	 Input('rsid-button', 'n_clicks')])
def update_dropdown(new_rsid, num_clicks):

	global rsid_button_clicks
	global all_annotations

	#if num_clicks is not None and num_clicks == rsid_button_clicks + 1:
	if num_clicks > 0 and num_clicks is not None:
		print("updating dropdown menu")
		print("annotations:", all_annotations)
		all_annotations = [key for key in var_data.keys()]

	return [{'label': anno, 'value': anno} for anno in all_annotations]

if __name__ == '__main__':
    application.run(debug=True, port=8080)



