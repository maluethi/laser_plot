
thesis = ${THESIS}

all : efield

# Chapter: EField
efield : cross_dist time_histo time_evolution

cross_dist: plot_cross_dist.py
	python plot_cross_dist.py -p

time_histo : plot_time_histo_th.py
	python plot_time_histo_th.py -p

time_evolution : plot_time_evolution.py
	python plot_time_evolution.py -p

# Chapter: LCS-System
lcssystem: aoi

aoi: plot_aoi.py
	python plot_aoi.py -p

install: 
	cp -r ./gfx/ $(thesis)
