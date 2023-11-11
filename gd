#!/usr/bin/python
import argparse
import subprocess

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
		line_num = r[1]
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
	if args.symbol == None:
		print(f"the {ACTION_GOTO_DEFINITION} action require the symbol argument")
		return 1

	results = rg(args.symbol, cwd=args.cwd, timeout=args.timeout)
	if results == None: return 1
	for file in results:
		print(file)
		# for r in results[file]:
			# print(r)
	# ripgrep after the symbol
	# use treesitter to parse each file
	# goto each of ripgrep's results and check if the location is a
	# 'definition' type node in tree sitter. if it is return the location.
	return 0

def main():
	parser = argparse.ArgumentParser(description='gd utility')
	parser.add_argument('--action',
						choices=[
							ACTION_GOTO_DEFINITION,
							ACTION_XREFS,
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
	return 1

if __name__ == '__main__':
	exit(main())
