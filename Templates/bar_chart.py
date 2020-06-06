import csv
import numpy as np
from bokeh.io import output_notebook, show, output_file, save, export_svgs, export_png
from bokeh.layouts import column, row, gridplot
from bokeh.plotting import figure, curdoc
from bokeh.models import NumeralTickFormatter, Select, ColumnDataSource, CustomJS, HoverTool, FactorRange
from bokeh.models.widgets import Paragraph, Div
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

    resources = ['Total Beds', 'Available Beds', 'Total Ventilators','Available Ventilators']

    data_r = {'states' : state_resources,
            'Total Beds': beds_total,
            'Available Beds': beds_aval,
            'Total Ventilators': ven_total,
            'Available Ventilators': ven_aval
            }

    # this creates [ ("Apples", "2015"), ("Apples", "2016"), ("Apples", "2017"), ("Pears", "2015), ... ]
    x_r = [ (s, r) for s in state_resources for r in resources ]
    counts = sum(zip(data_r['Total Beds'], data_r['Available Beds'], data_r['Total Ventilators'], data_r['Available Ventilators']), ()) # like an hstack

    source = ColumnDataSource(data = dict(states = states, predictions = predictions, all = predictions))
    source_rr = ColumnDataSource(data=dict(x_r=x_r, counts=counts, all_counts = counts))

    p_rr = figure(x_range=FactorRange(*x_r), plot_height=500, plot_width = 1200, title="State Resources - June 10th", toolbar_location=None, tools="")

    p_rr.vbar(x='x_r', top='counts', width=0.9, source=source_rr)

    p_rr.y_range.start = 0
    p_rr.x_range.range_padding = 0.1
    p_rr.xaxis.major_label_orientation = 1
    p_rr.xgrid.grid_line_color = None


    p_rr.add_tools(HoverTool(tooltips = [('Number of Resources', '@counts')]))


    p = figure(x_range = source.data['states'], plot_height = 500, plot_width = 1200, title = 'Predictions by State - June 10th', toolbar_location=None, tools="")
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

    menu = Select(options = ['All States'] + source.data['states'], value = 'All States', title = 'Select State')
    menu.js_on_change('value', callback)

    output_file('Templates/bar_chart.html')
    #output_file('bar_chart.html')

    title = Div(text = """<h1>Prediction of Covid-19 Cases and Availability of Resources</h1>""", width=1200, height=50)

    div1 = Div(text = """<h3>Overview</h3>
        In 2020, the coronavirus became a global pandemic, affecting millions of people around the world. As a result, many hospitals have been collecting data as new patients come in to aid research into its spread and overall trajectory.  Our model takes in data from various datasets and resources and compiles it to make a prediction about the number of cases in each state for a given day, depending on outbreak data from previous days. Furthermore, visualization of hospital data for each state such as number of beds and ventilators for selected states will allow us to better predict when shortages of personal protective equipment (PPE) and resources in hospitals may occur.
        <h3> Additional Resources</h3>
        <a href = "https://www.cdc.gov/coronavirus/2019-ncov/covid-data/covidview/index.html" target="_blank"> CDC Website</a> with information about treatment and symptoms <br>
        <a href = "https://covid19.healthdata.org/united-states-of-america" target="_blank"> University of Washington Model</a> with prediction on Covid-19 Cases<br>
        <a href = "https://docs.google.com/spreadsheets/d/1ir6MK_WFQwnuboa5sKVWtliHktkKOWDw3rUH7aiYTXU/edit?usp=sharing" target="_blank"> Google Sheets</a> with more information on state resources<br>
        """,
        width = 300, height = 100)

    side = column(menu,div1)

    layout = gridplot([title, None, p, side, p_rr,None], ncols = 2)

    curdoc().add_root(layout)
    save(layout, filename = 'Templates/bar_chart.html', title = 'Covid-19 Outbreak Prediction')
    #save(layout, filename = 'bar_chart.html', title = 'Covid-19 Outbreak Prediction')

#make_char()