from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import TextInput, Button, Select
from bokeh.layouts import row, column, widgetbox
from bokeh.io import curdoc

from functools import partial, lru_cache
from larana.lar_data import LarData
import numpy as np


#@lru_cache(maxsize=100)
def get_plane_idx(data, plane_id):
    if plane_id < 0 or plane_id > 2:
        raise ValueError("plane must be 0,1 or 2, it was {}".format(plane_id))
    return np.where(data == plane_id)


def get_tick(data, eventid, plane):
    hit = data.get_hits(eventid)
    return hit.tick[get_plane_idx(hit.plane, plane)]


def get_wire(data, eventid, plane):
    hit = data.get_hits(eventid)
    return hit.wire[get_plane_idx(hit.plane, plane)]


def get_ampl(data, eventid, plane):
    hit = data.get_hits(eventid)
    return hit.peak_amp[get_plane_idx(hit.plane, plane)]


def get_width(data, eventid, plane):
    hit = data.get_hits(eventid)
    start_tick = hit.start_tick[get_plane_idx(hit.plane, plane)]
    end_tick = hit.end_tick[get_plane_idx(hit.plane, plane)]

    return end_tick - start_tick


def get_histo(data, plane, bins=200):
    ranges = {0: [-2000,0],
              1: [0, 2000],
              2: [0, 2000]}

    return np.histogram(data, bins=bins, range=ranges[plane])


def get_data_hits(data, event):
    planes = {0: 'u', 1: 'v', 2: 'y'}

    wires = {str_plane: get_wire(data, event, plane) for plane, str_plane in planes.items()}
    ticks = {str_plane: get_tick(data, event, plane) for plane, str_plane in planes.items()}
    peaks = {str_plane: get_ampl(data, event, plane) for plane, str_plane in planes.items()}
    widths = {str_plane: get_width(data, event, plane) for plane, str_plane in planes.items()}

    hit_static = {plane: ColumnDataSource(data=dict(wire=wires[plane],
                                                    tick=ticks[plane],
                                                    peaks=peaks[plane],
                                                    width=widths[plane]
                                                    )
                                                 )
                         for plane in planes.values()}

    hit_selection = {plane: ColumnDataSource(data=dict(wire=[], tick=[])) for plane in planes.values()}

    return hit_static, hit_selection


def get_data_histo(selection):
    planes = {0: 'u', 1: 'v', 2: 'y'}

    dt = {plane: hit_source_static[plane].data[selection] for plane in planes.values()}

    histos = {str_plane: get_histo(dt[str_plane], plane) for plane, str_plane in planes.items()}

    histo_static = {plane: ColumnDataSource(data=dict(hist=hist, edge_left=edges[:-1], edge_right=edges[1:])) for
                   plane, [hist, edges] in histos.items()}

    histo_selection = {plane: ColumnDataSource(data=dict(hist=hist, edge_left=edges[:-1], edge_right=edges[1:]))
                             for plane, [hist, edges] in histos.items()}

    return histo_static, histo_selection


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
    hit_static, hit_selection = get_data_hits(data, evt)
    for plane, source in hit_source_static.items():
        source.data.update(hit_static[plane].data)

    # histo update
    hist, hist_selection = get_data_histo('peaks')
    for [plane_static, source_static], [plane_sel, source_sel] in zip(hist_source.items(), hist_source_selection.items()):
        source_static.data.update(hist[plane_static].data)
        source_sel.data.update(hist_selection[plane_sel].data)


def selection_change(attr, old, new):
    max_idx = np.max(hist_source_selection['y'].selected['1d']['indices'])
    min_idx = np.min(hist_source_selection['y'].selected['1d']['indices'])

    bin_max = hist_source_selection['y'].data['edge_left'][max_idx]
    bin_min = hist_source_selection['y'].data['edge_left'][min_idx]

    print(bin_max, bin_min)

    peak = hit_source_static['y'].data['peak']

    idx = np.where((peak < bin_max) & (peak > bin_min))
    select_hits = dict(wire=hit_source_static['y'].data['wire'][idx], tick=hit_source_static['y'].data['tick'][idx])
    hits_sel.data_source.data = select_hits


# Initilaization
base_dir = "/home/data/uboone/laser/7267/out/roi/"
filename = "LaserReco-LaserHit-7267-0789_digitfilter-exp-roi.root"

data = LarData(base_dir + filename)
data.read_ids()
data.read_hits(planes="u")

# plots and controls
planes = {0: 'u', 1: 'v', 2: 'y'}

plot_hits = {plane: figure(title='{}-plane hits'.format(plane), plot_width=1200, plot_height=300,
                           x_range=[0, 3460], y_range=[3200, 7000]
                           )
             for plane in planes.values()}

plot_hists = {plane: figure(title="{}-plane histo".format(plane),
                            plot_width=300, plot_height=300,
                            tools='pan,wheel_zoom,xbox_select,reset'
                            )
              for plane in planes.values()}

# controls
event_select = TextInput(value='1')
back_btn = Button(label='<')
fwrd_btn = Button(label='>')
hist_select = Select(value='Amplitude', options=['Amplitude', 'Width', 'Area'])

# definitions / data
event = 1
hit_source_static, hit_source_selection = get_data_hits(data, event)
hist_source, hist_source_selection = get_data_histo('peaks')

# histogram plot
plot_hists['y'].quad(top='hist', source=hist_source['y'], bottom=0,
               left='edge_left', right='edge_right',
               fill_color="#036564", line_color="#033649",
               )
hist_bkgnd = plot_hists['y'].circle('edge_left', 'hist',
                              selection_color="orange",
                              source=hist_source_selection['y'],
                              fill_color=None,
                              line_alpha=0)

hits, hits_sel = {}, {}
histos, histos_sel = {}, {}
# actual plotting
for plane in planes.values():
    # hits
    hits[plane] = plot_hits[plane].circle('wire', 'tick', source=hit_source_static[plane], fill_alpha=0.2)
    hits_sel[plane] = plot_hits[plane].cross('wire', 'tick', source=hit_source_selection[plane], color="orange", size=20)

    # histograms
    histos[plane] = plot_hists[plane].quad(top='hist', source=hist_source[plane], bottom=0,
                                           left='edge_left', right='edge_right',
                                           fill_color="#036564", line_color="#033649",
                                           )

    histos_sel[plane] = plot_hists[plane].circle('edge_left', 'hist',
                                                 selection_color="orange",
                                                 source=hist_source_selection[plane],
                                                 fill_color=None,
                                                 line_alpha=0)

# structure
uplots = row(plot_hits['u'], plot_hists['u'])
vplots = row(plot_hits['v'], plot_hists['v'])
yplots = row(plot_hits['y'], plot_hists['y'])
cntrl = widgetbox(back_btn, event_select, fwrd_btn, hist_select)
main_col = column(row(cntrl), uplots, vplots, yplots)

# callbacks
event_select.on_change('value', update_plots)
back_btn.on_click(partial(update_plots, attr='<', old='', new=''))
fwrd_btn.on_click(partial(update_plots, attr='>', old='', new=''))

hist_source_selection['y'].on_change('selected', selection_change)

curdoc().add_root(main_col)
curdoc().title = "Sliders"