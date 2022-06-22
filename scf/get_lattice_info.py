import numpy as np
import copy
from pymatgen.core import Structure
from scf.scf_util import get_param_idx, flatten, coord_for_poscar


class QELattice:
    def __init__(self, path_to_target) -> None:
        self.path_to_target = path_to_target
        with open(f'{path_to_target}/scf.in') as f:
            self.I_lines = [s.strip() for s in f.readlines()]
        with open(f'{path_to_target}/scf.out') as f:
            self.O_lines = [s.strip() for s in f.readlines()]
        num_atom = self.I_lines[get_param_idx('nat', self.I_lines)]
        num_atom = num_atom.split(' ')[-1]
        self.num_atom = int(num_atom)
        
        cell_idx = get_param_idx('CELL_PARAMETERS', self.I_lines)
        self.cell = self.I_lines[cell_idx+1 : cell_idx+4]
        
        coord_idx = get_param_idx('ATOMIC_POSITIONS', self.I_lines)
        self.coord = self.I_lines[coord_idx+1 : coord_idx+1+self.num_atom]
        
        self.au2ang = self.get_au2ang()
        self.rv2ev = 13.60
    
    def get_cell(self):
        cell_matlix = self.cell.copy()
        cell_matlix = np.array([list(map(lambda x: float(x), l.split(' '))) for l in cell_matlix])
        return cell_matlix
    
    def create_poscar_from_scf(self, lines):
        coord = self.coord.copy()
        coord = coord_for_poscar(coord=coord)
        lines = [f'Si{self.num_atom}', '1.0', self.cell, 'Si', str(self.num_atom), 'direct', coord_for_poscar(coord)]
        lines = list(flatten(lines))
        with open(f'{self.path_to_target}/POSCAR', 'w') as f:
            f.write('\n'.join(lines))
    
    def get_coord(self):
        structure = Structure.from_file(f"{self.path_to_target}/POSCAR")
        return np.array(structure.cart_coords)
    
    def get_force(self):
        force_idx = get_param_idx('Forces acting on atoms (cartesian axes, Ry/au):', self.O_lines)  
        start = force_idx+2
        end = force_idx+2 + self.num_atom
        forces = [list(filter(lambda l: l != '', line.split(' ')))[-3:] for line in self.O_lines[start:end]]
        forces = [ np.array([float(i) for i in force]) * (self.rv2ev / self.au2ang) for force in forces]
        return np.array(forces)
    
    def get_au2ang(self):
        lattice_constant = float(self.cell[0].split(' ')[0])
        au_idx = get_param_idx('lattice parameter (alat)', self.O_lines)
        au = float(list(filter(lambda l: l != '', self.O_lines[au_idx].split(' ')))[-2])
        au2ang = lattice_constant / au
        return au2ang
    
    def get_energy(self, is_ev=True):
        energy_idx = get_param_idx('!', self.O_lines)
        energy = float(list(filter(lambda l: l != '', self.O_lines[energy_idx].split(' ')))[-2])
        if is_ev:
            return energy * self.rv2ev
        else:
            return energy
        