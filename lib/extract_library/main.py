import powerbi
import initialization


def main():
    pbi = powerbi.PowerBi(r"C:\Users\mwham\Documents\repos\test-decompressor\pbis\api.pbix")
    print(pbi.read_schema())


if __name__ == "__main__":
    initialization.kill_current_servers()
    main()
