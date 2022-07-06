import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
from scf.scf_util import get_param_idx, remove_empty_from_array


def get_change_param_line(val, line):
    line = remove_empty_from_array(line.split(' '))
    line[0] = str(val)
    line[1] = str(val)
    line[2] = str(val)
    line = ' '.join(line)
    return line


def create_input_file(target_param, param_value, filename, path2template, path2target):
    with open(f'{path2template}/scf.in') as f:
        l_strip = [s.strip() for s in f.readlines()]
        param_idx = get_param_idx(param=target_param, lines=l_strip)
    param_idx += 1
    target_line = get_change_param_line(param_value, l_strip[param_idx])
    output_lines = l_strip.copy()
    output_lines[param_idx] = target_line
    with open(f'{path2target}/{filename}', mode='w') as f:
        f.write('\n'.join(output_lines))


if __name__ == '__main__':
    template_path = '/Users/y1u0d2/Desktop/Project/qe_script/template'
    target_dir = '/Users/y1u0d2/Desktop/Project/qe_script/wip'
    output_dir = '/Users/y1u0d2/Desktop/Project/qe_script/template'
    
    param_name = 'K_POINTS'
    param_range = [1, 2, 3, 4, 5, 6]
    for param_val in param_range:
        prefix = f'scf_kpoint_{param_val}'
        input_filename = f'{prefix}.in'
        output_filename = f'{prefix}.out'
        create_input_file(
            target_param=param_name,
            param_value=param_val,
            filename=input_filename,
            path2template=template_path,
            path2target=target_dir
            )
        try:
            process = subprocess.Popen(
                f'mpiexec.hydra -n 36 -machine $TMPDIR/machines pw.x -in {target_dir}/{input_filename} > {output_dir}/{output_filename}',
                shell=True)
            process.wait()
        except:
            continue