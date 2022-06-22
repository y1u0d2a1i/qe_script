import numpy as np
import matplotlib.pyplot as plt
from scf_util import get_energy_list

def plot_scf_convergence(path_to_target, path_to_save_dir=None, save_filename=None, graph_title=None, is_ev=True):
    energy_list = get_energy_list(path_to_target=path_to_target, is_ev=is_ev)
    x = range(1, len(energy_list) + 1)
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.set_title(f'scf convergense: {graph_title}')
    ax.set_xlabel('iter')
    if is_ev:
        ax.set_ylabel('Energy (eV)')
    else:
        ax.set_ylabel('Energy (Ry)')
    ax.plot(x, energy_list)
    if path_to_save_dir is not None:
        fig.savefig(f'{path_to_save_dir}/{save_filename}.png')