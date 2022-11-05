import parse_datasources
import json


def main(raw_data):
    data = parse_datasources.main(raw_data)


if __name__ == '__main__':
    with open('test.json') as f:
        data = json.load(f)
    main(data)