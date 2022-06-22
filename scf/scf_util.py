import numpy as np

def get_energy_list(path_to_target, filename='scf.out', is_ev=True):
    ry_to_ev = 13.60
    with open(f'{path_to_target}/{filename}') as f:
        l_strip = [s.strip() for s in f.readlines()]
    
    l_strip = list(filter(lambda l: 'total energy' in l, l_strip))
    l_strip = [list(filter(lambda l: l != '', line.split(' '))) for line in l_strip]
    energy_list = [float(line[-2]) for line in l_strip if 'Ry' in line]
    energy_list = np.array(list(dict.fromkeys(energy_list))) #重複削除(multiprocess時)
    if is_ev:
        energy_list = energy_list * ry_to_ev
    return energy_list


def get_param_idx(param, lines):
    """
    get param index from scf.in
    """
    param_idx = None
    for i, l in enumerate(lines):
        if param in l:
            param_idx = i
    if param_idx is None:
        raise ValueError('invalid param')
    else:
        return param_idx