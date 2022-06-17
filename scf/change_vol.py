import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import subprocess


template_path = '/Users/y1u0d2/Desktop/Project/qe/template'
target_dir = '/Users/y1u0d2/Desktop/Project/qe/wip'
output_dir = '/Users/y1u0d2/Desktop/Project/qe/template'

def change_lattice_coord(offset, axis, lattice):
    axis = axis.split(' ')
    axis[offset] = lattice
    axis = ' '.join(axis)
    return axis

def create_input_file(lattice, filename):
    with open(f'{template_path}/scf.in') as f:
        l_strip = [s.strip() for s in f.readlines()]
        cell_start_index = l_strip.index('CELL_PARAMETERS {angstrom}')
        a_axis = l_strip[cell_start_index+1]
        b_axis = l_strip[cell_start_index+2]
        c_axis = l_strip[cell_start_index+3]
        
    a_axis = change_lattice_coord(0, a_axis, lattice)
    b_axis = change_lattice_coord(1, b_axis, lattice)
    c_axis = change_lattice_coord(2, c_axis, lattice)

    output_lines = l_strip.copy()
    output_lines[cell_start_index+1] = a_axis
    output_lines[cell_start_index+2] = b_axis
    output_lines[cell_start_index+3] = c_axis
    
    with open(f'{target_dir}/{filename}', mode='w') as f:
        f.write('\n'.join(output_lines))
        
def get_energy_list(filename):
    with open(f'{output_dir}/{filename}') as f:
        l_strip = [s.strip() for s in f.readlines()]
    
    l_strip = list(filter(lambda l: 'total energy' in l, l_strip))
    l_strip = [list(filter(lambda l: l != '', line.split(' '))) for line in l_strip]
    energy_list = [float(line[-2]) for line in l_strip if 'Ry' in line]
    energy_list = list(dict.fromkeys(energy_list)) #重複削除(multiprocess時)
    return energy_list

def plot_scf_convergense(output_filename, save_dir=None, save_filename=None):
    energy_list = get_energy_list(output_filename)
    x = range(1, len(energy_list)+1)
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.set_title(f'scf convergense: {save_filename}')
    ax.set_xlabel('iter')
    ax.set_ylabel('Energy (Ry)')
    ax.plot(x, energy_list)
    if save_dir is not None:
        fig.savefig(f'{save_dir}/{save_filename}.png')

if __name__ == '__main__':
    lattice_range = np.arange(1.7, 6.3, 0.5)
    for lattice in lattice_range:
        lattice = str('{:.2f}'.format(lattice))
        input_filename = f'scf_{lattice}.in'
        output_filename = f'scf_{lattice}.out'
        png_filename = f'scf_{lattice}'
        create_input_file(lattice, input_filename)
        try:
            process = subprocess.Popen(f'mpirun -np 16 pw.x -in {target_dir}/{input_filename} > {output_filename}', shell=True)
            process.wait()
            plot_scf_convergense(output_filename,save_dir=target_dir, save_filename=png_filename)
        except:
            continue
        