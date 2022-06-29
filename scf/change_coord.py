import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import random
import os
from scf.scf_util import get_param_idx
    
    
def change_coord(coord:float, displacement:float) -> float:
    coord = coord + round(random.uniform(0, displacement), 3)
    if coord > 1:
        coord = 0.99
    elif coord < 0:
        coord = 0
    return round(coord, 4)


def create_input_file(target_param, target_path, template_path, displacement):
    n_atom_param = 'nat'
    with open(f'{template_path}/scf.in') as f:
        l_strip = [s.strip() for s in f.readlines()]
        param_idx = get_param_idx(param=target_param, lines=l_strip)
        n_atom_idx = get_param_idx(param=n_atom_param, lines=l_strip)
    param_idx += 1
    n_atom = int(l_strip[n_atom_idx].split(' ')[-1])
    
    coord_lines = l_strip[param_idx : param_idx+n_atom]
    new_coord_lines = []
    for l in coord_lines:
        l = l.split(' ')
        l = list(filter(None, l))
        l[1] = str(change_coord(float(l[1]), displacement))
        l[2] = str(change_coord(float(l[2]), displacement))
        l[3] = str(change_coord(float(l[3]), displacement))
        l = ' '.join(l)
        new_coord_lines.append(l)
    
    output_lines = l_strip.copy()
    output_lines[param_idx : param_idx+n_atom] = new_coord_lines
    with open(target_path, mode='w') as f:
        f.write('\n'.join(output_lines))


if __name__ == '__main__':
    template_path = '/Users/y1u0d2/desktop/Lab/result/qe/Si/mp-165/template'
    target_dir = '/Users/y1u0d2/desktop/Lab/result/qe/Si/mp-165/coord/l_1'
    
    param_name = 'ATOMIC_POSITIONS'
    n_sample = 3
    displacement = 0.21
    for i in range(n_sample):
        current_dir = os.path.join(target_dir, f'scf_{i}')
        os.mkdir(current_dir)
        if not os.path.exists(current_dir):
            print(f'path not exist : {current_dir}')
            break
        
        input_filename = 'scf.in'
        output_filename = 'scf.out'
        create_input_file(
            target_param=param_name,
            target_path=os.path.join(current_dir, input_filename),
            template_path=template_path,
            displacement=displacement
            )
        try:
            process = subprocess.Popen(
                f'OMP_NUM_THREADS=4 mpirun -np 8 pw.x -in {current_dir}/{input_filename} > {current_dir}/{output_filename}',
                shell=True)
            process.wait()
        except:
            continue