import sys
import argparse
from .view import err_out, table_out, version
from neoop.data import altaz_plot, radec_plot, is_neo, neocp_array, update_neo_data
from config import COLUMNS


def main():

    parser = argparse.ArgumentParser()

    action = parser.add_mutually_exclusive_group()

    action.add_argument('-p', action="store_true", help="Plot NEO's, defaults to all on radec.", required=False)
    action.add_argument('-l', action="store_true", help="Display table with stored data. Use --outfile to save.", required=False)

    parser.add_argument('-u', '--update', action="store_true", help="Force update stored data.", required=False)
    parser.add_argument("-d", "--desig", nargs=1, default=["all"], help="Indicate specific NEO with a designator.")
    parser.add_argument("-t", "--type", nargs=1, default=["radec"], choices=["altaz", "radec"], help="Select graph type for plot.")
    parser.add_argument("-o", "--outfile", nargs=1, default=[None], help="Provide path to save file .")
    parser.add_argument("-c", "--cols", nargs="+", default=None, choices=COLUMNS, help="Select columns to show.")

    parser.add_argument("--version", action="store_true", help="Display program version.")

    args = parser.parse_args()

    if args.p:
        _plot(args.desig[0], args.type[0], args.update)
    if args.l:
        _list(args.outfile[0], args.cols, args.update)
    if args.version:
        _version()


# run on startup

def _init(force):

    update_neo_data(force)


# Define each option

def _version():

    version()


def _plot(desig, typ, upd):

    _init(upd)

    if not is_neo(desig) and desig != "all":
        err_out("Specified NEO does not exist. Caution: Designation is case sensitive.")
        sys.exit(2)

    if typ == "radec":
        radec_plot(temp_desig=desig if desig != "all" else None)
    elif typ == "altaz":
        altaz_plot(temp_desig=desig if desig != "all" else None)
    else:
        err_out("Invalid plot type. Use -h for help.")
        sys.exit(2)


def _list(outfile, cols, upd):

    _init(upd)

    table_out(neocp_array(cols), outfile)
