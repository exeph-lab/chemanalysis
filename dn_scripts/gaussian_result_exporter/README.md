# Gaussian result explorer

Gaussian result explorer is a Python program for dealing with Gaussian 09 or 16 output files. Currently ground state energies and dihedrals angles exporting is  supported. Scans multiple gaussian .log or .out files and saves selected results to the text file. Searching directory can be specified or the script can be run from the target directory.

## Usage

The program is run from terminal:

```
python3 get_results_gaussian.py [-h] [-i I] [-o O] [-l L] [-nested] [-e E] [-overwrite]
```
Optional arguments: <br />
  -h, --help  show this help message and exit <br />
  -i I  Folder with input files. <br />
  -o O  Specific beginning for exported data filenames. <br />
  -l L  Specifies the labels for saving results. 0 - no labels, 1 - means only filenames will be specified, 2 - also a folder in which file exist, 3 - folder of folder and so on.  <br />
  -nested Searches for files through subdirectories.  <br />
  -e E  Specify the extention, .log is the default.  <br />
  -overwrite  Disable overwrite protection.  <br />

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
