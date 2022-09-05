import os

from scf.get_lattice_info import QELattice
from scf.get_relax_lattice_info import RelaxQELattice


def get_qel(path2target):
    if os.path.exists(os.path.join(path2target, 'scf.in')):
        return QELattice(path2target) 
    elif os.path.exists(os.path.join(path2target, 'relax.in')):
        return RelaxQELattice(path2target)
    else:
        raise Exception('files in target directory is not enough')