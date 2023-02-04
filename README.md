# NEOOP

Near Earth Object Observation Program (no affiliation to NASA). Designed for use by the NEO undergraduate observation team at the University of Washington.

Version: 0.2.2

Last updated February 4th, 2023.

[CHANGELOG](https://github.com/taylornstjean/neoop/blob/main/CHANGELOG.md)

---

### Description

This program provides convenience to download and interpret data provided by the Minor Planet Center (MPC) to perform routine observations on Near Earth Objects. 

Automatically converts data to an Azimuth-Elevation frame and determines their visibility. Parameters such as minimum view angle, observatory location and viewing times can be specified. 

Description is a work in progress...

---

### Usage

`neoop.py [options] arguments`

This program currently has limited functionality, more will be added as new versions are released.

| Command&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Description                                                                                                                                                                                                                                                                                                                                                                    |
|---------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-h, --help`                                                        | Display the help page.                                                                                                                                                                                                                                                                                                                                                         |
| `--version`                                                         | Display the program version.                                                                                                                                                                                                                                                                                                                                                   |
| `-p`                                                                | Plot data in one of two formats, `altaz` and `radec` (`altaz` refers to an Altitude/Time graph while `radec` indicates a Right Ascension/Declination plot). The default behavior of this command is to plot all stored objects in a `radec` plot. Use `-t, --type` to specify a plot type and `-d, --desig` to specify a specific NEO to plot using its temporary designation. |
| `-l`                                                                | Display all stored data as a table. Use `-o, --outfile` and specify a filesystem path to save the table as a text file.                                                                                                                                                                                                                                                        |
| `-t, --type`                                                        | Use in conjunction with `-p` to specify a plot type (from `altaz`, `radec`).                                                                                                                                                                                                                                                                                                   |
| `-d, --desig`                                                       | Use in conjunction with `-p` to include an NEO designation. Designations are case sensitive.                                                                                                                                                                                                                                                                                   |
| `-o, --outfile`                                                     | Use in conjunction with `-l` to save the output to a text file. Provide a path to a valid directory to save the text file.                                                                                                                                                                                                                                                     |
| `-u, --update`                                                      | Force the system to update the stored NEOCP data. By default, the update will occur automatically once per hour.                                                                                                                                                                                                                                                               |
| `-c, --cols`                                                        | Use in conjunction with `-l` to only display specified columns.                                                                                                                                                                                                                                                                                                                |


---

### Contributions

If you would like to contribute, please follow these simple instructions:

__Clone the dev branch.__

`git clone -b dev https://github.com/taylornstjean/neoop.git`

Make edits while making sure the code on your system is up to date.

While making modifications, record them in the [CHANGELOG](https://github.com/taylornstjean/neoop/blob/main/CHANGELOG.md) under [Unreleased] using the following categories:

| Category | Description                                                                                                                                                                       |
|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Fixed    | List of any changes that fix an issue or bug.                                                                                                                                     |
| Changed  | List of any changes that don't fix any issues or bugs but may improve the program in some way (i.e. QOL, optimization updates, etc). Can also include any functionality removals. |
| Added    | List of any new additions to the program.                                                                                                                                         |

Commit messages should be one to three word descriptions of the most significant change made.

__Push to dev branch.__

`git push origin dev`

Create a pull request when code is ready to be merged with the master branch.

---

### Acknowledgements

This research has made use of data and/or services provided by the International Astronomical Union's Minor Planet Center.
