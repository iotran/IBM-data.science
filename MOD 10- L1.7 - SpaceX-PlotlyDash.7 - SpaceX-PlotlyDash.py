from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os

# Change to the directory where your CSV file is located
os.chdir("C:\\Users\\iotra\\OneDrive\\Desktop\\Coursera\\IBM -  Python Stuff")


# Confirm the change by checking the current working directory
print("Current Working Directory:", os.getcwd())

# Assuming 'spacex_df' is already loaded with your data
spacex_df = pd.read_csv('spacex_launch_data.csv')  # replace with your file path if needed
launch_sites = spacex_df['Launch Site'].unique()


############################# TASK1 - DROPDOWN MENU #############################

#TASK 1 - Define the dropdown options, with all sites option: 

dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}] + \
    [{'label': site, 'value': site} for site in launch_sites]
    
# Create a dash application
app = Dash(__name__)

# Create an app layout

app.layout = html.Div([
    dcc.Dropdown(
        id='site-dropdown',
        options=dropdown_options,
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    dcc.RangeSlider( #task3
        id='Payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: f'{i} kg' for i in range(0, 10001, 1000)},
        value=[0,10000]#full range
    ),    
    dcc.Graph(id='success-pie-chart'),# task2 pie chart
    dcc.Graph(id='success-payload-scatter-chart')# task4 scatter chart
])

############################# TASK2/3 - CALLBACK MENU #############################

# Callback function for pie chart
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='Payload-slider', component_property='value')])

def get_pie_chart(entered_site, payload_range):
    # Filter data based on selected launch site and payload range
    filtered_data = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    if entered_site == 'ALL':
        data = filtered_data.groupby(['class']).size().reset_index(name='counts')
        fig = px.pie(data, values='counts', names='class', title='Success vs. Failure Rate for All Sites')
        
    else:
        #filter for selected site: 
        site_df = filtered_data[filtered_data['Launch Site'] == entered_site]
        data = site_df.groupby(['class']).size().reset_index(name='counts')
        fig = px.pie(data, values='counts', names='class', title='Success vs. Failure Rate for Site: '+ entered_site)
        
    return fig

# TASK4 -- Callback function for scatter plot based on site and payload range

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='Payload-slider', component_property='value')]
)
def get_scatter_plot(entered_site, payload_range):
    # Filter data based on selected payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    if entered_site == 'ALL':
        # Scatter plot for all sites
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                         color='Booster Version', 
                         title='Payload vs. Outcome for All Sites')
    else:
        # Scatter plot for selected site
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(site_df, x='Payload Mass (kg)', y='class', 
                         color='Booster Version', 
                         title=f'Payload vs. Outcome for {entered_site}')
    
    return fig




if __name__ == '__main__':
    app.run_server(debug=True)