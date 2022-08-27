from scf.get_lattice_info import QELattice
from scf.scf_util import get_param_idx


class RelaxQELattice(QELattice):
    """Lattice info from a result of relax calculation by Quantum espresso

    Args:
        QELattice (_type_): base scf parser
    """
    def __init__(self, path_to_target, name_relax_in='relax.in', name_relax_out='relax.out') -> None:
        super().__init__(path_to_target, name_relax_in, name_relax_out)

        coord_idx = get_param_idx('ATOMIC_POSITIONS', self.O_lines)
        self.coord = self.O_lines[coord_idx+1 : coord_idx+1+self.num_atom]