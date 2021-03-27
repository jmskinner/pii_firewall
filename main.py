import json
import sys
from pii_firewall import PIIFirewall


def parse_args():
    try:
        with open(sys.argv[1]) as json_file:
            return json.load(json_file)
    except Exception:
        print(f'Error reading file from source: {sys.argv[1]}')

def parse_args_test():

    try:
        with open("example_config.json") as json_file:
            return json.load(json_file)
    except Exception:
        print(f'Error reading file from source: {sys.argv[1]}')

def bordered(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐']
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')
    return '\n'.join(res)


if __name__ == '__main__':
    results_path = '/Users/skinner/Desktop/mpcs/practicum/pii_firewall/testing/output'
    print(bordered("Running the program now"))
    config = parse_args_test()
    analyzer = PIIFirewall(config)
    analyzer.run()
    print(bordered("Run is commplete!"))

