import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import subprocess

template_path = '/Users/y1u0d2/Desktop/Project/qe/template'
target_dir = '/Users/y1u0d2/Desktop/Project/qe/wip'
output_dir = '/Users/y1u0d2/Desktop/Project/qe/template'

def get_change_param_line(val, line):
    line = line.split(' ')
    line[-1] = str(val)
    line = ' '.join(line)
    return line

def get_param_idx(param, lines):
    param_idx = None
    for i, l in enumerate(lines):
        if param in l:
            param_idx = i
    if param_idx is None:
        raise ValueError('invalid param')
    else:
        return param_idx

def create_input_file(target_param,param_value, filename):
    with open(f'{template_path}/scf.in') as f:
        l_strip = [s.strip() for s in f.readlines()]
        param_idx = None
        for i, l in enumerate(l_strip):
            if target_param in l:
                param_idx = i

    target_line = l_strip[param_idx]
    target_line = get_change_param_line(param_value, target_line)

    output_lines = l_strip.copy()
    output_lines[param_idx] = target_line
    output_lines[param_idx]
    with open(f'{target_dir}/{filename}', mode='w') as f:
        f.write('\n'.join(output_lines))


def get_energy_list(filename):
    with open(f'{output_dir}/{filename}') as f:
        l_strip = [s.strip() for s in f.readlines()]

    l_strip = list(filter(lambda l: 'total energy' in l, l_strip))
    l_strip = [list(filter(lambda l: l != '', line.split(' '))) for line in l_strip]
    energy_list = [float(line[-2]) for line in l_strip if 'Ry' in line]
    energy_list = list(dict.fromkeys(energy_list))  # 重複削除(multiprocess時)
    return energy_list


def plot_scf_convergence(output_filename, save_dir=None, save_filename=None):
    energy_list = get_energy_list(output_filename)
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
    param_range = [10, 20, 30, 40, 50, 60, 70]
    param_name = 'ecutwfc'
    for param_val in param_range:
        prefix = f'scf_ecut_{param_val}'
        input_filename = f'{prefix}.in'
        output_filename = f'{prefix}.out'
        create_input_file(target_param=param_name,param_value=param_val, filename=input_filename)
        try:
            process = subprocess.Popen(
                f'mpirun -np 16 pw.x -in {target_dir}/{input_filename} > {output_filename}',
                shell=True)
            process.wait()
        except:
            continue