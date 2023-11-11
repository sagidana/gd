#!/usr/bin/python
import subprocess
import argparse
import os

from treesitter import *


def rg(pattern, cwd=None, timeout=None):
	raw_result = None
	try:
		raw_result = subprocess.run(['rg','-n', pattern],
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
		line_num = int(r[1])
		text = r[2]

		if file_name not in results: results[file_name] = []
		results[file_name].append({
			'line_num': line_num,
			'text': text,
		})
	return results

ACTION_XREFS = 'xrefs'
def action_xrefs(args): return 1

ACTION_GOTO_DEFINITION = 'goto-definition'
def action_goto_definition(args):
	ret = []
	if args.symbol == None:
		print(f"the {ACTION_GOTO_DEFINITION} action require the symbol argument")
		return 1

	ts_init(args.language)

	# ripgrep after the symbol
	results = rg(args.symbol, cwd=args.cwd, timeout=args.timeout)
	if results == None: return 1
	for file in results:
		file_path = os.path.join(args.cwd, file)
		# use treesitter to parse each file
		tree = ts_parse_file(args.language, file_path)
		if tree == None:
			print(f"[!] failed to parse file: {file}")
			continue
		for result in results[file]:
			# goto each of ripgrep's results and check if the location is a
			# 'definition' type node in tree sitter. if it is return the location.
			if ts_is_definition(tree, result['line_num']):
				ret.append(f"{file_path}:{result['line_num']}:{result['text']}")

	for r in ret: print(r) # is it ok?
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
