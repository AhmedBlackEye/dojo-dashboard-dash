from dash import html, dcc
from millify import millify


def metric(
    title, value, desc, img_name=None, is_num_metric=True, add_sterling_symbol=True
):
    if is_num_metric:
        value = "£ " + millify(value, 2) if add_sterling_symbol else millify(value, 2)
        desc = round(desc, 1)
        if desc == 0:
            stat_desc_element = None
        else:
            color, arrow_direction = (
                ["green", "up_arrow"] if desc > 0 else ["red", "down_arrow"]
            )
            stat_desc_element = html.Div(
                className=f"stat-desc text-{color}-400 font-semibold flex",
                children=[
                    html.Img(className="w-4", src=f"assets/{arrow_direction}.svg"),
                    html.Span(children=f"{desc}%"),
                ],
            )
    else:
        stat_desc_element = stat_desc_element = html.Div(
            className="stat-desc font-semibold",
            children=desc,
        )

    stat_img_element = (
        html.Img(className="stat-figure w-10", src=f"assets/{img_name}.svg")
        if img_name
        else None
    )

    return html.Div(
        className="stat",
        children=[
            stat_img_element,
            html.Div(className="stat-title", children=title),
            html.Div(className="stat-value", children=value),
            stat_desc_element,
        ],
    )
