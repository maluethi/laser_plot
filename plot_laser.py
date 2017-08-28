from larana.lar_utils import read_laser, disassemble_laser, make_figure, plot_edges
import matplotlib.pyplot as plt

fig, axes = make_figure()

basedir = "/home/data/uboone/laser/sim/"
filename = basedir + "Tracks-Sim.root"
laser_data = read_laser(filename)

for evt in range(len(laser_data)):
    laser_entry, laser_exit, laser_dir, laser_pos = disassemble_laser(laser_data[evt])

    entry = laser_entry.tolist()
    exit = laser_exit.tolist()
    plot_edges(axes, entry, exit)

plt.show()