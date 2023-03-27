import os
import argparse
from math import inf
import numpy as np
from constants_gaussian import symbols


def main():
    folder, out_name, label_depth, isNested, ext, overwrite = parse_args()
    if folder == '':
        folder = os.getcwd()
    paths = generate_paths(folder, ext, isNested)
    if len(paths) == 0:
        print("No files were found.")
        return None
    selected_results = ask_which_results()
    coordinates = []
    energy_results = [["Filename",
                       "Energy, a.u."]]
    dih_results = [["Filename",
                    "Atom indices",
                    "Element symbols",
                    "Dihedral angle, deg."]]

    if 2 in selected_results:
        dih_sel = ask_which_dehidrals()
    for path in paths:
        energy, coordinates, atoms = read_energies_coordinates(path)

        label = os.path.splitext(path)[0]
        label = ' '.join(label.split('\\')[-label_depth:])

        if 1 in selected_results:
            energy_results.append([label, energy[-1]])  # Final energy.
        if 2 in selected_results:
            for dih_idx in dih_sel:  # Final crd.
                dih_crd = []
                dih_elem = []
                # TODO: add warning notification if atom order between
                # files does not match.
                for d in dih_idx:
                    try:
                        dih_crd.append(coordinates[-1][d - 1])
                    except IndexError:
                        print("Dihedral", dih_idx, "cannot be computed. \
Selected atom does not exist. Aborted.")
                        return None
                    dih_elem.append(symbols[atoms[d - 1]])
                dih = calc_dih(np.array(dih_crd, dtype=float))
                dih_results.append([label, ', '.join(map(str, dih_idx)),
                                    ', '.join(dih_elem), dih])

    if 1 in selected_results:
        energy_fn = os.path.join(folder, out_name + "_energy.txt")
        export_data(energy_results, energy_fn, overwrite)
    if 2 in selected_results:
        dihedrals_fn = os.path.join(folder, out_name + "_dihedrals.txt")
        export_data(dih_results, dihedrals_fn, overwrite)


def parse_args():
    """
    Generates parameters from terminal user specified flags.

    Returns
    -------
    args : tuple
        Returns a tuple of user written flags.

    """
    parser = argparse.ArgumentParser(
        prog="Gaussian result exporter",
        description="Scans multiple gaussian .log or .out files and saves \
selected results to the text file. \
Searching directory can be specified or the script can be run from the \
target directory.")

    parser.add_argument("-i", default='',
                        help="Folder with input files.")
    parser.add_argument("-o", default='',
                        help="Specific beginning for exported data filenames.")
    parser.add_argument("-l", default=1, type=int,
                        help="Specifies the labels for saving results. 0 - no \
labels, 1 - means only filenames will be specified, 2 - also a folder in \
which file exist, 3 - folder of folder and so on.")
    parser.add_argument("-nested", action='store_true',
                        help="Searches for files through subdirectories.")
    parser.add_argument("-e", default='.log',
                        help="Specify the extention, .log is the default.")
    parser.add_argument("-overwrite", action='store_true',
                        help="Disable overwrite protection.")
    args = vars(parser.parse_args()).values()
    return args


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


def check_input(input_msg='', allowed_input=[], list_size=None,
                to_num=None, num_rng=None):
    """
    Checks the input type and returns the requested type. If user input
    is wrong, he will be asked to do it again. Multiple input elements are
    separated with space. num_rng overrides allowed_input.

    Parameters
    ----------
    input_msg : str, optional
        Input message. The default is ''.
    allowed_input : TYPE, optional
        Self-explanatory. The default is [].
    list_size : int, optional
        Used for checking if list length is correct. The default is None.
    to_num : type or None, optional
        Used for converting list elements to numbers. The default is None.
    num_rng : tuple or list, optional
        Allowed numbers range, elements represent minimum and maximum values.
        The default is None.

    Returns
    -------
    inp : list
        Returns user inputted value.

    """
    while True:
        inp = input(input_msg)
        inp = inp.split()
        if not inp:  # Empty list is like False.
            print("You must enter something!")
            continue
        if not (len(inp) == list_size or list_size is None):
            print("You must enter correct length of the input!")
            continue
        if to_num:  # If to_num float or int, it acts as True.
            numbers_idx = []
            for i, a in enumerate(inp):
                try:
                    inp[i] = to_num(a)
                    numbers_idx.append(i)
                except ValueError:
                    pass
            if num_rng:  # If range is specified, input is checked.
                nums_are_valid = True
                for i in numbers_idx:
                    if not num_rng[0] <= inp[i] <= num_rng[1]:
                        print("You must enter a valid number!")
                        nums_are_valid = False
                        break
                if not nums_are_valid:
                    continue
                if allowed_input:
                    for i in numbers_idx:  # num_rng overrides allowed input.
                        allowed_input.append(inp[i])
        if allowed_input:
            if not all(a in allowed_input for a in inp):
                print("Enter valid selection!")
                continue
        return inp


