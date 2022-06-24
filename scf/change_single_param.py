import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
from scf.scf_util import get_param_idx, get_energy_list


def get_change_param_line(val, line):
    line = line.split(' ')
    line[-1] = str(val)
    line = ' '.join(line)
    return line


def create_input_file(target_param, param_value, filename, path2template, path2target):
    with open(f'{path2template}/scf.in') as f:
        l_strip = [s.strip() for s in f.readlines()]
        param_idx = get_param_idx(param=target_param, lines=l_strip)

    target_line = l_strip[param_idx]
    target_line = get_change_param_line(param_value, target_line)

    output_lines = l_strip.copy()
    output_lines[param_idx] = target_line
    output_lines[param_idx]
    with open(f'{path2target}/{filename}', mode='w') as f:
        f.write('\n'.join(output_lines))


def plot_scf_convergence(output_filename, path2target, save_dir=None, save_filename=None):
    energy_list = get_energy_list(path_to_target=path2target, filename=output_filename)
    x = range(1, len(energy_list) + 1)
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.set_title(f'scf convergense: {save_filename}')
    ax.set_xlabel('iter')
    ax.set_ylabel('Energy (Ry)')
    ax.plot(x, energy_list)
    if save_dir is not None:
        fig.savefig(f'{save_dir}/{save_filename}.png')


if __name__ == '__main__':
    path2template = '/Users/y1u0d2/Desktop/Project/qe/template'
    path2target = '/Users/y1u0d2/Desktop/Project/qe/wip'
    path2out = '/Users/y1u0d2/Desktop/Project/qe/template'
    
    param_range = [10, 20, 30, 40, 50, 60, 70]
    param_name = 'ecutwfc'
    for param_val in param_range:
        prefix = f'scf_ecut_{param_val}'
        input_filename = f'{prefix}.in'
        output_filename = f'{prefix}.out'
        create_input_file(target_param=param_name,param_value=param_val, filename=input_filename)
        try:
            process = subprocess.Popen(
                f'mpirun -np 8 pw.x -in {path2target}/{input_filename} > {path2out}/{output_filename}',
                shell=True)
            process.wait()
        except:
            continue