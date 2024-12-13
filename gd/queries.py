queries = {
    'python':{
        'is_definition':
            """
            (function_definition (identifier) @name)
            (class_definition (identifier) @name)
            """,
        'is_xref':
            """
            """
    },
    'c':{
        'is_definition':
            """
            (function_definition (function_declarator (identifier) @name))
            (preproc_function_def (identifier) @name)
            (preproc_def (identifier) @name)
            (type_definition (type_identifier) @name)
            (init_declarator (identifier) @name)
            (init_declarator (array_declarator (identifier) @name))
            (declaration (identifier) @name)
            """,
        'is_xref':
            """
            """
    },
    'java':{
        'is_definition':
            """
            (enum_declaration (identifier) @name)
            (method_declaration (identifier) @name)
            (class_declaration (identifier) @name)
            (field_declaration (variable_declarator (identifier) @name))
            """,
        'is_xref':
            """
            """
    }
}
