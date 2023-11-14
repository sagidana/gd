#!/usr/bin/python
import subprocess
import argparse
import os

from treesitter import *


def rg(pattern, cwd=None, timeout=None):
	raw_result = None
	try:
		raw_result = subprocess.run(['rg',
									 '--vimgrep',
									 '-g', '!tags',
									 '--max-columns', '200',
									 '--vimgrep',
									 pattern],
									cwd=cwd,
									timeout=timeout,
									capture_output=True,  # make stdout contain the data
									text=True)			# make stdout point to string
									# check=True)		   # check return code
	except Exception as e:
		print(f"[!] Exception: {e}")
		return None
	results = {}
	for r in raw_result.stdout.splitlines():
		r = r.split(':')
		file_name = r[0]
		y = int(r[1]) - 1 # needs to be 0-based
		x = int(r[2]) 	# rg, why x isn't 1-based like y? WTF
		text = r[3]

		if file_name not in results: results[file_name] = []
		results[file_name].append({
			'y': y,
			'x': x,
			'text': text,
		})
	return results

def is_type(args, cb):
	ret = []
	if args.symbol == None: return None

	ts_init(args.language)

	# ripgrep after the symbol
	results = rg(f"\W{args.symbol}([\W$])", cwd=args.cwd, timeout=args.timeout)
	# results = rg(f"{args.symbol}", cwd=args.cwd, timeout=args.timeout)
	if results == None: return None
	for file in results:
		file_path = os.path.join(args.cwd, file)
		# use treesitter to parse each file
		tree = ts_parse_file(args.language, file_path)
		if tree == None:
			print(f"[!] failed to parse file: {file}")
			continue
		for result in results[file]:
			# if ts_is_xref(tree, result['line_num']):
			if cb(tree, result['x'], result['y']):
				ret.append(f"{file_path}:{result['y']+1}:{result['x']}:{result['text']}")
	return ret

ACTION_XREFS = 'xrefs'
def action_xrefs(args):
	ret = []
	if args.symbol == None:
		print(f"the {ACTION_XREFS} action require the symbol argument")
		return 1
	results = is_type(args, ts_is_xref)
	if results == None or len(results) == 0: return 1
	for r in results: print(r) # is it ok?
	return 0

ACTION_GOTO_DEFINITION = 'goto-definition'
def action_goto_definition(args):
	ret = []
	if args.symbol == None:
		print(f"the {ACTION_GOTO_DEFINITION} action require the symbol argument")
		return 1
	results = is_type(args, ts_is_definition)
	if results == None or len(results) == 0: return 1
	for r in results: print(r) # is it ok?
	return 0

ACTION_BUILD_TREESITTER = 'build-treesitter'
def action_build_treesitter(args):
	if not ts_build_library(): return 1
	return 0

def main():
	parser = argparse.ArgumentParser(description='gd utility')
	parser.add_argument('--action',
						choices=[
							ACTION_GOTO_DEFINITION,
							ACTION_XREFS,
							ACTION_BUILD_TREESITTER,
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
	if args.action == ACTION_XREFS:
		return action_xrefs(args)
	if args.action == ACTION_BUILD_TREESITTER:
		return action_build_treesitter(args)
	return 1

if __name__ == '__main__':
	exit(main())
