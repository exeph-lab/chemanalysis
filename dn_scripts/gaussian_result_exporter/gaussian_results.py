import os
import argparse
import numpy as np
from elements import atomnames2str
from utilities import transpose, iterskip, generate_paths, export_data

energy_headers = ("Filename",
                  "Energy, a.u.")

distance_headers = ("Filename",
                    "Atoms",
                    "Distance, nm?.")

neighbours_headers = ("Filename",
                      "Atom",
                      "Distances, nm?.")

dihedral_headers = ("Filename",
                    "Atoms",
                    "Dihedral, deg.")

thermo_headers = ("Filename",
                  "Zero-point correction (Hartree/Particle)",
                  "Thermal correction to Energy",
                  "Thermal correction to Enthalpy",
                  "Thermal correction to Gibbs Free Energy",
                  "Sum of electronic and zero-point Energies",
                  "Sum of electronic and thermal Energies",
                  "Sum of electronic and thermal Enthalpies",
                  "Sum of electronic and thermal Free Energies")

counterpoise_headers = ("Filename",
                        "Counterpoise corrected energy",
                        "BSSE energy",
                        "sum of monomers",
                        "complexation energy (raw)",
                        "complexation energy (corrected)")


def main():
    args = parse_args()
    if args.folder == '':
        args.folder = os.getcwd()
    paths = generate_paths(args.folder, args.extention, args.nested)
    if len(paths) == 0:
        print("No files were found.")
        return
    data = []
    for path in paths:
        data.append(Gdata(path, args.label, args.link1))
    for c in range(len(data) - 1):
        if data[c].atomnames[-1] != data[c + 1].atomnames[-1]:
            print("The arrangement of atoms in the final geometry varies \
between files. Be careful!")
            break

    while True:
        event = ask_results()
        if event is None:
            break
        if event == "1":
            if args.custom:
                filename = input("Enter filename:")
            else:
                filename = "energy.txt"
            path = os.path.join(args.folder, filename)
            export_data(get_labels(data),
                        get_energies(data),
                        head=energy_headers,
                        path=path,
                        overwrite=args.overwrite)

        if event == "3":
            if args.custom:
                filename = input("Enter filename:")
            else:
                filename = "thermo.txt"
            path = os.path.join(args.folder, filename)
            results = get_thermo(data)
            if any((None in res) for res in results):
                print("Warning: Thermo data is not available for some files, \
--link1 flag may fix the issue.")
            export_data(get_labels(data),
                        *transpose(results),
                        head=thermo_headers,
                        path=path,
                        overwrite=args.overwrite)

        if event == "4":
            if args.custom:
                filename = input("Enter filename:")
            else:
                filename = "counterpoise.txt"
            path = os.path.join(args.folder, filename)
            results = get_counterpoise(data)
            export_data(get_labels(data),
                        *transpose(results),
                        head=counterpoise_headers,
                        path=path,
                        overwrite=args.overwrite)

            if False:  # TODO: Not implemented yet. #event == "5":
                if args.custom:
                    filename = input("Enter filename:")
                else:
                    filename = "distance.txt"
                path = os.path.join(args.folder, filename)
                print("Select two atoms indices for which to calculate distance. \
    First atom index is 1. Seperate selection with spaces. \
    Write q to finish selections.")
                count = 0
                while True:
                    indices = ask_distances()
                    if indices is None:
                        break
                    for d in data:
                        d.calc_dist(indices)
                    count += 1
                    print("Anything else?")

                labels = get_labels(data) * count
                results = []
                for i in range(count):
                    results += get_distances(data, i)

                export_data(labels,
                            *transpose(results),
                            head=distance_headers,
                            path=path,
                            overwrite=args.overwrite)

        if event == "6":
            if args.custom:
                filename = input("Enter filename:")
            else:
                filename = "neighbours.txt"
            path = os.path.join(args.folder, filename)
            print("Select one atom index for which to calculate distance to\
neighbours. First atom index is 1. Write q to finish selections.")
            count = 0
            while True:
                index = ask_neighbours()
                if index is None:
                    break
                for d in data:
                    d.calc_nbr(index, 2.35)
                count += 1
                print("Anything else?")

            labels = get_labels(data) * count
            results = []
            for i in range(count):
                results += get_neighbours(data, i)

            export_data(labels,
                        *transpose(results),
                        head=neighbours_headers,
                        path=path,
                        overwrite=args.overwrite)

        if event == "8":
            if args.custom:
                filename = input("Enter filename:")
            else:
                filename = "dihedrals.txt"
            path = os.path.join(args.folder, filename)
            print("Select four atoms indices for which to calculate dihedral \
angle. First atom index is 1. Seperate selection with spaces. \
Write q to finish selections.")
            count = 0
            while True:
                indices = ask_dehidrals()
                if indices is None:
                    break
                for d in data:
                    d.calc_dih(indices)
                count += 1
                print("Anything else?")

            labels = get_labels(data) * count
            results = []
            for i in range(count):
                results += get_dihedrals(data, i)

            export_data(labels,
                        *transpose(results),
                        head=dihedral_headers,
                        path=path,
                        overwrite=args.overwrite)


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

    parser.add_argument(
        "-f", "--folder", default='', metavar='\b',
        help="folder with input files."
        )
    parser.add_argument(
        "--link1", action='store_true',
        help="do not ignore non-first link1 jobs (for e.g. opt and freq)"
        )
    parser.add_argument(
        "-c", "--custom", action='store_true',
        help="custom filenames for exported data"
        )
    parser.add_argument(
        "-l", "--label", default=1, type=int,
        help="specifies the labels during exporting:\n\
0 - no labels,\n\
1 - filename,\n\
2 - folder/filename,\n\
3 - root/folder/filename and so on"
        )
    parser.add_argument(
        "-n", "--nested", action='store_true',
        help="searches for files through subdirectories"
        )
    parser.add_argument(
        "-e", "--extention", default='.log', metavar='\b',
        help="    specify the extention, .log is the default"
        )
    parser.add_argument(
        "-o", "--overwrite", action='store_true',
        help="disable overwrite protection"
        )
    return parser.parse_args()


