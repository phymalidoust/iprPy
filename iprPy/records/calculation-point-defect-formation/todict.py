from DataModelDict import DataModelDict as DM

import atomman as am
import atomman.unitconvert as uc
import numpy as np

from iprPy.tools import aslist

def todict(record, full=True, flat=True):

    model = DM(record)

    calc = model['calculation-point-defect-formation']
    params = {}
    params['calc_key'] =     calc['key']
    params['calc_script'] =  calc['calculation']['script']
    
    params['energytolerance']=  calc['calculation']['run-parameter']['energytolerance']
    params['forcetolerance'] =  calc['calculation']['run-parameter']['forcetolerance']
    params['maxiterations']  =  calc['calculation']['run-parameter']['maxiterations']
    params['maxevaluations'] =  calc['calculation']['run-parameter']['maxevaluations']
    params['maxatommotion']  =  calc['calculation']['run-parameter']['maxatommotion']
    params['load_options'] =    calc['calculation']['run-parameter']['load_options']
    sizemults =                 calc['calculation']['run-parameter']['size-multipliers']

    params['potential_key'] = calc['potential']['key']
    params['potential_id'] =  calc['potential']['id']
    
    params['load'] =          '%s %s' % (calc['system-info']['artifact']['format'],
                                         calc['system-info']['artifact']['file'])
    params['prototype'] =     calc['system-info']['artifact']['family']
    symbols =                   aslist(calc['system-info']['symbols'])
    
    params['pointdefect_key'] = calc['point-defect']['key']
    params['pointdefect_id'] =  calc['point-defect']['id']
    
    if flat is True:
        params['a_mult1'] = sizemults['a'][0]
        params['a_mult2'] = sizemults['a'][1]
        params['b_mult1'] = sizemults['b'][0]
        params['b_mult2'] = sizemults['b'][1]
        params['c_mult1'] = sizemults['c'][0]
        params['c_mult2'] = sizemults['c'][1]
        for i, symbol in enumerate(symbols):
            params['symbol'+str(i+1)] = symbol
    else:
        params['sizemults'] = np.array([sizemults['a'], sizemults['b'], sizemults['c']])
        params['symbols'] = symbols
    
    params['status'] = calc.get('status', 'finished')
    
    if full is True:
        if params['status'] == 'error':
            params['error'] = calc['error']
        
        elif params['status'] == 'not calculated':
            pass
            
        else:
            params['E_f'] =     uc.value_unit(calc['defect-formation-energy'])
            params['natoms'] =  uc.value_unit(calc['number-of-atoms'])
            
            r_c = calc['reconfiguration-check']
            params['reconfigured'] = iprPy.input.boolean(r_c['has_reconfigured'])
            if flat is False:
                params['centrosummation'] = r_c['centrosummation']
                params['position_shift'] = r_c.get('position_shift', np.nan)
                params['db_vect_shift'] =  r_c.get('db_vect_shift',  np.nan)

    return params 
    
