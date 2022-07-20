import os
from plistlib import InvalidFileException
import random, string
import shutil


def randomname(n: int) -> str:
    """create random string of n characters

    Args:
        n (int): number of characters
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


def validate_scf_source(path2target: str, path2source: str, all_source_filename: str='all_source.txt') -> None:
    """validate whether scf source already exists in a data list

    Args:
        path2target (str): path to dir which has all_source_filename
        path2source (str): path to scf source
        all_source_filename (str, optional): name of all source file. Defaults to 'all_source.txt'.

    Raises:
        ValueError: if scf source exists
    """
    path2allsource = os.path.join(path2target, all_source_filename)
    if not os.path.exists(path2allsource):
        with open(path2allsource, mode='w') as f:
            pass
        
    with open(path2allsource, mode='r') as f:
        all_path = [s.strip() for s in f.readlines()]
    if path2source in all_path:
        raise ValueError(f'already exists: {path2source}')
    else:
        with open(path2allsource, mode='a') as f:
            f.write(f'\n{path2source}')
    

def add_new_structure_data(path2source: str, path2data: str) -> None:
    """add new structure to data list

    Args:
        path2source (str): path to scf source
        path2data (str): path to data list
    """
    # get structure_id(mp-*) from path2source
    try:
        structure_id = list(filter(lambda x: 'mp-' in x, path2source.split('/')))[0]
    except InvalidFileException as e:
        print(e)
    
        
    path2allsource = os.path.join(path2data, structure_id)
    try:
        validate_scf_source(
            path2target=path2allsource,
            path2source=path2source
            )
    except:
        print(f'already exist: {path2source}')
        return
            
    # ディレクトリの重複管理
    is_loop = True
    while is_loop:
        id_size = random.randint(10, 20)
        id = randomname(id_size)
        path2target = os.path.join(path2data, structure_id, id)
        if os.path.exists(path2target):
            continue
        else:
            os.mkdir(path2target)
            is_loop = False
        
    # scf.in, scf.outのコピー 
    try:
        shutil.copy(os.path.join(path2source, 'scf.in'), path2target)
        shutil.copy(os.path.join(path2source, 'scf.out'), path2target)
    except FileNotFoundError as e:
        print(f'copy: failed: {path2source}')
        print(e)
        os.rmdir(path2target)
        return
    
    # path.txtにデータの元を追記
    with open(os.path.join(path2target, 'path.txt'), mode='w') as f:
        f.write(path2source)
    
    print(f'successfully added: {path2source} to {path2target}, dir name: {id}')