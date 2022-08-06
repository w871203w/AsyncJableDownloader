import argparse

def args_parse():
    parser = argparse.ArgumentParser(prog='jable.py', description='Tutorial')
    parser.add_argument('-u', '--url', type=str, required=False, help='input you want to download url')
    parser.add_argument('-t', '--txt', type=str, required=False)
    return parser.parse_args()