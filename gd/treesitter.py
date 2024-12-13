from tree_sitter_language_pack import(get_binding,
                                      get_language,
                                      get_parser)
import tree_sitter
import subprocess
import json

from .queries import queries

def rg(pattern, cwd=None, timeout=None):
    raw_result = None
    try:
        raw_result = subprocess.run(['rg',
                                     '--vimgrep',
                                     '-g', '!tags',
                                     '-g', '!*.gcov',
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


class TS:
    def __init__(self, language):
        if language not in (
            'python',
            ):
            raise Exception("language is not supported by TS")
        self._language = language
        self.language = get_language(language)
        self.parser = get_parser(language)

    def _create_query(self, query):
        assert isinstance(query, str)
        return self.language.query(query)

    def get_tree(self, path):
        file_bytes = open(path, 'rb').read()
        tree = self.parser.parse(file_bytes)
        return tree.root_node

    def enumerate_query(self, tree, query, range=None):
        assert isinstance(query, str)
        assert isinstance(tree, tree_sitter.Node)
        assert isinstance(range, (type(None), tuple))

        _query = self._create_query(query)
        if range is not None: _query.set_point_range(range)
        captures = _query.captures(tree)

        for scope in captures:
            for node in captures[scope]:
                yield node, scope

    def get_only_node(self, tree, query, range=None):
        assert isinstance(query, str)
        assert isinstance(tree, tree_sitter.Node)
        assert isinstance(range, (type(None), tuple))

        _query = self._create_query(query)
        if range is not None: _query.set_point_range(range)
        captures = _query.captures(tree)
        assert len(captures.keys()) == 1
        for scope in captures:
            nodes = captures[scope]
            assert len(nodes) == 1
            return captures[scope][0]

    def get_relevant_node(self, tree, query, range=None):
        assert isinstance(query, str)
        assert isinstance(tree, tree_sitter.Node)
        assert isinstance(range, (type(None), tuple))
        _query = self._create_query(query)
        if range is not None: _query.set_point_range(range)
        captures = _query.captures(tree)
        for scope in captures:
            for node in captures[scope]:
                return node
        return None

    def is_definition(self, tree, range=None):
        assert isinstance(tree, tree_sitter.Node)
        assert isinstance(range, (type(None), tuple))
        query = queries[self._language].get('is_definition', None)
        assert query is not None
        node = self.get_relevant_node(tree, query, range)
        return node is not None


def test():
    ts = TS('python')

    # test 3
    results = rg("test")
    for path in results:
        tree = ts.get_tree(path)
        for find in results[path]:
            y = find['y']
            is_definition =  ts.is_definition(
                    tree,
                    ((y-1 if y>0 else y, 0), (y+1, 0))
                )
            print(f"{is_definition} -> {find}")

    # # test 2
    # results = rg("test")
    # for path in results:
        # tree = ts.get_tree(path)
        # for find in results[path]:
            # y = find['y']
            # node =  ts.get_relevant_node(
                    # tree,
                    # """
                    # (function_definition (identifier) @id)
                    # """,
                    # ((y-1 if y>0 else y, 0), (y+1, 0))
                # )
            # print(f"{node} -> {find}")

    # # test 3
    # tree = ts.get_tree('gd/treesitter.py')
    # node = ts.get_only_node(tree,
        # """
        # (
         # (function_definition) @function
         # (#match? @function "test")
        # )
        # """
    # )
    # print(node)

    # results = ts.enumerate_query(tree,
        # """
        # (
         # (function_definition) @function
         # (#match? @function "test")
        # )
        # """
    # )
    # for node, scope in results:
        # print(scope)

if __name__=="__main__":
    test()
