import csv
import numpy as np
from bokeh.io import output_notebook, show, output_file, save
from bokeh.layouts import column
from bokeh.plotting import figure, curdoc
from bokeh.models import NumeralTickFormatter, Select, ColumnDataSource, CustomJS, HoverTool, FactorRange
import math

def make_char():
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

    state_resources = []
    beds_total = []
    beds_aval = []
    ven_total = []
    ven_aval = []
    with open('PPE_Datasheet.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 1:
                state_resources.append(row[0])
                beds_total.append(row[1])
                beds_aval.append(row[2])
                ven_total.append(row[3])
                ven_aval.append(row[4])
            else:
                line_count += 1

    resources = ['beds_total', 'beds_aval', 'ven_total','ven_aval']

    data_r = {'states' : state_resources,
            'beds_total': beds_total,
            'beds_aval': beds_aval,
            'ven_total': ven_total,
            'ven_aval': ven_aval
            }

    # this creates [ ("Apples", "2015"), ("Apples", "2016"), ("Apples", "2017"), ("Pears", "2015), ... ]
    x_r = [ (s, r) for s in state_resources for r in resources ]
    counts = sum(zip(data_r['beds_total'], data_r['beds_aval'], data_r['ven_total'], data_r['ven_aval']), ()) # like an hstack

    source = ColumnDataSource(data = dict(states = states, predictions = predictions, all = predictions))
    source_rr = ColumnDataSource(data=dict(x_r=x_r, counts=counts, all_counts = counts))

    p_rr = figure(x_range=FactorRange(*x_r), plot_height=500, plot_width = 1500, title="State Resources", toolbar_location=None, tools="")

    p_rr.vbar(x='x_r', top='counts', width=0.9, source=source_rr)

    p_rr.y_range.start = 0
    p_rr.x_range.range_padding = 0.1
    p_rr.xaxis.major_label_orientation = 1
    p_rr.xgrid.grid_line_color = None


    p = figure(x_range = source.data['states'], plot_height = 500, plot_width = 1500, title = 'Predictions by State')
    p.vbar(x = 'states', top = 'predictions', width = 0.5, source = source)
    p.xaxis.major_label_orientation = math.pi/2
    p.yaxis[0].formatter = NumeralTickFormatter(format = '0')
    p.add_tools(HoverTool(tooltips = [('State', '@states'), ('Predicted Number of Cases', '@predictions')]))

    callback = CustomJS(args=dict(source=source, source_rr = source_rr), code= """
        var data = source.data;
        var selection = cb_obj.value
        var states = data['states']
        var predictions = data['predictions']
        var all = data['all']
        for (var i = 0; i < states.length; i++) {
            if (selection == 'All States'){
                predictions[i] = all[i]
            }
            else if (selection != states[i]) {
                predictions[i] = 0
            }
            else {
                predictions[i] = all[i]
            }
        }


        var data_rr = source_rr.data;
        var states_rr = data_rr['x_r']
        var resources_rr = data_rr['counts']
        var resources_rr_all = data_rr['all_counts']
        var start = -1

        for (var i = 0; i < states_rr.length; i++) {

            if (selection == 'All States'){
                resources_rr[i] = resources_rr_all[i]
            }
            else if(selection == states_rr[i][0]){
                if(start == -1){
                    start = i
                }
            }
        }

        for (var i = 0; i < states_rr.length; i++){
            if (start != -1){
                if (i >= start && i < (start + 4)){
                    resources_rr[i] = resources_rr_all[i]
                }
                else {
                    resources_rr[i] = 0
                }
            }
            else{
                resources_rr[i] = resources_rr_all[i]
            }
        }

        source_rr.change.emit();
        source.change.emit();
    """)

    menu = Select(options = source.data['states'] + ['All States'], value = 'uniform', title = 'States')
    menu.js_on_change('value', callback)

    output_file('Templates/bar_chart.html')

    layout = column(menu, p, p_rr)
    curdoc().add_root(layout)
    save(layout, filename = 'Templates/bar_chart.html')