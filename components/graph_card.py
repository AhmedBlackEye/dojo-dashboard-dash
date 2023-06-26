from dash import html, dcc, Input, Output, State


def graph_card(title, content, fig):
    return html.Div(
        className="card lg:card-side bg-base-100 shadow-xl",
        children=[
            dcc.Graph(
                figure=fig,
                className="rounded-l-lg h-[30rem] overflow-x sm:h-[15rem] sm:w-[30rem] lg:w-[40rem] lg:h-[20rem] xl:w-[50rem] xl:h-[25rem]",
            ),
            html.Div(
                className="card-body flex flex-col items-center justify-center",
                children=[
                    html.H2(className="card-title", children=title),
                    html.P(className="max-w-prose", children=content),
                ],
            ),
        ],
    )
