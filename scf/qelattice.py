import os
import pickle

from scf.get_lattice_info import QELattice
from scf.get_relax_lattice_info import RelaxQELattice


def get_qel_from_bin(path2target, bin_filename='qel.bin'):
    with open(os.path.join(path2target, bin_filename), 'rb') as p:
        qel = pickle.load(p)
    return qel


def get_qel(path2target):
    if os.path.exists(os.path.join(path2target, 'qel.bin')):
        return get_qel_from_bin(path2target)

    if os.path.exists(os.path.join(path2target, 'scf.in')):
        return QELattice(path2target) 
    elif os.path.exists(os.path.join(path2target, 'relax.in')):
        return RelaxQELattice(path2target)
    else:
        raise Exception('files in target directory is not enough')