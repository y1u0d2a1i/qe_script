from re import I
import numpy as np
import copy
import glob
import os
from ase.io import read 
from pymatgen.core import Structure
from scf.scf_util import get_param_idx, flatten, coord_for_poscar
from scf.scf_util import remove_empty_from_array


class QELattice:
    def __init__(self, path_to_target, name_scf_in='scf.in', name_scf_out='scf.out') -> None:
        self.path_to_target = path_to_target
        self.name_scf_in = name_scf_in
        with open(f'{path_to_target}/{name_scf_in}') as f:
            self.I_lines = [s.strip() for s in f.readlines()]
        with open(f'{path_to_target}/{name_scf_out}') as f:
            self.O_lines = [s.strip() for s in f.readlines()]
        
        self.validate_o_lines()
        
        num_atom = self.I_lines[get_param_idx('nat', self.I_lines)]
        num_atom = num_atom.split(' ')[-1]
        self.num_atom = int(num_atom)
        
        cell_idx = get_param_idx('CELL_PARAMETERS', self.I_lines)
        self.cell = self.I_lines[cell_idx+1 : cell_idx+4]
        
        coord_idx = get_param_idx('ATOMIC_POSITIONS', self.I_lines)
        self.coord = self.I_lines[coord_idx+1 : coord_idx+1+self.num_atom]
        
        self.au2ang = self.get_au2ang()
        self.rv2ev = 13.60

        self.structure_id = list(filter(lambda x: 'mp-' in x, path_to_target.split('/')))[0]

        self.qeltype = 'SCF'
    

    def get_structure(self):
        structure = read(os.path.join(self.path_to_target, self.name_scf_in), format='espresso-in')
        return structure
    

    def validate_o_lines(self):
        if 'JOB DONE.' not in self.O_lines:
            raise Exception("invalid: job didnot finished")
            
        for line in self.O_lines:
            if 'convergence NOT achieved' in line:
                raise Exception('invalid: convergence NOT achieved')

            if 'SCF correction compared to forces is large' in line:
                raise Exception('invalid: Unreliable scf result')

    
    def get_cell(self):
        cell_matlix = self.cell.copy()
        cell_matlix = np.array([list(map(lambda x: float(x), remove_empty_from_array(l.split(' ')))) for l in cell_matlix])
        return cell_matlix

    
    def get_vol(self):
        lattice = self.get_cell()
        a = lattice[0]
        b = lattice[1]
        c = lattice[2]
        vol = np.dot(a, np.cross(b,c))
        return round(vol, 3)
    

    def create_poscar_from_scf(self):
        coord = self.coord.copy()
        coord = coord_for_poscar(coord=coord)
        lines = [f'Si{self.num_atom}', '1.0', self.cell, 'Si', str(self.num_atom), 'direct', coord]
        lines = list(flatten(lines))
        with open(f'{self.path_to_target}/POSCAR', 'w') as f:
            f.write('\n'.join(lines))

    
    def get_coord(self):
        structure = read(os.path.join(self.path_to_target, self.name_scf_in), format='espresso-in')
        return structure.get_positions()

    
    def get_force(self, is_ev_ang=True):
        force_idx = get_param_idx('Forces acting on atoms (cartesian axes, Ry/au):', self.O_lines)  
        start = force_idx+2
        end = force_idx+2 + self.num_atom
        forces = [list(filter(lambda l: l != '', line.split(' ')))[-3:] for line in self.O_lines[start:end]]
        if is_ev_ang:
            forces = [ np.array([float(i) for i in force]) * (self.rv2ev / self.au2ang) for force in forces]
        return np.array(forces)

    
    def get_au2ang(self):
        """ Get convert factor from au(Atomic unit) to angstrom see link below.
        https://courses.engr.illinois.edu/mse404ela/sp2019/6.DFT-walkthrough.html

        Returns:
            float: factor
        """
        # lattice_constant = float(self.cell[0].split(' ')[0])
        # au2ang = lattice_constant
        # return au2ang
        au2ang = 0.529177211
        return au2ang

    
    def get_energy(self, is_ev=True):
        energy_idx = get_param_idx('!', self.O_lines)
        energy = float(list(filter(lambda l: l != '', self.O_lines[energy_idx].split(' ')))[-2])
        if is_ev:
            return energy * self.rv2ev
        else:
            return energy
    
    def get_energy_per_atom(self):
        return self.get_energy() / self.num_atom
        
    
    def get_energy_list(self, is_ev=True):
        l_strip = self.O_lines.copy()
        l_strip = list(filter(lambda l: 'total energy' in l, l_strip))
        l_strip = [list(filter(lambda l: l != '', line.split(' '))) for line in l_strip]
        energy_list = [float(line[-2]) for line in l_strip if 'Ry' in line]
        energy_list = np.array(list(dict.fromkeys(energy_list))) #重複削除(multiprocess時)
        if is_ev:
            energy_list = energy_list * self.rv2ev
        return energy_list