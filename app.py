from dash import Dash, html, dcc
import dash

app = Dash(
    __name__,
    external_stylesheets=["https://cdn.jsdelivr.net/npm/daisyui@3.1.6/dist/full.css"],
    # external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"],
    external_scripts=["https://cdn.tailwindcss.com"],
    use_pages=True,
)

app.layout = html.Div(
    className="grid place-items-center bg-gray-200 px-2 md:px-4 lg:px-10",
    children=[
        html.H1("Multi-page app with Dash Pages"),
        html.Div(
            [
                html.Div(
                    dcc.Link(
                        f"{page['name']} - {page['path']}", href=page["relative_path"]
                    )
                )
                for page in dash.page_registry.values()
            ]
        ),
        dash.page_container,
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
