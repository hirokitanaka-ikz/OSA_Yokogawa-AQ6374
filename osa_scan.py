from OSAControllerClass import OSAController
import matplotlib.pyplot as plt
import pandas as pd

ACTIVE_TRACE = 'TRA'
start_wavelength = 1015.0
stop_wavelength = 1025.0
resolution = 0.05
sensitivity = 'MID'

osa_controller = OSAController()
osa_controller.connect()
osa_controller.reset()
osa_controller.set_active_trace(ACTIVE_TRACE)
osa_controller.set_fiber_core_size('SMALL')
osa_controller.set_scale('LINEAR')
osa_controller.set_auto_ref_level('ON')


osa_controller.set_wavelength_start(start_wavelength)
osa_controller.set_wavelength_stop(stop_wavelength)
osa_controller.set_resolution(resolution)
osa_controller.set_auto_sampling('ON')
osa_controller.set_sensitivity(sensitivity)

# osa_controller.sweep()

def get_spectrum():
    wl = osa_controller.get_Xdata(ACTIVE_TRACE)
    intensity = osa_controller.get_Ydata(ACTIVE_TRACE)     
    return wl, intensity

df = pd.DataFrame()

N = 50
for i in range(N):
    osa_controller.sweep()
    wl, intensity = get_spectrum()

    df['wavelength'] = wl
    df[f'scan_{i}'] = intensity
    plt.plot(wl, intensity, lw=0.5)

df.to_csv('2022-11-30/test.txt', sep='\t', index=False)
plt.show()


