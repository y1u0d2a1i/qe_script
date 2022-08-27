import numpy as np

from scf.get_lattice_info import QELattice
from scf.scf_util import get_param_idx, remove_empty_from_array


class RelaxQELattice(QELattice):
    """Lattice info from a result of relax calculation by Quantum espresso

    Args:
        QELattice (_type_): base scf parser
    """
    def __init__(self, path_to_target, name_relax_in='relax.in', name_relax_out='relax.out') -> None:
        super().__init__(path_to_target, name_relax_in, name_relax_out)

        coord_idx = get_param_idx('ATOMIC_POSITIONS', self.O_lines)
        self.coord = self.O_lines[coord_idx+1 : coord_idx+1+self.num_atom]
    

    def get_scaled_coord(self):
        scaled_coord = []
        for atom in self.coord:
            atom = remove_empty_from_array(atom.split(' '))[1:]
            scaled_coord.append([float(i) for i in atom])
            # atom = ' '.join([float(i) for i in atom])
        return np.array(scaled_coord)