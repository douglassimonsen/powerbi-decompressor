import powerbi
import json


def main():
    pbi = powerbi.PowerBi(r"C:\Users\mwham\Documents\repos\test-decompressor\api.pbix")
    print(pbi.get_table('Kris'))
    print(pbi.update_tables('Kris'))
    print(pbi.get_table('Kris'))
    exit()
    pbi.save_image(r"C:\Users\mwham\Documents\a.pbix")


if __name__ == "__main__":
    main()