class Gdata():
    def __init__(self, path, label_depth, allowLink1):
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
        self.distance = []
        self.neighbours = []
        self.angles = []
        self.dihedrals = []
        

        label = os.path.splitext(path)[0]
        label = '\t'.join(label.split('\\')[-label_depth:])
        self.label = label

        self.path = path
        file = open(path, 'r')

        self.coordinates = []
        self.atomnames = []
        self.energies = []
        self.steps = []
        self.thermo = (None, ) * 8  # Needed for exporting.
        self.counter = (None, ) * 5  # Needed for exporting.
        doReadCrd = False
        isAtomsOrdered = True
        # Skipping first lines, where link1 string may be.
        iterator = enumerate(file)
        iterskip(iterator, 30)
        for i, line in iterator:
            line = line.strip()
            if line.startswith("Input orientation:"):
                iterskip(iterator, 4)
                sp_coordinates = []
                sp_atomnames = []
                doReadCrd = True
                continue

            if doReadCrd:
                if not line.startswith("-----"):
                    line = line.split()
                    sp_coordinates.append(tuple(map(float, line[3:6])))
                    sp_atomnames.append(int(line[1]))
                    continue
                else:
                    self.coordinates.append(sp_coordinates)
                    if isAtomsOrdered:
                        if len(self.atomnames) > 1:
                            if self.atomnames[-1] != sp_atomnames:
                                isAtomsOrdered = False
                    self.atomnames.append(sp_atomnames)
                    doReadCrd = False
                    continue

            if line.startswith("SCF Done:  E("):
                line_list = line.split()
                self.energies.append(float(line_list[4]))
                continue

            if line.startswith("Step number"):
                line_list = line.split()
                self.steps.append(int(line_list[2]) - 1)  # Pythonic counting.
                continue

            if line.startswith("Zero-point correction="):
                # Assuming that there is single freq calculaiton in one file.
                self.thermo = []
                for _ in range(8):
                    line = line.split('=')[-1]
                    line = line.split('(')  # Removing "(Hartree/Particle)".
                    self.thermo.append(float(line[0].strip()))
                    i, line = next(iterator)
                continue

            if line.startswith("Counterpoise corrected energy ="):
                # Assuming that there is single counterpoise.
                self.counter = []
                for _ in range(5):
                    line = line.split('=')[-1]
                    line = line.split('k')  # Removing "kcal/mole".
                    self.counter.append(float(line[0].strip()))
                    i, line = next(iterator)
                continue

            if not allowLink1:
                if (line.startswith("Entering Link 1 ") or
                        line.startswith("Link1:")):
                    break
        file.close()

        if not isAtomsOrdered:
            print("Warning: Atom ordering changed during gaussian \
calculations in %s" % path)

    def calc_dih(self, indices, step=-1):
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
        atomnames = atomnames2str(self.atomnames[step])
        if max(indices) >= len(atomnames):
            print("Warning: Selected dihedral is out of bounds in %s. \
It was not calcualted." % self.path)
            self.dihedrals.append((None, None))
            return
        atomnames = ' '.join(atomnames[i] for i in indices)

        coordinates = self.coordinates[step]
        p0, p1, p2, p3 = (np.array(coordinates[i]) for i in indices)

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
        v = b0 - np.dot(b0, b1) * b1
        w = b2 - np.dot(b2, b1) * b1

        # angle between v and w in a plane is the torsion angle
        # v and w may not be normalized but that's fine since tan is y/x
        x = np.dot(v, w)
        y = np.dot(np.cross(b1, v), w)
        dih = np.degrees(np.arctan2(y, x))

        self.dihedrals.append((atomnames, dih))

    def calc_dist(self, indices, step=-1):
        atomnames = atomnames2str(self.atomnames[step])
        if max(indices) >= len(atomnames):
            print("Warning: Selected distance is out of bounds in %s. \
It was not calcualted." % self.path)
            self.distance.append((None, None))
            return
        atomnames = ' '.join(atomnames[i] for i in indices)

        coordinates = self.coordinates[step]
        p0, p1 = (np.array(coordinates[i]) for i in indices)

        dist = np.linalg.norm(p0 - p1)
        self.distance.append((atomnames, dist))

    def calc_nbr(self, index, threshold, step=-1):
        atomnames = atomnames2str(self.atomnames[step])
        if max(index) >= len(atomnames):
            print("Warning: Selected atom is out of bounds in %s. \
Distances to neighbours were not calculated." % self.path)
            self.neighbours.append((None, None))
            return

        coordinates = self.coordinates[step]

        index, = index
        neighbours = ''
        p0 = np.array(coordinates[index])
        for i in range(len(coordinates)):
            if i != index:
                p1 = np.array(coordinates[i])
                dist = np.linalg.norm(p0 - p1)
                if dist < threshold:
                    neighbours += ("%s\t%.3f\t" % (atomnames[i], dist))

        self.neighbours.append((atomnames[index], neighbours.strip()))


