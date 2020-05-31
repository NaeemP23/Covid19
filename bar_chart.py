import csv
import numpy as np
from bokeh.io import output_notebook, show, output_file
from bokeh.layouts import column
from bokeh.plotting import figure, curdoc 
from bokeh.models import NumeralTickFormatter, Select, ColumnDataSource, CustomJS, HoverTool
import math

states = []
predictions = []
with open('predictions.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            for state in row: 
                if state == '' or state == 'predicted_cases': 
                    continue
                state = state.replace('state_', "")
                states.append(state)
            line_count += 1
        else:
            predictions.append(row[-1])
            line_count += 1
results = dict(zip(states, predictions))

states = []
predictions = []
with open('predictions.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            for state in row: 
                if state == '' or state == 'predicted_cases': 
                    continue
                state = state.replace('state_', "")
                states.append(state)
            line_count += 1
        else:
            predictions.append(row[-1])
            line_count += 1
results = dict(zip(states, predictions))

output_file = ('graph.html')

source = ColumnDataSource(data = dict(states = states, predictions = predictions))

callback = CustomJS(args=dict(source=source), code="""
    var data = source.data;
    var selection = cb_obj.value;
    var states = source.data['states'];
    var predictions = source.data['predictions'];
    for (var i = 0; i < states.length; i++) {
        if (selection == states[i]) {
            data['states'] = selection;
            data['predictions'] = predictions[i];
        }
    }
    source.data = data;
    source.change.emit();
""")

p = figure(x_range = source.data['states'], plot_height = 500, plot_width = 1500, title = 'Predictions by State')
p.vbar(x = 'states', top = 'predictions', width = 0.5, source = source)
p.xaxis.major_label_orientation = math.pi/2
p.y_range.start = 0
p.y_range.end = 375000
p.yaxis[0].formatter = NumeralTickFormatter(format = '0')
p.add_tools(HoverTool(tooltips = [('State', '@states'), ('Predicted Number of Cases', '@predictions')]))
menu = Select(options = source.data['states'], value = 'uniform', title = 'States')
menu.js_on_change('value', callback)
layout = column(menu, p)
curdoc().add_root(layout)
show(layout)
