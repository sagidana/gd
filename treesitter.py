from tree_sitter import Language, Parser
from os import path


C_LANGUAGE = None
CPP_LANGUAGE = None
PY_LANGUAGE = None
JS_LANGUAGE = None
JAVA_LANGUAGE = None

parser = None
parser_language = None

def ts_build_library():
	"""
	in order to build the treesitter .so we need to create a directory named
	'vendor' and git clone into that directory the following repos:
	- git clone https://github.com/tree-sitter/tree-sitter-c.git
	- git clone https://github.com/tree-sitter/tree-sitter-cpp.git
	- git clone https://github.com/tree-sitter/tree-sitter-python.git
	- git clone https://github.com/tree-sitter/tree-sitter-javascript.git
	- git clone https://github.com/tree-sitter/tree-sitter-java.git
	"""
	try:
		Language.build_library(
		  # Store the library in the `build` directory
		  'build/my-languages.so',

		  # Include one or more languages
		  [
		    'vendor/tree-sitter-c',
		    'vendor/tree-sitter-cpp',
		    'vendor/tree-sitter-python',
		    'vendor/tree-sitter-javascript',
		    'vendor/tree-sitter-java',
		  ]
		)
	except Exception as e:
		print(f"[!] Exception: {e}")
		return False
	return True

def ts_init(language=None):
	local_path = "/home/s/github/gd/"
	global C_LANGUAGE
	global CPP_LANGUAGE
	global PY_LANGUAGE
	global JS_LANGUAGE
	global JAVA_LANGUAGE
	C_LANGUAGE = Language(path.join(local_path, 'build/my-languages.so'), 'c')
	CPP_LANGUAGE = Language(path.join(local_path, 'build/my-languages.so'), 'cpp')
	PY_LANGUAGE = Language(path.join(local_path, 'build/my-languages.so'), 'python')
	JS_LANGUAGE = Language(path.join(local_path, 'build/my-languages.so'), 'javascript')
	JAVA_LANGUAGE = Language(path.join(local_path, 'build/my-languages.so'), 'java')
	if language: return ts_set_parser(language)
	return True

def ts_set_parser(language):
	global parser
	global parser_language
	try:
		parser = Parser()
		if language == 'c':
			parser_language = language
			parser.set_language(C_LANGUAGE)
			return True
		if language == 'cpp':
			parser_language = language
			parser.set_language(CPP_LANGUAGE)
			return True
		if language == 'python':
			parser_language = language
			parser.set_language(PY_LANGUAGE)
			return True
		if language == 'javascript':
			parser_language = language
			parser.set_language(JS_LANGUAGE)
			return True
		if language == 'java':
			parser_language = language
			parser.set_language(JAVA_LANGUAGE)
			return True
	except Exception as e:
		print(f"[!] Exception {e}")
		return False
	return False

def ts_parse_file(language, file_path):
	global parser
	global parser_language

	if parser_language != language:
		if not ts_set_parser(language): return None
	# the parser is ready for the file now..
	try:
		with open(file_path, 'rb') as f:
			tree = parser.parse(f.read())
	except Exception as e:
		print(f"[!] Exception: {e}")
		return None
	return tree

def ts_is_fit_query(query, tree, x, y):
	captures = query.captures(  tree.root_node,
								# start_point=[y, x],
								# end_point=[y, x])
								start_point=[y-1 if y > 0 else y, 0],
								end_point=[y+1, 0])
	for node, name in captures:
		start_y = node.start_point[0]
		start_x = node.start_point[1]
		end_y = node.end_point[0]
		end_x = node.end_point[1]
		if start_y > y: continue
		if end_y < y: continue
		if start_x > x: continue
		if end_x < x: continue
		return True
	return False

def ts_is_definition(tree, x, y):
	global parser_language
	if parser_language == 'c':
		query = C_LANGUAGE.query("""
			(function_declarator (identifier) @name)
			(preproc_function_def (identifier) @name)
			(preproc_def (identifier) @name)
			(type_definition (type_identifier) @name)
			(init_declarator (identifier) @name)
			(init_declarator (array_declarator (identifier) @name))
			(declaration (identifier) @name)
			""")
		return ts_is_fit_query(query, tree, x, y)
	if parser_language == 'cpp':
		return False
	if parser_language == 'python':
		query = PY_LANGUAGE.query("""
			(function_definition (identifier) @name)
			(class_definition (identifier) @name)
			""")
		return ts_is_fit_query(query, tree, x, y)
	if parser_language == 'javascript':
		return False
	if parser_language == 'java':
		return False
	return False

def ts_is_xref(tree, x, y):
	global parser_language
	if parser_language == 'c':
		query = C_LANGUAGE.query("""
			(function_declarator (identifier) @name)
			(preproc_function_def (identifier) @name)
			(preproc_def (identifier) @name)
			(type_definition (type_identifier) @name)
			(init_declarator (identifier) @name)
			""")
		return ts_is_fit_query(query, tree, x, y)
	if parser_language == 'cpp':
		return False
	if parser_language == 'python':
		query = PY_LANGUAGE.query("""
			(function_definition (identifier) @name)
			(class_definition (identifier) @name)
			""")
		return ts_is_fit_query(query, tree, x, y)
	if parser_language == 'javascript':
		return False
	if parser_language == 'java':
		return False
	return False


