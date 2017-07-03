from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import TextInput, Button, Select
from bokeh.layouts import row, column, widgetbox
from bokeh.io import curdoc

from functools import partial, lru_cache
from larana.lar_data import LarData
import numpy as np


#@lru_cache(maxsize=100)
def get_plane_idx(dt, plane_id):
    if plane_id < 0 or plane_id > 2:
        raise ValueError("plane must be 0,1 or 2, it was {}".format(plane_id))
    return np.where(dt == plane_id)


def get_tick(dt, eventid, plane):
    hit = dt.get_hits(eventid)
    return hit.tick[get_plane_idx(hit.plane, plane)]


def get_wire(dt, eventid, plane):
    hit = dt.get_hits(eventid)
    return hit.wire[get_plane_idx(hit.plane, plane)]


def get_ampl(dt, eventid, plane):
    hit = dt.get_hits(eventid)
    return hit.peak_amp[get_plane_idx(hit.plane, plane)]


def get_width(dt, eventid, plane):
    hit = dt.get_hits(eventid)
    start_tick = hit.start_tick[get_plane_idx(hit.plane, plane)]
    end_tick = hit.end_tick[get_plane_idx(hit.plane, plane)]

    return end_tick - start_tick


def get_histo(dt, plane, dim, bins=200):
    print(plane, dim)
    ranges = {'peaks':  {0: [-2000, 0], 1: [0, 2000], 2: [0, 2000]},
              'width': {0: [0, 500], 1: [0, 500], 2: [0, 500]}
              }

    return np.histogram(dt, bins=bins, range=ranges[dim][plane])


def get_data_hits(dt, event):
    planes = {0: 'u', 1: 'v', 2: 'y'}

    wires = {str_plane: get_wire(dt, event, plane) for plane, str_plane in planes.items()}
    ticks = {str_plane: get_tick(dt, event, plane) for plane, str_plane in planes.items()}
    peaks = {str_plane: get_ampl(dt, event, plane) for plane, str_plane in planes.items()}
    widths = {str_plane: get_width(dt, event, plane) for plane, str_plane in planes.items()}

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
    dim = dimensions[dim_select.value]

    dt = {plane: hit_source_static[plane].data[selection] for plane in planes.values()}
    histos = {str_plane: get_histo(dt[str_plane], plane, dim) for plane, str_plane in planes.items()}
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
    if attr == '>':
        evt = int(event_select.value) + 1
        event_select.value = str(evt)
    else:
        evt = int(event_select.value)

    # histo update
    hist, hist_selection = get_data_histo(dimensions[dim_select.value])
    for [plane_static, source_static], [plane_sel, source_sel] in zip(hist_source.items(), hist_source_selection.items()):
        source_static.data.update(hist[plane_static].data)
        source_sel.data.update(hist_selection[plane_sel].data)

    # hit update
    hit_static, hit_selection = get_data_hits(data, evt)
    for [plane_static, source_static], [plane_sel, source_sel] in zip(hit_source_static.items(), hit_source_selection.items()):
        source_static.data.update(hit_static[plane_static].data)
        source_sel.data.update(hit_selection[plane_sel].data)

        selection_change('', '', '', plane_sel)


def selection_change(attr, old, new, plane):
    try:
        max_idx = np.max(hist_source_selection[plane].selected['1d']['indices'])
        min_idx = np.min(hist_source_selection[plane].selected['1d']['indices'])
    except ValueError:
        bin_max = 0
        bin_min = 0
    else:
        bin_max = hist_source_selection[plane].data['edge_left'][max_idx]
        bin_min = hist_source_selection[plane].data['edge_left'][min_idx]

    print('{}-plane bin selection: {}, {}'.format(plane, bin_min, bin_max))

    hist = hit_source_static[plane].data[dimensions[dim_select.value]]

    idx = np.where((hist < bin_max) & (hist > bin_min))
    select_hits = dict(wire=hit_source_static[plane].data['wire'][idx], tick=hit_source_static[plane].data['tick'][idx])
    hit_source_selection[plane].data.update(select_hits)


def dimension_change(attr, old, new):
    hist, hist_selection = get_data_histo(dimensions[dim_select.value])
    for [plane_static, source_static], [plane_sel, source_sel] \
            in zip(hist_source.items(), hist_source_selection.items()):
        source_static.data.update(hist[plane_static].data)
        source_sel.data.update(hist_selection[plane_sel].data)


# Initilaization
base_dir = "/home/data/uboone/laser/7267/out/roi/"
filename = "LaserReco-LaserHit-7267-0789_digitfilter-exp-roi.root"

data = LarData(base_dir + filename)
data.read_ids()
data.read_hits(planes="u")

dimensions = {"Amplitude": 'peaks',
              "Width": 'width'}

# plots and controls
planes = {0: 'u', 1: 'v', 2: 'y'}
wire_limits = {'u': [0, 2000], "v": [0, 2000], 'y': [0, 3460]}
tick_limits = [3200, 9600]


plot_hits = {plane: figure(title='{}-plane hits'.format(plane), plot_width=1200, plot_height=300,
                           x_range=wire_limits[plane], y_range=tick_limits
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
dim_select = Select(value='Amplitude', options=sorted(dimensions.keys()))

# definitions / data
event = 1
hit_source_static, hit_source_selection = get_data_hits(data, event)
hist_source, hist_source_selection = get_data_histo('peaks')

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
cntrl = [back_btn, event_select, fwrd_btn, dim_select]
main_col = column(row(cntrl), uplots, vplots, yplots)

# callbacks
event_select.on_change('value', update_plots)
back_btn.on_click(partial(update_plots, attr='<', old='', new=''))
fwrd_btn.on_click(partial(update_plots, attr='>', old='', new=''))
dim_select.on_change('value', dimension_change)
for plane in planes.values():
    hist_source_selection[plane].on_change('selected', partial(selection_change, plane=plane))

# output
curdoc().add_root(main_col)
curdoc().title = "Sliders"