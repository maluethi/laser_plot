from larana.laser_sim import *
import matplotlib.pyplot as plt
from larana.lar_utils import make_figure, plot_endpoints
from larana.laser_sim import Laser, LASER_POS, convert_to_uboone
import csv

def plot_edges(axes, start, end, kwargs=None):
    if kwargs is None:
        axes[0].plot([start[2], end[2]], [start[0], end[0]], '-*')
        axes[1].plot([start[2], end[2]], [start[1], end[1]], '-*')
        axes[2].plot([start[0], end[0]], [start[1], end[1]], '-*')
    else:
        axes[0].plot([start[2], end[2]], [start[0], end[0]], **kwargs)
        axes[1].plot([start[2], end[2]], [start[1], end[1]], **kwargs)
        axes[2].plot([start[0], end[0]], [start[1], end[1]], **kwargs)

basedir = "/home/matthias/workspace/larana/projects/out/"

sim_file = "input.txt"
lasr_file = "Run-1.txt"

scale = 20

fig, axes, = make_figure()

with open(basedir + sim_file) as f_sim, open(basedir + lasr_file) as f_las:
    lasr_reader = csv.reader(f_las, delimiter=' ')
    for line in lasr_reader:
        laser_id = int(line[0])
        lsr = Laser(laser_id)

        azimu = lsr.azimu_raw2laser(float(line[2]))
        polar = lsr.polar_tick2laser(float(line[3]))
        direc = convert_to_uboone(azimu, polar, 1.0, laser_id)

        start = LASER_POS[laser_id]
        end = [s + 1000 * m for s, m in zip(start, direc)]

        plot_edges(axes, start, end, kwargs={"alpha": 0.1, "color": "green"})

    sim_reader = csv.reader(f_sim, delimiter=' ')
    for line in sim_reader:
        if len(line) > 2:
            start = [float(line[12 + idx]) for idx in range(3)]
            momen = [float(line[7 + idx]) for idx in range(3)]
            end = [s + scale * m for s, m in zip(start, momen)]

            plot_edges(axes, start, end, kwargs={"linestyle": "--", "color": "black"})

plt.show()
