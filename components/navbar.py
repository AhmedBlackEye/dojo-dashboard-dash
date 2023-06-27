from dash import html, dcc


def navbar(pages):
    return html.Div(
        className="navbar bg-base-100 max-w-screen-xl my-8 rounded-lg",
        children=[
            html.Div(
                className="flex-1",
                children=[
                    html.A(
                        className="btn btn-ghost normal-case md:text-4xl font-sans font-bold",
                        children="Dojo",
                    )
                ],
            ),
            html.Div(
                className="flex-none",
                children=[
                    html.Ul(
                        className="menu menu-horizontal px-1",
                        children=[
                            *[
                                html.Li(
                                    dcc.Link(page["name"], href=page["relative_path"])
                                )
                                for page in pages
                            ],
                        ],
                    )
                ],
            ),
        ],
    )
