from lark import Transformer, Tree

grammar = r"""
    // ─── Primitives ──────────────────────────────────────────────────────────
    FILE_CODE.2   : /SAV[0-9A-Za-z]+/               // If save plain text keeps the compiling format

    DATE   : /\d+\.\d+\.\d+(?:\.\d+)*/              // i.e 1836.1.1.6
    FLOAT  : /[+-]?\d+\.\d+/
    //CNAME_DOT_INT: /[A-Za-z_][\w\-]*\.\d+/
    CNAME_DOT: /[A-Za-z_][\w\-]*\.[\w\-]+/          // i.e utopian.1, pb_shield_pattern_00.dds
    INT    : /[+-]?\d+/
    CNAME  : /[A-Za-z_][\w\-]*/

    %import common.ESCAPED_STRING
    %import common.WS
    %ignore WS

    %declare _NEWLINE

    // ─── Grammar ─────────────────────────────────────────────────────────
    start: file_code? pair+

    file_code: FILE_CODE            -> file_code

    pair : (CNAME | INT | ESCAPED_STRING) "=" value    -> key_value

    ?value: primitive
        | rgb_call                  -> rgb_value
        | set

    // ─────── Structures ─────────────────────────────────────────────────────
    rgb_call: "rgb" set3
    set3: "{" INT INT INT "}"

    set: "{" item* "}"              -> set_handler
    ?item: pair                     -> elem_pair
        | primitive                 -> elem_prim
        | set                       -> elem_set

    ?primitive: ESCAPED_STRING      -> escaped_str_val
           | CNAME_DOT              -> return_val
           | DATE                   -> return_val
           | FLOAT                  -> float_val
           | INT                    -> int_val
           | CNAME                  -> return_val
    """

class ToVic3(Transformer):
    # ─── Composites ──────────────────────────────────────────────────────────
    def start(self, items):
        return items
    
    def file_code(self, items):
        return ("file coding", items[0])
    
    def key_value(self, items):
        key = str(items[0])
        val = items[1]
        return (key, val)

    def elem_pair(self, items):
        return items[0]

    def elem_prim(self, items):
        return items[0]

    def elem_set(self, items):
        return items[0]

    def set_handler(self, items):
        if all(isinstance(i, tuple) for i in items):
            return dict(items)
        return items

    def rgb_value(self, items):
        # items[0] is Tree("rgb_call", [Tree("set3", [Token(INT,...), ...])])
        rgb_tree = items[0]
        # rgb_call contains set3
        r, g, b = map(int, rgb_tree.children[0].children)
        return {'rgb': {'r': r, 'g': g, 'b': b}}

    def set3(self, items):
        # Wrap raw ints in a Tree so rgb_call always receives a consistent Tree
        return Tree('set3', items)
    

    # ─── Primitives ──────────────────────────────────────────────────────────

    def escaped_str_val(self, s):
        # removes quotes ""
        return s[0][1:-1]

    def float_val(self, s):
        return float(s[0])

    def int_val(self, s):
        return int(s[0])
    
    def return_val(self, s):
        return s[0]
