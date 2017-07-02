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
    print(attr)
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
    peak = get_ampl(data, evt, plane)
    hit_source_static.data = dict(wire=wire, tick=tick, peak=peak)
    hit_source_selection.data = dict(wire=[], tick=[])

    # hist update
    hist, edges = get_histo(peak, plane=plane)
    hist_source.data = dict(hist=hist, edge_left=edges[:-1], edge_right=edges[1:])
    hist_source_selection.data = dict(hist=hist, edge_left=edges[:-1], edge_right=edges[1:])


def selection_change(attr, old, new):
    max_idx = np.max(hist_source_selection.selected['1d']['indices'])
    min_idx = np.min(hist_source_selection.selected['1d']['indices'])

    bin_max = hist_source_selection.data['edge_left'][max_idx]
    bin_min = hist_source_selection.data['edge_left'][min_idx]

    print(bin_max, bin_min)

    peak = hit_source_static.data['peak']

    idx = np.where((peak < bin_max) & (peak > bin_min))
    select_hits = dict(wire=hit_source_static.data['wire'][idx], tick=hit_source_static.data['tick'][idx])
    hits_sel.data_source.data = select_hits


base_dir = "/home/data/uboone/laser/7267/out/roi/"
filename = "LaserReco-LaserHit-7267-0789_digitfilter-exp-roi.root"
data = LarData(base_dir + filename)
data.read_ids()
data.read_hits(planes="u")

plt_hits = figure(title='hits', plot_width=1200, plot_height=300, x_range=[0, 3460], y_range=[3200, 7000])
plt_hist = figure(title="histo", plot_width=300, plot_height=300, tools='pan,wheel_zoom,xbox_select,reset')
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

hit_source_static = ColumnDataSource(data=dict(wire=wire, tick=tick, peak=peak))
hit_source_selection = ColumnDataSource(data=dict(wire=[], tick=[]))

hist_source = ColumnDataSource(data=dict(hist=hist, edge_left=edges[:-1], edge_right=edges[1:]))
hist_source_selection = ColumnDataSource(data=dict(hist=hist, edge_left=edges[:-1], edge_right=edges[1:]))

# histogram plot
plt_hist.quad(top='hist', source=hist_source, bottom=0,
              left='edge_left', right='edge_right',
              fill_color="#036564", line_color="#033649",
              )
hist_bkgnd = plt_hist.circle('edge_left', 'hist',
                selection_color="orange",
                source=hist_source_selection,
                fill_color=None,
                line_alpha=1.)

# hit plot
hits = plt_hits.circle('wire', 'tick', source=hit_source_static, fill_alpha=0.2)
hits_sel = plt_hits.cross('wire', 'tick', source=hit_source_selection, color="orange",size=20)


plots = row(plt_hits, plt_hist)
cntrl = widgetbox(back_btn, event_select, fwrd_btn)
main_col = column(row(cntrl), plots)

# callbacks
event_select.on_change('value', update_plots)
back_btn.on_click(partial(update_plots, attr='<', old='', new=''))
fwrd_btn.on_click(partial(update_plots, attr='>', old='', new=''))

hist_source_selection.on_change('selected', selection_change)

curdoc().add_root(main_col)
curdoc().title = "Sliders"