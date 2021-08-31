import logging
from math import pi

import pandas as pd
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from django.utils.translation import gettext as _
from hhscarper.models import Request

logger = logging.getLogger(__name__)


def get_report_figure(data, title=''):
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


def get_dashoard_figure():
    data = {row['date_created']: row['total'] for row in Request.objects.group_by_date()}
    series = pd.Series(data).reset_index(name='total').rename(columns={'index': 'date'})
    source = ColumnDataSource(data={'date': series['date'], 'total': series['total']})

    plot = figure(
        plot_width=1110,
        plot_height=500,
        x_axis_type='datetime',
        tools='save',
    )
    hover = HoverTool(
        tooltips=[(_('Дата'), '@date{%F}'), (_('Запросы'), '@total')],  # noqa: WPS323
        formatters={'@date': 'datetime'},
    )
    plot.add_tools(hover)
    plot.toolbar.logo = None

    plot.line(
        x='date',
        y='total',
        source=source,
        color='red',
        alpha=1,
    )
    return components(plot)