def get_labels(datalist):
    return [d.label for d in datalist]


def get_coordinates(datalist, step=-1):
    return [d.coordinates[step] for d in datalist]


def get_neighbours(datalist, idx):
    return [d.neighbours[idx] for d in datalist]


def get_atomnames(datalist, step=-1):
    return [d.atomnames[step] for d in datalist]


def get_energies(datalist, step=-1):
    return [d.energies[step] for d in datalist]


def get_dihedrals(datalist, idx):
    return [d.dihedrals[idx] for d in datalist]


def get_thermo(datalist):
    return [d.thermo for d in datalist]

def get_counterpoise(datalist):
    return [d.counter for d in datalist]


def ask_results():
    """
    Promts the terminal with the options for selecting data to save.

    Returns
    -------
    sel_results : list
        A list of selected data.

    """
    result_choice_msg = "Select which results do you want to save:\n\
  1 - Ground state energies\n\
  3 - Thermo information\n\
  4 - Counterpoise information\n\
  5 - Distances\n\
  6 - Closest atoms\n\
  8 - Dihedrals\n\
  q - Exit"
    # This part can be modified for adding new options for data export.
    print(result_choice_msg)
    selection_choices = ["1", "3", "4", "5", "6", "8"]
    while True:
        inp = input().strip()
        if inp in selection_choices:
            return inp
        elif inp == "q":
            return
        elif inp == '':
            print("Choose something!")
        else:
            print("Enter valid selection!")


def ask_dehidrals():
    """
    Promts the terminal with the options for selecting data to save.
    TODO: clean up this mess, tidy up
    Returns
    -------
    sel_results : list
        A list of selected data.

    """
    while True:
        inp = input()
        if inp == "q":
            return
        elif inp == '':
            print("Choose something!")
            continue
        inp = inp.split()
        if len(inp) != 4:
            print("You must enter indices of 4 atoms!")
            continue
        if all(a.isdigit() for a in inp):
            return [int(x) - 1 for x in inp]
        else:
            print("Enter valid selection!")


def ask_neighbours():
    """
    Promts the terminal with the options for selecting data to save.
    TODO: clean up this mess, tidy up
    Returns
    -------
    sel_results : list
        A list of selected data.

    """
    while True:
        inp = input()
        if inp == "q":
            return
        elif inp == '':
            print("Choose something!")
            continue
        inp = inp.split()
        if len(inp) != 1:
            print("You must enter indices of 1 atoms!")
            continue
        if all(a.isdigit() for a in inp):
            return [int(x) - 1 for x in inp]
        else:
            print("Enter valid selection!")


if __name__ == '__main__':
    main()
