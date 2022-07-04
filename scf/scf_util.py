import numpy as np
import collections

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
    get param index from scf.in and scf.out
    """
    param_idx = None
    for i, l in enumerate(lines):
        if param in l:
            param_idx = i
    if param_idx is None:
        raise ValueError('invalid param')
    else:
        return param_idx


def coord_for_poscar(coord):
    """
    scf.inの座標をPOSCARファイル用に変換
    """
    for i, line in enumerate(coord):
        tmp = line.split(' ')[1:]
        atom_type = line.split(' ')[0]
        tmp.append(atom_type)
        line = ' '.join(tmp)
        coord[i] = line
    return coord

def flatten(l):
    for el in l:
        if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el
            

def remove_empty_from_array(arr: list) -> list:
    return list(filter(None, arr))