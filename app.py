import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Sample datasets
datasets = {
    "Fruits": ["Apple", "Banana", "Orange"],
    "Vegetables": ["Carrot", "Broccoli", "Spinach"]
}
data_values = {dataset: [10, 15, 20] for dataset in datasets.keys()}

app.layout = dbc.Container([
    html.H1("Dynamic Bar Chart Generator", className="text-center text-primary mt-4"),
    
    dbc.Row([
        dbc.Col([
            html.Label("Select Dataset:", className="fw-bold"),
            dcc.Dropdown(id='dataset-dropdown', 
                         options=[{'label': k, 'value': k} for k in datasets.keys()], 
                         value=list(datasets.keys())[0],
                         className="mb-3"),
        ], width=6)
    ], justify="center"),
    
    dbc.Row([
        dbc.Col([
            html.Label(id='values-hint', className="fw-bold text-info"),
            dcc.Input(id='values-input', type='text', value="", className="form-control mb-3"),
        ], width=6)
    ], justify="center"),
    
    dbc.Row([
        dbc.Col([
            dbc.Button("Update Chart", id='update-button', n_clicks=0, color="primary", className="mb-4")
        ], width=6, className="text-center")
    ], justify="center"),
    
    dbc.Row([
        dbc.Col([
            html.Label("Create New Dataset:", className="fw-bold"),
            dcc.Input(id='new-dataset-name', type='text', placeholder='Dataset Name', className="form-control mb-2"),
            dcc.Input(id='new-dataset-items', type='text', placeholder='Items (comma-separated)', className="form-control mb-3"),
            dbc.Button("Create Dataset", id='create-dataset-button', n_clicks=0, color="success", className="mb-4")
        ], width=6)
    ], justify="center"),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-chart', className="border rounded p-3 shadow")
        ], width=10)
    ], justify="center")
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
    Input('update-button', 'n_clicks'),
    State('dataset-dropdown', 'value'),
    State('values-input', 'value')
)
def update_chart(n_clicks, dataset, values):
    if not dataset or not values:
        return px.bar(title="Please enter valid data.")
    
    try:
        values_list = [float(v.strip()) for v in values.split(',')]
        if len(values_list) != len(datasets[dataset]):
            return px.bar(title="Number of values must match number of categories.")
        
        data_values[dataset] = values_list
        df = pd.DataFrame({"Category": datasets[dataset], "Values": data_values[dataset]})
        return px.bar(df, x='Category', y='Values', title=f"Dataset: {dataset}", color_discrete_sequence=["#007bff"])
    except ValueError:
        return px.bar(title="Please enter numerical values only.")

@app.callback(
    Output('dataset-dropdown', 'options'),
    Output('dataset-dropdown', 'value'),
    Input('create-dataset-button', 'n_clicks'),
    State('new-dataset-name', 'value'),
    State('new-dataset-items', 'value')
)
def create_dataset(n_clicks, name, items):
    if not name or not items:
        return [{'label': k, 'value': k} for k in datasets.keys()], list(datasets.keys())[0]
    
    datasets[name] = items.split(',')
    data_values[name] = [0] * len(datasets[name])
    options = [{'label': k, 'value': k} for k in datasets.keys()]
    return options, name

if __name__ == '__main__':
    app.run_server(debug=True)
