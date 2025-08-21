import requests
import pandas as pd
import dash
from dash import dcc, html, Input, Output, State, no_update
import plotly.express as px
from datetime import datetime

# ---------------------------------------------
# CONFIG
# ---------------------------------------------
API_KEY = "6ef5b587ee904859b14635135f9201da"  
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# ---------------------------------------------
# FUNCTIONS
# ---------------------------------------------
def get_current_weather(city: str):
    """Fetch current weather snapshot for a city. Returns None if invalid."""
    try:
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        r = requests.get(BASE_URL, params=params).json()
        if r.get("cod") != 200:
            return None
    except Exception:
        return None

    return {
        "City": r.get("name", city),
        "Temperature (°C)": r["main"]["temp"],
        "Humidity (%)": r["main"]["humidity"],
        "Wind Speed (km/h)": round(r["wind"]["speed"] * 3.6, 1),
        "Condition": r["weather"][0]["description"].capitalize(),
        "Updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

def get_forecast(city: str) -> pd.DataFrame:
    """Fetch 5-day forecast (3h steps) for a city."""
    try:
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        r = requests.get(FORECAST_URL, params=params).json()
        if r.get("cod") != "200":
            return pd.DataFrame()
    except Exception:
        return pd.DataFrame()

    return pd.DataFrame([
        {
            "Date": datetime.fromtimestamp(entry["dt"]),
            "Temperature (°C)": entry["main"]["temp"],
            "Humidity (%)": entry["main"]["humidity"],
            "Wind Speed (km/h)": round(entry["wind"]["speed"] * 3.6, 1),
            "Condition": entry["weather"][0]["description"].capitalize()
        }
        for entry in r.get("list", [])
    ])

# ---------------------------------------------
# Initialize Dash app
# ---------------------------------------------
app = dash.Dash(__name__)
app.title = "Weather Dashboard"

# ---------------------------------------------
# Layout
# ---------------------------------------------
app.layout = html.Div([
    html.H1("🌤️ Real-time Weather Data Visualizer", style={"textAlign": "center"}),

    html.Div([
        dcc.Dropdown(
            id="city-dropdown",
            options=[{"label": c, "value": c} for c in ["Patna", "Delhi"]],
            value=["Patna", "Delhi"],
            multi=True,
            searchable=True,
            placeholder="🔎 Type a city and press Enter…"
        )
    ], style={"width": "70%", "margin": "auto"}),

    html.Div([
        dcc.RadioItems(
            id='theme-toggle',
            options=[
                {'label': '☀️ Light', 'value': 'plotly'},
                {'label': '🌙 Dark', 'value': 'plotly_dark'}
            ],
            value='plotly',
            labelStyle={'display': 'inline-block', 'marginRight': '10px'}
        )
    ], style={'textAlign': 'center', 'marginTop': '10px'}),

    dcc.Interval(id="interval", interval=15*60*1000, n_intervals=0),

    html.Div(id="city-cards", 
             style={"display": "flex", "flexWrap": "wrap", "gap": "20px",
                    "marginTop": "20px", "justifyContent": "center"}),

    dcc.Graph(id="temp-line-chart"),
    dcc.Graph(id="humidity-bar-chart"),
    dcc.Graph(id="wind-line-chart"),

    html.Div(id="condition-pies",
             style={"display": "flex", "flexWrap": "wrap", "justifyContent": "center", "gap": "20px"})
])

# ---------------------------------------------
# Callback: update dashboard
# ---------------------------------------------
@app.callback(
    [
        Output("city-cards", "children"),
        Output("temp-line-chart", "figure"),
        Output("humidity-bar-chart", "figure"),
        Output("wind-line-chart", "figure"),
        Output("condition-pies", "children"),
        Output("city-dropdown", "options"),
        Output("city-dropdown", "value"),
    ],
    [
        Input("city-dropdown", "value"),
        Input("interval", "n_intervals"),
        Input("theme-toggle", "value"),
        Input("city-dropdown", "search_value"),
    ],
    [State("city-dropdown", "options")]
)
def update_dashboard(cities, _n, theme, search_value, current_options):
    cities = list(cities or [])
    options = list(current_options or [])
    added_city = False

    if search_value and search_value.strip():
        candidate = search_value.strip()
        if candidate.lower() not in [c.lower() for c in cities]:
            w = get_current_weather(candidate)
            if w:
                canonical = w["City"]
                cities.append(canonical)
                if not any(o["value"].lower() == canonical.lower() for o in options):
                    options.append({"label": canonical, "value": canonical})
                added_city = True

    temp_data, hum_data, wind_data, pie_charts, cards = [], [], [], [], []

    for city in cities:
        w = get_current_weather(city)
        if w:
            cards.append(html.Div([
                html.H4(w['City']),
                html.P(f"🌡 {w['Temperature (°C)']} °C"),
                html.P(f"💧 {w['Humidity (%)']} %"),
                html.P(f"💨 {w['Wind Speed (km/h)']} km/h"),
                html.P(f"☁️ {w['Condition']}"),
                html.P(f"⏰ Updated: {w['Updated']}")
            ], style={"border": "1px solid #ccc", "borderRadius": "8px",
                      "padding": "10px", "width": "200px", "textAlign": "center",
                      "backgroundColor": "#f9f9f9"}))

        forecast = get_forecast(city)
        if not forecast.empty:
            forecast["City"] = w["City"] if w else city
            temp_data.append(forecast[["Date", "Temperature (°C)", "City"]])
            hum_data.append(forecast[["Date", "Humidity (%)", "City"]])
            wind_data.append(forecast[["Date", "Wind Speed (km/h)", "City"]])

            condition_counts = forecast["Condition"].value_counts().reset_index()
            condition_counts.columns = ["Condition", "Count"]
            pie_fig = px.pie(
                condition_counts, names="Condition", values="Count",
                title=f"{forecast['City'].iloc[0]} - Condition Distribution", template=theme
            )
            pie_charts.append(html.Div([dcc.Graph(figure=pie_fig, style={"width": "400px", "height": "400px"})]))

    temp_fig = px.line(title="No Temperature Data") if not temp_data else px.line(
        pd.concat(temp_data), x="Date", y="Temperature (°C)", color="City",
        title="🌡 Temperature Forecast Comparison", template=theme
    )
    hum_fig = px.bar(title="No Humidity Data") if not hum_data else px.bar(
        pd.concat(hum_data), x="Date", y="Humidity (%)", color="City", barmode="group",
        title="💧 Humidity Forecast Comparison", template=theme
    )
    wind_fig = px.line(title="No Wind Data") if not wind_data else px.line(
        pd.concat(wind_data), x="Date", y="Wind Speed (km/h)", color="City",
        title="💨 Wind Speed Forecast Comparison", template=theme
    )

    return cards, temp_fig, hum_fig, wind_fig, pie_charts, (options if added_city else no_update), (cities if added_city else no_update)

# ---------------------------------------------
# Run server
# ---------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)