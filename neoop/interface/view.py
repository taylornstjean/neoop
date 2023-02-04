from datetime import datetime as dt
from texttable import Texttable
from config import __version__, last_update
import os


def version():
    print(f"""\n 
         _   _ ______ ____   ____  _____  
        | \ | |  ____/ __ \ / __ \|  __ \\ 
        |  \| | |__ | |  | | |  | | |__) |
        | . ` |  __|| |  | | |  | |  ___/ 
        | |\  | |___| |__| | |__| | |     
        |_| \_|______\____/ \____/|_|     
        \n\t(MIT License)\n\n\tProgram version: {__version__}\n\tContributors: Taylor St Jean\n\tLast update on {last_update}.\n""")


def proc_out(string):
    print(f"[{dt.now()}]:\033[96m{string}\033[0m")


def std_out(string):
    print(f"{string}")


def err_out(string):
    print(f"[{dt.now()}]: \033[91m[ERROR] {string}\033[0m")


def wrn_out(string):
    print(f"[{dt.now()}]: \033[93m[WARNING] {string}\033[0m")


def table_out(data, outfile):
    table = Texttable(max_width=200)
    table.set_deco(Texttable.HEADER | Texttable.BORDER)
    table.add_rows([data[0].keys()]+[entry.values() for entry in data])

    if not outfile:
        print("\n\n", table.draw(), "\n")
    else:
        try:
            with open(os.path.join(outfile, "neocp_data.txt"), "w") as f:
                f.writelines(table.draw())
        except Exception as e:
            err_out(e)
