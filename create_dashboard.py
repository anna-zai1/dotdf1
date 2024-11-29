import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

original_df = pd.read_csv('finaldata.csv')
average_df = pd.read_csv('averagedata.csv')
dotds = pd.read_csv('driver_of_the_day.csv')
rawstartend = pd.read_csv('raw_start_end.csv')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(
    "Is getting Driver Of The Day linked to performance?",
    style={'color': 'black', 'backgroundColor': 'white', 'fontFamily': 'Calibri, sans-serif', 'fontSize': 24}),
    
    dcc.Dropdown(
        id='variable-selector',
        options=[
            {'label': '2023 Drivers of the Day', 'value': '2023 Drivers of the Day'},
            {'label': 'Raw End and Start Position', 'value': 'Raw End and Start Position'},
            {'label': 'Finish Position', 'value': 'End Position'},
            {'label': 'Race Story/Number of places gained', 'value': 'Race Story'},
            {'label': 'Did he get fastest lap?', 'value': 'Did the driver get fastest lap?'},
            {'label': 'Was he a rookie?', 'value': 'Rookie?'},
            {'label': 'Number of Overtakes', 'value': 'Number of Overtakes'},
            {'label': 'Number of times overtaken', 'value': 'Number Overtaken'},
        ],
        value='End Position',
        style={
        'width': '50%',
        'fontFamily': 'Calibri, sans-serif',
        'fontSize': 14,
        'color': 'black',
        'backgroundColor': 'white'
    }
    ),
    
    dcc.Graph(id='graph-container'),
])

@app.callback(
    dash.dependencies.Output('graph-container', 'figure'),
    [dash.dependencies.Input('variable-selector', 'value')]
)
def update_graph(selected_variable):

    fig = go.Figure()

    if selected_variable in ['End Position', 'Race Story', 'Number of Overtakes', 'Number Overtaken']:
        fig = px.scatter(
            original_df, x='Race', y=selected_variable, title=f'{selected_variable} Across Races',
            hover_data=['Driver'], color_discrete_sequence=['red']
        )

        avg_scatter = px.scatter(
            average_df, x='Race', y=f'Average {selected_variable}', title=f'{selected_variable} Across Races (Average)',
            hover_data=['Driver'], color_discrete_sequence=['green']
        )

        line_trace_original = go.Scatter(
            x=original_df['Race'],
            y=original_df[selected_variable],
            mode='lines+markers',
            line=dict(color='red'),
            name='DOTD Data',
            hoverinfo='skip'
        )

        line_trace_average = go.Scatter(
            x=average_df['Race'],
            y=average_df[f'Average {selected_variable}'],
            mode='lines+markers',
            line=dict(color='green'),
            name='Average Data',
            hoverinfo='x+y'
        )

        fig.add_trace(line_trace_original)
        fig.add_trace(line_trace_average)

        fig.update_layout(
        title_text=f'{selected_variable} Across Races',
        xaxis_title='Race',
        yaxis_title=selected_variable,
        font=dict(family="Arial, sans-serif", size=14, color="black"),
        paper_bgcolor='white',  
        plot_bgcolor='light grey',
        legend=dict(title=dict(text='', font=dict(color='black')), font=dict(color='black')),
    )

    elif selected_variable in ['Rookie?', 'Did the driver get fastest lap?']:
        fig = px.pie(original_df, names=selected_variable, title=f'Proportion of {selected_variable}',hole=0.4, labels={'Driver': selected_variable})
    
    elif selected_variable in ['2023 Drivers of the Day']:
        table = ff.create_table(dotds)  
        table.update_layout(
            margin=dict(l=200, r=200, b=200, t=50), 
            font=dict(family="Calibri, sans-serif", size=12, color="black"), 
            title_text='2023 Drivers of the Day',
        )
        fig = go.Figure(data=table)

    elif selected_variable in ['Raw End and Start Position']:
        table = ff.create_table(rawstartend)  
        table.update_layout(
            margin=dict(l=200, r=200, b=200, t=50), 
            font=dict(family="Calibri, sans-serif", size=12, color="black"), 
            title_text='Raw Start and End Position Data',
        )
        fig = go.Figure(data=table)
       

    return fig

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
