from dash import html, dcc


def navbar(pages):
    return html.Div(
        className="navbar bg-base-100 max-w-screen-xl my-8 rounded-lg text-white",
        children=[
            html.Div(
                className="flex-1",
                children=[
                    html.A(
                        className="btn btn-ghost normal-case md:text-4xl font-sans font-bold",
                        children="Dojo",
                        href="https://dojo.tech/",
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
                                    [
                                        dcc.Link(
                                            page["name"], href=page["relative_path"]
                                        )
                                    ],
                                    className="text-md",
                                )
                                for page in pages
                            ],
                        ],
                    )
                ],
            ),
        ],
    )
