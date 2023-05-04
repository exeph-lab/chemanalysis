import os


def transpose(lst):
    return list(map(list, zip(*lst)))


def iterskip(iterator, steps):
    for _ in range(steps):
        next(iterator)


def generate_paths(folder, extention, isNested):
    """
    Generates a list of file paths after scanning specified directory and
    subdirectories if selected.

    Parameters
    ----------
    folder : str
        The path of folder.
    extention : str
        Outputs paths of files of specified extention.
    isNested : bool
        If True, scans and returns paths of subdirectories.

    Returns
    -------
    paths : list
        The list of paths of searched files.

    """
    paths = []
    if isNested:
        for root, dirs, files in os.walk(folder):
            for filename in files:
                if filename.endswith(extention):
                    paths.append(os.path.join(root, filename))
    else:
        for filename in os.listdir(folder):
            file = os.path.join(folder, filename)
            if os.path.isfile(file) and file.endswith(extention):
                paths.append(os.path.join(folder, filename))
    return paths


def export_data(*columns, head, path, overwrite):
    """
    Saves double-nested lists (matrix) to a file

    Parameters
    ----------
    data : double-nested list
        Data to export.
    path : str
        Slef-explanatory.
    overwrite : bool
        If True, overwrites already existing files, but not folders.

    Returns
    -------
    None.

    """
    while True:
        if os.path.isfile(path) and not overwrite:
            print("File already exists. Remove it or use --overwrite")
        elif os.path.isdir(path):
            print("A folder already exists with the same name as the \
path. Cannot save.")
        else:
            break
        inp = input("Try again? (yes or no)\n")
        if inp in ("y", "yes"):
            continue
        else:
            return

    file = open(path, 'w')
    rows = transpose(columns)
    head_space = "\t" * (len(columns) - len(head))
    file.write(head_space + "\t".join(head) + "\n")
    for row in rows:
        if not (None in row):
            file.write("\t".join(map(str, row)) + "\n")
    file.close()
    print("Results saved.\n")
