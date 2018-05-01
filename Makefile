
thesis = ${THESIS}

all : efield

# Chapter: EField
efield : cross_dist time_histo 

cross_dist: plot_cross_dist.py
	python plot_cross_dist.py -p

time_histo : plot_time_histo_th.py
	python plot_time_histo_th.py -p

install: 
	cp -r ./gfx/ $(thesis)
