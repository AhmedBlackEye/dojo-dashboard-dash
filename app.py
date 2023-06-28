from dash import Dash, html
import dash
from components.navbar import navbar

app = Dash(
    __name__,
    external_stylesheets=["https://cdn.jsdelivr.net/npm/daisyui@3.1.6/dist/full.css"],
    external_scripts=["https://cdn.tailwindcss.com"],
    use_pages=True,
)


app.layout = html.Div(
    className="grid place-items-center bg-gray-200 px-2 md:px-4 lg:px-10 font-sans",
    children=[
        navbar(dash.page_registry.values()),
        dash.page_container,
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