def ask_which_results():
    """
    Promts the terminal with the options for selecting data to save.

    Returns
    -------
    sel_results : list
        A list of selected data.

    """
    result_choice_msg = "Select which results to save (if multiple, seperate \
with space):\n\
  1 - Ground state energies\n\
  2 - Dihedrals\n\
  a - Save everything\n\
  q - Done selecting\n"
    # This part can be modified for adding new options for data export.
    selection_choices = [1, 2]
    print(result_choice_msg)
    sel_results = []
    while True:
        sel_results += check_input(to_num=int,
                                   allowed_input=["a", "q"]+selection_choices)
        if "a" in sel_results:
            sel_results = selection_choices
            print("You have selected everything.")
            break
        elif "q" in sel_results:
            sel_results.remove("q")
            if sel_results == []:
                print("Choose something!")
                continue
            else:
                break
        elif all(s in sel_results for s in selection_choices):
            print("You have selected everything.")
            break
        else:
            print("Anything else?")
            continue
    sel_results = list(dict.fromkeys(sel_results))  # Removing multiples.
    return sel_results


def read_energies_coordinates(path):
    """
    Finds ground state energies in gaussian log file and returns a
    list of them.
    Also searches for all coordinates for all optimization steps.
    TODO differentiate energies when using on scan files and add excited
    gathering.

    Parameters
    ----------
    path : str
        The path of gaussian log file.

    Returns
    -------
    energies : list
        Calculated S0 energies, coordinates, present atoms.

    """
    file = open(path, 'r')
    energies = []
    coordinates = []
    single_crd = []
    atoms = []
    step = 0
    crd_start = 0
    doReadCrd = False
    # Bad (overcomplicated) readibility because of performance reasons.
    for i, line in enumerate(file):
        if line.startswith(" Step number"):
            line_list = line.split()
            new_step = int(line_list[2])
            if new_step > step:
                step = new_step
                continue
            else:
                break
        if line.startswith(" SCF Done:  E("):
            line_list = line.split()
            energies.append(float(line_list[4]))
            continue
        if i > crd_start and doReadCrd:
            if not line.startswith(" -----"):
                line = line.split()
                single_crd.append(line[3:6])
                if step < 1:  # Appending atom types once.
                    atoms.append(int(line[1]))
                continue
            else:
                coordinates.append(single_crd)
                single_crd = []
                doReadCrd = False
        if line.startswith("                          Input orientation:"):
            crd_start = i + 4
            doReadCrd = True

    file.close()
    # Filtering energy from frequency job.
    energies = energies[:step]
    coordinates = coordinates[:step]
    return energies, coordinates, atoms


def ask_which_dehidrals():
    """
    Promts the terminal with the options for selecting data to save.

    Returns
    -------
    sel_results : list
        A list of selected data.

    """
    dihedral_choice_msg = "Select four atoms for which to calculate dihedral \
angle. First atom index is 1. Seperate selection with spaces. Write q to \
finish selections.\n"
    print(dihedral_choice_msg)
    sel_results = []
    while True:
        end_selection = False
        inp = check_input(allowed_input=["q"], to_num=int, num_rng=(1, inf))
        if "q" in inp:
            inp.remove("q")
            if inp == []:
                if sel_results == []:
                    print("Choose something!")
                    continue
                else:
                    break
            end_selection = True
        if len(inp) == 4:
            sel_results.append(inp)
        else:
            print("Enter exactly 4 atom indices!")
            continue
        if end_selection:
            break
        else:
            print("Maybe another dihedral?")
    return sel_results


def export_data(data, filename, overwrite):
    """
    Saves double-nested lists (matrix) to a file

    Parameters
    ----------
    data : double-nested list
        Data to export.
    filename : str
        Slef-explanatory.
    overwrite : bool
        If True, overwrites already existing files, but not folders.

    Returns
    -------
    None.

    """
    if os.path.isfile(filename) and not overwrite:
        print("Result file already exist. Remove it or use -overwrite")
        return None
    elif os.path.isdir(filename):
        print("A folder already exists with the same name as result file. \
Cannot save.")
    file = open(filename, 'w')
    for i, a in enumerate(data):  # Converting numbers to strings.
        for j, b in enumerate(a):
            data[i][j] = str(b)
    for a in data:
        file.write("\t".join(a) + "\n")
    file.close()


def calc_dih(p):
    """
    Praxeolitic formula
    Calculated dihedral angle between four points. 1 sqrt, 1 cross product.
    Source:
    https://stackoverflow.com/questions/20305272/dihedral-torsion-angle-from-four-points-in-cartesian-coordinates-in-python

    Parameters
    ----------
    p : np.ndarray
        Input, 3 column, 4 row matrix, where each row is a cartesian point.

    Returns
    -------
    float
        Calculated positive (or negative) dihedral angle.

    """
    p0 = p[0]
    p1 = p[1]
    p2 = p[2]
    p3 = p[3]

    b0 = -1.0*(p1 - p0)
    b1 = p2 - p1
    b2 = p3 - p2

    # normalize b1 so that it does not influence magnitude of vector
    # rejections that come next
    b1 /= np.linalg.norm(b1)

    # vector rejections
    # v = projection of b0 onto plane perpendicular to b1
    #   = b0 minus component that aligns with b1
    # w = projection of b2 onto plane perpendicular to b1
    #   = b2 minus component that aligns with b1
    v = b0 - np.dot(b0, b1)*b1
    w = b2 - np.dot(b2, b1)*b1

    # angle between v and w in a plane is the torsion angle
    # v and w may not be normalized but that's fine since tan is y/x
    x = np.dot(v, w)
    y = np.dot(np.cross(b1, v), w)
    return np.degrees(np.arctan2(y, x))


if __name__ == '__main__':
    main()
