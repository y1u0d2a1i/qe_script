import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
from plot_energy_convergence import plot_scf_convergence


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
        

if __name__ == '__main__':
    template_path = '/Users/y1u0d2/Desktop/Project/qe/template'
    target_dir = '/Users/y1u0d2/Desktop/Project/qe/wip'
    output_dir = '/Users/y1u0d2/Desktop/Project/qe/template'
    
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
            plot_scf_convergence(path_to_target=target_dir, graph_title='scf.out')
            # plot_scf_convergence(output_filename,save_dir=target_dir, save_filename=png_filename)
        except:
            continue
        