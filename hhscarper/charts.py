from math import pi

import pandas as pd
from bokeh.embed import components
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum


def get_figure(data, title=''):
    keyword_data = data

    data = pd.Series(keyword_data).reset_index(name='value').rename(columns={'index': 'keyword'})  # noqa: E501

    data['angle'] = (data['value'] / data['value'].sum()) * 2 * pi
    data['color'] = Category20c[len(keyword_data)]

    plot = figure(
        plot_height=400,
        plot_width=600,
        title=title,
        toolbar_location='below',
        tools='hover,save',
        tooltips='@keyword: @value',
        x_range=(-0.5, 1.0),
    )

    plot.wedge(
        x=0,
        y=1,
        radius=0.4,
        start_angle=cumsum('angle', include_zero=True),
        end_angle=cumsum('angle'),
        line_color='white',
        fill_color='color',
        legend_field='keyword',
        source=data,
    )

    plot.axis.axis_label = None
    plot.axis.visible = False
    plot.grid.grid_line_color = None
    plot.toolbar.logo = None

    return components(plot)
