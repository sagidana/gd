from tree_sitter import Language, Parser


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
	global C_LANGUAGE
	global CPP_LANGUAGE
	global PY_LANGUAGE
	global JS_LANGUAGE
	global JAVA_LANGUAGE
	C_LANGUAGE = Language('build/my-languages.so', 'c')
	CPP_LANGUAGE = Language('build/my-languages.so', 'cpp')
	PY_LANGUAGE = Language('build/my-languages.so', 'python')
	JS_LANGUAGE = Language('build/my-languages.so', 'javascript')
	JAVA_LANGUAGE = Language('build/my-languages.so', 'java')
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

def ts_is_definition(tree, line_num):
	global parser_language
	if parser_language == 'c':
		query = C_LANGUAGE.query("""
			(function_declarator (identifier) @name)
			(preproc_function_def (identifier) @name)
			(preproc_def (identifier) @name)
			(type_definition (type_identifier) @name)
			(init_declarator (identifier) @name)
			""")
		captures = query.captures(  tree.root_node,
									start_point=[line_num -1, 0],
									end_point=[line_num+1 -1, 0])
		for capture, name in captures:
			if capture.start_point[0]+1 <= line_num <= capture.end_point[0]+1:
				return True
		return False
	if parser_language == 'cpp':
		return False
	if parser_language == 'python':
		query = PY_LANGUAGE.query("""
			(function_definition (identifier) @name)
			(class_definition (identifier) @name)
			""")
		captures = query.captures(  tree.root_node,
									start_point=[line_num -1, 0],
									end_point=[line_num+1 -1, 0])
		for capture, name in captures:
			if capture.start_point[0]+1 <= line_num <= capture.end_point[0]+1:
				return True
		return False
		return False
	if parser_language == 'javascript':
		return False
	if parser_language == 'java':
		return False
	return False

def ts_is_xref(tree, line_num):
	pass


