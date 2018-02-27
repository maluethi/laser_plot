
import numpy as np
import larana.lar_utils as laru
from larana.lar_utils import TPC_LIMITS

from mayavi import mlab


input_filename = '/home/matthias/workspace/my_fieldcorr/output/RecoDispl-exp-roii.root'
input_filename = '/home/matthias/workspace/FieldCalibration/output/RecoCorrection-Sim_same.root'

# check this for more fun:
# http://docs.enthought.com/mayavi/mayavi/mlab.html#d-plotting-functions-for-numpy-arrays

dist_raw = laru.get_histos(input_filename)
distortion = laru.make_array(dist_raw).T.view(np.recarray)

x, y, z = np.meshgrid(np.linspace(laru.TPC.x_min, laru.TPC.x_max, distortion.shape[0]),
                      np.linspace(laru.TPC.y_min, laru.TPC.y_max, distortion.shape[1]),
                      np.linspace(laru.TPC.z_min, laru.TPC.z_max, distortion.shape[2]))
print( np.linspace(laru.TPC.z_min, laru.TPC.z_max, distortion.shape[2]))

distortion = laru.filter_max(distortion)
src = mlab.pipeline.vector_field(distortion.dx, distortion.dy, distortion.dz)

mlab.pipeline.vectors(src, mask_points=20, scale_factor=3.)
#flow = mlab.flow(distortion.dx, distortion.dy, distortion.dz, seed_scale=0.2,
#                          seed_resolution=10,
#                          integration_direction='both')

#mlab.outline(extent=[minmax[0] for minmax in TPC_LIMITS] + [minmax[1] for minmax in TPC_LIMITS])
#mlab.pipeline.vector_cut_plane(src, mask_points=3, scale_factor=3)
mlab.show()

#mlab.pipeline.vectors(src, mask_points=20, scale_factor=3.)