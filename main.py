import os
from pathlib import Path
from treelib import Tree
from colorama import init, Fore
from datetime import datetime

init(autoreset=True)

folder = Path(r'C:/')


class TreeElement:
    def __init__(self, path: Path, level, children: list = None):
        self.path = path
        self.name = path.name
        if not children:
            self.children = []
        else:
            self.children = children
        try:
            self.files = [(file, round(os.stat(file).st_size / 8 / 1000), 2) for file in path.glob('*') if
                          not file.is_dir()]
            self.files_weight = sum([file[1] for file in self.files])
        except Exception:
            self.files = ['error']
            self.files_weight = 0
        self.weight = get_directory_weight(path)
        self.level = level
        self.parent = path.parent

    def __repr__(self):
        return f'{self.path}'


def get_tree(base_folder: Path, level: int = 0, max_level=None):
    base_tree_element = TreeElement(base_folder, level)
    content = base_folder.glob('*')
    parent = base_tree_element
    level += 1
    for item in content:
        if item.is_dir():
            if max_level and level < max_level:
                base_tree_element.children.append(get_tree(item, level, max_level))
            base_tree_element.parent = parent.parent
    return base_tree_element


def get_directory_weight(directory: Path):
    sub_size = 0
    for path, _, files in os.walk(directory):
        for file in files:
            try:
                filename = os.path.join(path, file)
                sub_size += os.path.getsize(filename) / 1024 / 1024
            except Exception as error:
                print(f'{_}: {error}')
    return round(sub_size, 2)


def draw_tree(tree_el: TreeElement, yellow_mb=None, red_mb=None, limit=None):
    tree_obj = Tree()
    tree_obj.create_node((Fore.BLUE + f'{tree_el.weight} MB: {tree_el}' + Fore.RESET), f'{tree_el.path}')
    tree_obj = draw_tree_iter(tree_el, tree_obj, yellow_mb, red_mb, limit)
    tree_obj.show()


def draw_tree_iter(tree_el: TreeElement, tree_obj: Tree, yellow_mb=None, red_mb=None, limit=None):
    for tree_element in tree_el.children:
        if red_mb and tree_element.weight >= red_mb:
            element = (Fore.RED + f'{tree_element.weight} MB: {tree_element}' + Fore.RESET)
        elif yellow_mb and tree_element.weight >= yellow_mb:
            element = (Fore.YELLOW + f'{tree_element.weight} MB: {tree_element}' + Fore.RESET)
        else:
            element = (Fore.GREEN + f'{tree_element.weight} MB: {tree_element}' + Fore.RESET)
        if tree_element.weight >= limit:
            tree_obj.create_node(element,
                                 f'{tree_element.path}',
                                 parent=f'{tree_element.path.parent}')
        draw_tree_iter(tree_element, tree_obj, yellow_mb, red_mb, limit)
    return tree_obj


def main(directory=Path('xxx'), level=None, limit=None, yellow_mb=None, red_mb=None):
    while True:
        while not directory.is_dir():
            directory = Path(input('Choose directory: '))
        if not level:
            while not level:
                level = input('Choose depth: ')
                level = int(level) if level != '' else 1
        if not limit:
            limit = input('Choose MB limit for visualization: ')
            limit = float(limit) if limit != '' else 1
        if not yellow_mb:
            yellow_mb = input('Choose yellow MB threshold: ')
            yellow_mb = float(yellow_mb) if yellow_mb != '' else None
        if not red_mb:
            red_mb = input('Choose redC; MB threshold: ')
            red_mb = float(red_mb) if red_mb != '' else None

        start = datetime.now()
        tree_object = get_tree(directory, max_level=level)
        draw_tree(tree_object, yellow_mb, red_mb, limit)
        print(f'Done in {(datetime.now() - start).seconds + (datetime.now() - start).microseconds / 1000000}s.\n')
        cont = input('Continue? (y - yes, n - no, r - restart): ').lower().strip()
        if cont == 'n':
            exit()
        elif cont == 'r':
            continue
        else:
            directory = Path('xxx')
            level = None
            limit = None
            yellow_mb = None
            red_mb = None


if __name__ == '__main__':
    main()
