#!/home/sagid/.pyenv/shims/python
import argparse
import os

from .treesitter import *


def is_type(args, cb):
    ret = []
    if args.symbol == None: return None

    ts = TS(args.language)

    # ripgrep after the symbol
    results = rg(f"\W{args.symbol}([\W$])", cwd=args.cwd, timeout=args.timeout)
    if results == None: return None
    for file in results:
        file_path = os.path.join(args.cwd, file)
        # use treesitter to parse each file
        tree = ts.get_tree(file_path)
        if tree == None:
            print(f"[!] failed to parse file: {file}")
            continue
        for result in results[file]:
            # if ts_is_xref(tree, result['line_num']):
            y = result['y']
            if cb(ts, tree, ((y-1 if y>0 else y, 0), (y+1, 0))):
                ret.append(f"{file_path}:{result['y']+1}:{result['x']}:{result['text']}")
    return ret

# ACTION_XREFS = 'xrefs'
# def action_xrefs(args):
    # ret = []
    # if args.symbol == None:
        # print(f"the {ACTION_XREFS} action require the symbol argument")
        # return 1
    # results = is_type(args, TS.is_xref)
    # if results == None or len(results) == 0: return 1
    # for r in results: print(r) # is it ok?
    # return 0

ACTION_GOTO_DEFINITION = 'goto-definition'
def action_goto_definition(args):
    ret = []
    if args.symbol == None:
        print(f"the {ACTION_GOTO_DEFINITION} action require the symbol argument")
        return 1
    results = is_type(args, TS.is_definition)
    if results == None or len(results) == 0: return 1
    for r in results: print(r) # is it ok?
    return 0

def main():
    parser = argparse.ArgumentParser(description='gd utility')
    parser.add_argument('--action',
                        choices=[
                            ACTION_GOTO_DEFINITION,
                            # ACTION_XREFS,
                            ],
                        default=ACTION_GOTO_DEFINITION,
                        help='the action we performing')
    parser.add_argument('--language',
                        choices=[
                            'c',
                            'cpp',
                            'python',
                            'smali',
                            'java',
                            ],
                        default='c',
                        help='the language')
    parser.add_argument('--cwd', default='.', help='the cwd to work from')
    parser.add_argument('--timeout', type=int, help='the symbol we operating on')
    parser.add_argument('--symbol', help='the symbol we operating on')
    parser.add_argument('--symbol-location',   help='the symbol location we operating on, '
                        'in the following format: '
                        '<filepath>:<line_num>:<col_num>')
    args = parser.parse_args()

    if args.action == ACTION_GOTO_DEFINITION:
        return action_goto_definition(args)
    # if args.action == ACTION_XREFS:
        # return action_xrefs(args)
    return 1

if __name__ == '__main__':
    exit(main())
