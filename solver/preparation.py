import inputs as inp
import numpy as np

RPM = np.arange(inp.min_RPM, inp.max_RPM, inp.stepsize_RPM)

true_EVO = 180 - inp.EVO
true_EVC = 360 + inp.EVC
true_IVO = 360 - inp.IVO
true_IVC = 540 + inp.IVC

theta = true_IVO - true_EVO - inp.wave_delay