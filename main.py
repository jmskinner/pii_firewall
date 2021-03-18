import json
import sys
from pii_analyzer import PIIAnalyzer


def parse_args():
    try:
        with open(sys.argv[1]) as json_file:
            return json.load(json_file)
    except Exception:
        print(f'Error reading file from source: {sys.argv[1]}')

def parse_args_test():

    try:
        with open("/Users/skinner/Desktop/mpcs/practicum/pii_analyzer/config.json") as json_file:
            return json.load(json_file)
    except Exception:
        print(f'Error reading file from source: {sys.argv[1]}')


if __name__ == '__main__':
    print("Running the program now")
    analyzer = PIIAnalyzer(parse_args_test())
    analyzer.run()

