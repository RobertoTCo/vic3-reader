from lark import Lark

from .lexicon import grammar, ToVic3

parser = Lark(grammar, parser="lalr", transformer=ToVic3(), lexer='contextual')

__all__ = ["parser",]