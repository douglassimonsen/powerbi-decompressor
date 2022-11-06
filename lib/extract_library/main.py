import powerbi
import initialization
from pprint import pprint


def main():
    pbi = powerbi.PowerBi(r"C:\Users\mwham\Documents\repos\test-decompressor\pbis\api.pbix")
    pprint(pbi.read_schema())


if __name__ == "__main__":
    initialization.kill_current_servers()
    main()
