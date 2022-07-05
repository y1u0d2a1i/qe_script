import numpy as np
import random
from scf.scf_util import get_param_idx, remove_empty_from_array
from sympy import re


class ChangeQeInputParam():
    def __init__(self) -> None:
        pass
    
    
    def change_single_param(line, val: int or float):
        line = remove_empty_from_array(line.split(' '))
        line[-1] = str(val)
        line = ' '.join(line)
        return line
    
    
    def change_kpoint(line, val: int or float):
        line = remove_empty_from_array(line.split(' '))
        line[0] = str(val)
        line[1] = str(val)
        line[2] = str(val)
        line = ' '.join(line)
        return line
    
    
    def change_lattice(self, lattice: np.array, displacement: float):
        cell = []
        for l in lattice:
            l = remove_empty_from_array(l.split(' '))
            l = np.array(list(map(float, l)))
            cell.append(l)
        cell = np.array(cell)
        unit_vec = self.get_unit_vec(cell)
        final_cell = cell + displacement * unit_vec
        
        lines = []
        for l in final_cell:
            l = [round(i ,4) for i in l]
            l = list(map(str, l))
            lines.append(' '.join(l))
        return lines
        
    
    
    def change_coord(self, coord_lines: list[str], displacement: float):
        lines = []
        for l in coord_lines:
            l = remove_empty_from_array(l.split(' '))
            l[1] = str(self.add_displacement_to_coord(float(l[1]), displacement))
            l[2] = str(self.add_displacement_to_coord(float(l[2]), displacement))
            l[3] = str(self.add_displacement_to_coord(float(l[3]), displacement))
            l = ' '.join(l)
            lines.append(l)
        return lines
    
    
    def get_unit_vec(vec):
        a = vec[0]
        b = vec[1]
        c = vec[2]
        a_unit = a / np.linalg.norm(a)
        b_unit = b / np.linalg.norm(b)
        c_unit = c / np.linalg.norm(c)
        return np.array([a_unit, b_unit, c_unit])
    
    
    def add_displacement_to_coord(coord:float, displacement:float) -> float:
        coord = coord + round(random.uniform(0, displacement), 3)
        if coord > 1:
            coord = 0.99
        elif coord < 0:
            coord = 0
        return round(coord, 4)
    
    
    def create_input(self, params: dict, path2template, path2target, in_filename='scf.in', out_filename='scf.out'):
            n_atom_param = 'nat'
            with open(f'{path2template}/{in_filename}') as f:
                l_strip = [s.strip() for s in f.readlines()]
            
            for k, v in params.items():
                if k == 'K_POINTS':
                    pass
                
        
    
    