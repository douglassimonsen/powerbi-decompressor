import powerbi
import json


def main():
    pbi = powerbi.PowerBi(r"C:\Users\mwham\Documents\repos\test-decompressor\api.pbix")
    pbi.update_table('Kris')
    exit()
    pbi.save_image(r"C:\Users\mwham\Documents\a.pbix")


if __name__ == "__main__":
    main()
