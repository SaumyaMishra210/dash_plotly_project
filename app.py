import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

# Sample datasets
datasets = {
    "Fruits": ["Apples", "Bananas", "Cherries", "Dates","Pineapple"],
    "Countries": ["USA", "Canada", "Mexico", "Brazil"],
    "Products": ["Laptops", "Tablets", "Smartphones", "Desktops"]
}

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dynamic Bar Chart Generator", style={'textAlign': 'center'}),
    
    html.Label("Select Dataset:"),
    dcc.Dropdown(
        id='dataset-dropdown',
        options=[{'label': key, 'value': key} for key in datasets.keys()],
        value='Fruits'
    ),
    
    html.Label(id='values-hint', style={'font-weight': 'bold', 'margin-top': '10px'}),
    
    dcc.Input(id='values-input', type='text', value='', style={'width': '100%'}),
    
    html.Button("Submit", id='submit-button', n_clicks=0),
    
    dcc.Graph(id='bar-chart')
])

@app.callback(
    Output('values-hint', 'children'),
    Input('dataset-dropdown', 'value')
)
def update_hint(dataset):
    num_categories = len(datasets[dataset])
    return f"Enter {num_categories} numerical values, separated by commas."

@app.callback(
    Output('bar-chart', 'figure'),
    Input('submit-button', 'n_clicks'),
    State('dataset-dropdown', 'value'),
    State('values-input', 'value')
)
def update_chart(n_clicks, dataset, values):
    if not dataset or not values:
        return px.bar(title="Please enter valid data.")
    
    try:
        values_list = [float(v.strip()) for v in values.split(',')]
        categories = datasets[dataset]
        
        if len(values_list) != len(categories):
            return px.bar(title="Number of values must match number of categories.")
        
        df = pd.DataFrame({"Category": categories, "Value": values_list})
        fig = px.bar(df, x="Category", y="Value", title=f"Bar Chart for {dataset}")
        return fig
    except ValueError:
        return px.bar(title="Please enter numerical values only.")

if __name__ == '__main__':
    app.run_server(debug=True)