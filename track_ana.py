from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import TextInput, Button
from bokeh.layouts import row, column, widgetbox
from bokeh.io import curdoc

from functools import partial
from larana.lar_data import LarData
import numpy as np


def get_tick(data, eventid, plane):
    if plane < 0 or plane > 2:
        raise ValueError("plane must be 0,1 or 2, it was {}".format(plane))

    hit = data.get_hits(eventid)
    hit_idx = np.where(hit.plane == plane)
    return hit.tick[hit_idx]


def get_wire(data, eventid, plane):
    if plane < 0 or plane > 2:
        raise ValueError("plane must be 0,1 or 2, it was {}".format(plane))

    hit = data.get_hits(eventid)
    hit_idx = np.where(hit.plane == plane)
    return hit.wire[hit_idx]


def get_ampl(data, eventid, plane):
    if plane < 0 or plane > 2:
        raise ValueError("plane must be 0,1 or 2, it was {}".format(plane))

    hit = data.get_hits(eventid)
    hit_idx = np.where(hit.plane == plane)
    return hit.peak_amp[hit_idx]


def get_histo(data, plane, bins=200):
    ranges = {0: [-2000,0],
              1: [0, 2000],
              2: [0, 2000]}

    return np.histogram(data, bins=bins, range=ranges[plane])


def update_plots(attr, old, new):
    if attr == '<':
        evt = int(event_select.value) - 1
        event_select.value = str(evt)
        plane = 2
    if attr == '>':
        evt = int(event_select.value) + 1
        event_select.value = str(evt)
        plane = 2
    else:
        evt = int(event_select.value)
        plane = 2

    # hit update
    wire = get_wire(data, evt, plane)
    tick = get_tick(data, evt, plane)
    hit_source.data = dict(wire=wire, tick=tick)

    # hist update
    peak = get_ampl(data, evt, plane)
    hist, edges = get_histo(peak, plane=plane)
    hist_source.data = dict(hist=hist, edge_left=edges[:-1], edge_right=edges[1:])


base_dir = "/home/data/uboone/laser/7267/out/roi/"
filename = "LaserReco-LaserHit-7267-0789_digitfilter-exp-roi.root"
data = LarData(base_dir + filename)
data.read_ids()
data.read_hits(planes="u")

plt_hits = figure(title='hits', plot_width=1200, plot_height=300, x_range=[0, 3460], y_range=[0, 9600])
plt_hist = figure(title="histo", plot_width=300, plot_height=300)
event_select = TextInput(value='1')
back_btn = Button(label='<')
fwrd_btn = Button(label='>')

# definitions / data
event = 1
plane = 2
wire = get_wire(data, event, plane)
tick = get_tick(data, event, plane)

peak = get_ampl(data, event, plane)
hist, edges = get_histo(peak, plane=plane)

hit_source = ColumnDataSource(data=dict(wire=wire, tick=tick))
hist_source = ColumnDataSource(data=dict(hist=hist, edge_left=edges[:-1], edge_right=edges[1:]))

# histogram plot
plt_hist.quad(top='hist', source=hist_source, bottom=0,
              left='edge_left', right='edge_right',
              fill_color="#036564", line_color="#033649",
              )

# hit plot
plt_hits.circle('wire', 'tick', source=hit_source)


plots = row(plt_hits, plt_hist)
cntrl = widgetbox(back_btn, event_select, fwrd_btn)
main_col = column(row(cntrl), plots)

# callbacks
event_select.on_change('value', update_plots)
back_btn.on_click(partial(update_plots, attr='<', old='', new=''))
fwrd_btn.on_click(partial(update_plots, attr='>', old='', new=''))
hist_source

curdoc().add_root(main_col)
curdoc().title = "Sliders"