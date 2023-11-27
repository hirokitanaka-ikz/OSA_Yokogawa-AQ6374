import numpy as np
import pyvisa
import re


class OSAController():

    def __init__(self) -> None:
        
        self.connect()
        self.reset()
        self.set_command_type('AQ6374')
    
    def connect(self):
        rm = pyvisa.ResourceManager()
        gpib = rm.list_resources()
        self.instrument = rm.open_resource(gpib[0])
    
    def reset(self):
        self.instrument.write('*RST')
    
    def set_command_type(self, command_type):
        if command_type in ('AQ6317', 'AQ6374'):
            self.instrument.write(f':SYSTEM:COMMUNICATE:CFORMAT {command_type}')
        else:
            print('UNKNOWN COMMAND!')

    def set_sensitivity(self, sensitivity):
        self.instrument.write(f':SENSE:SENSE {sensitivity}')
    
    def set_resolution(self, resolution_nm):
        self.instrument.write(f':SENSE:BANDWIDTH:RESOLUTION {resolution_nm}NM')

    def set_wavelenth_center(self, wavelength_center_nm):
        self.instrument.write(f':SENSE:WAVELENGTH:CENTER {wavelength_center_nm}NM')
    
    def set_wavelength_span(self, wavelength_span_nm):
        self.instrument.write(f':SENSE:WAVELENGTH:SPAN {wavelength_span_nm}NM')

    def set_wavelength_start(self, wavelength_start_nm):
        self.instrument.write(f':SENSE:WAVELENGTH:START {wavelength_start_nm}NM')
    
    def set_wavelength_stop(self, wavelength_stop_nm):
        self.instrument.write(f':SENSE:WAVELENGTH:STOP {wavelength_stop_nm}NM')
    
    def set_sampling_step(self, sampling_step_nm):
        self.instrument.write(f':SENSE:SWEEP:STEP {sampling_step_nm}NM')
    
    def set_auto_sampling(self, ONorOFF):
        self.instrument.write(f':SENSE:SWEEP:POINTS:AUTO {ONorOFF}')
    
    def set_fiber_core_size(self, SMALLorLARGE):
        self.instrument.write(f':SENSE:SETTING:FIBER {SMALLorLARGE}')

    def set_active_trace(self, trace):
        self.instrument.write(f':TRACE:ACTIVE {trace}')
    
    def set_scale(self, scale):
        self.instrument.write(f':DISPLAY:TRACE:Y1:SPACING {scale}')
    
    def set_auto_ref_level(self, ONorOFF):
        self.instrument.write(f':CALCULATE:MARKER:MAXIMUM:SRLevel:AUTO {ONorOFF}')

    def get_ID(self):
        return self.instrument.query('*IDN?')
    
    def get_sensitivity(self):
        sensitivity = int(self.instrument.query(':SENSE:SENSE?'))
        if sensitivity == 0:
            return 'NHLD'
        elif sensitivity == 1:
            return 'NAUT'
        elif sensitivity == 2:
            return 'MID'
        elif sensitivity == 3:
            return 'HIGH1'
        elif sensitivity == 4:
            return 'HIGH2'
        elif sensitivity == 5:
            return 'HIGH3'
        elif sensitivity == 6:
            return 'NORMAL'
    
    def get_resolution(self):
        return self.instrument.query(':SENSE:BANDWIDTH:RESOLUTION?')

    def get_wavelength_center(self):
        return self.instrument.query(':SENSE:WAVELENGTH:CENTER?')
    
    def get_wavelength_span(self):
        return self.instrument.query(':SENSE:WAVELENGTH:SPAN?')

    def get_wavelength_start(self):
        return self.instrument.query(':SENSE:WAVELENGTH:START?')
    
    def get_wavelength_stop(self):
        return self.instrument.query(':SENSE:WAVELENGTH:STOP?')
    
    def get_sampling_step(self):
        return self.instrument.query(':SENSE:SWEEP:STEP?')
    
    def get_auto_sampling(self):
        ONorOFF = int(self.instrument.query(':SENSE:SWEEP:POINTS:AUTO?'))
        if ONorOFF == 0:
            return 'OFF'
        elif ONorOFF == 1:
            return 'ON'
    
    def get_sampling_points(self):
        return self.instrument.query(':SENSE:SWEEP:POINTS?')
    
    def get_fiber_core_size(self):
        fiber_core_size = int(self.instrument.query(':SENSE:SETTING:FIBER?'))
        if fiber_core_size == 0:
            return 'SMALL'
        elif fiber_core_size == 1:
            return 'LARGE'
    
    def get_active_trace(self):
        return self.instrument.query(':TRACE:ACTIVE?')
    
    def get_scale(self):
        scale = int(self.instrument.query(':DISPLAY:TRACE:Y1:SPACING?'))
        if scale == 0:
            return 'LOGARITHMIC'
        elif scale == 1:
            return 'LINEAR'
    
    def get_Xdata(self, trace):
        xdata_list = self.instrument.query(f'TRACE:X? {trace}').strip().split(',')
        return np.asarray(xdata_list, 'f')
    
    def get_Ydata(self, trace):
        ydata_list = self.instrument.query(f'TRACE:Y? {trace}').strip().split(',')
        return np.asarray(ydata_list, 'f')

    def sweep(self):
        self.instrument.write(':INITIATE')
        status = 0
        while status == 0:
            status = self.instrument.query(':STAT:OPER:EVEN?')
            status = int(re.sub(r'\D', '', status))
        # print('SWEEP FINISH!')