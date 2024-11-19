import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import requests

# Fetch real-time COVID-19 data
def fetch_data():
    try:
        
        url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
        data = pd.read_csv(url)
        print("Data fetched successfully.")
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Prepare data for visualization
def prepare_data(data):
    data['date'] = pd.to_datetime(data['date'])
    data = data[['location', 'date', 'total_cases', 'new_cases', 'total_vaccinations', 'new_vaccinations', 'population']]
    return data

# Fetch and prepare data
covid_data = fetch_data()
if covid_data is not None:
    covid_data = prepare_data(covid_data)


app = dash.Dash(__name__)
app.title = "COVID-19 Data Dashboard"

# Layout of the dashboard
app.layout = html.Div([
    html.H1("COVID-19 Data Analysis Dashboard", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Select Country:"),
        dcc.Dropdown(
            id='country-dropdown',
            options=[
                {'label': country, 'value': country}
                for country in sorted(covid_data['location'].unique())
            ],
            value='World',
            multi=False,
            placeholder="Select a country",
        ),
    ], style={'width': '50%', 'margin': '0 auto'}),
    dcc.Graph(id='cases-trend'),
    dcc.Graph(id='vaccination-trend'),
])

# Callbacks for interactivity
@app.callback(
    [Output('cases-trend', 'figure'),
     Output('vaccination-trend', 'figure')],
    [Input('country-dropdown', 'value')]
)
def update_dashboard(selected_country):
    filtered_data = covid_data[covid_data['location'] == selected_country]

    # Daily Cases Trend
    fig_cases = px.line(
        filtered_data,
        x='date',
        y='new_cases',
        title=f"Daily New Cases in {selected_country}",
        labels={'new_cases': 'New Cases', 'date': 'Date'}
    )
    fig_cases.update_traces(mode='lines+markers')

    # Vaccination Trend
    fig_vaccinations = px.line(
        filtered_data,
        x='date',
        y='new_vaccinations',
        title=f"Daily New Vaccinations in {selected_country}",
        labels={'new_vaccinations': 'New Vaccinations', 'date': 'Date'}
    )
    fig_vaccinations.update_traces(mode='lines+markers')

    return fig_cases, fig_vaccinations

if __name__ == '__main__':
    app.run_server(debug=True)
