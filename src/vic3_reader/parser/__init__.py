from lark import Lark

from vic3_reader.parser.lexicon import grammar, ToVic3

parser = Lark(grammar, parser="lalr", transformer=ToVic3(), lexer='contextual')

__all__ = ["parser",]