#!/usr/bin/python
import argparse


def main():
	parser = argparse.ArgumentParser(description='gd utility')
	parser.add_argument('--action',
						choices=[
							"goto-definition",
							"xrefs",
						],
						default='goto-definition',
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
	parser.add_argument('--symbol', help='the symbol we operating on')
	parser.add_argument('--symbol-location',   help='the symbol location we operating on, '
													'in the following format: '
													'<filepath>:<line_num>:<col_num>')
	args = parser.parse_args()

	print(args.language)
	print(args.cwd)
	print(args.action)
	print(args.symbol)
	print(args.symbol_location)

if __name__ == '__main__':
	main()
