import powerbi
import json


def main():
    pbi = powerbi.PowerBi(r"C:\Users\mwham\Documents\repos\test-decompressor\pbis\api.pbix")
    pbi.load_image()
    print(pbi.read_schema())


if __name__ == "__main__":
    main()
