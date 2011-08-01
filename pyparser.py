#!/usr/bin/python2.6.5

'''
Parser stuff for query evaluation
taken from the pyparsing's wiki and modified heavily :)
'''

from pyparsing import *


class UnaryOperation(object):
    def __init__(self, t):
        self.op, self.a = t[0]


class BinaryOperation(object):
    def __init__(self, t):
            self.op = t[0][1]
            self.operands = t[0][0::2]
          
class SearchAnd(BinaryOperation):
    def generateSetExpression(self):
        expr = ""
        for oper in self.operands:
            if isinstance(oper, SearchTerm): expr += "\"" + str(oper) + "\"," 
            else: expr += str(oper) + ","
        return "self.intersect([%s])" % expr[:-1]#(",".join(str(oper) for oper in self.operands))
    def __repr__(self):
        expr = ""
        for oper in self.operands:
            if isinstance(oper, SearchTerm): expr += "\"" + str(oper) + "\"," 
            else: expr += str(oper) + ","
        return "self.intersect([%s])" % expr[:-1]#(",".join(str(oper) for oper in self.operands))
    

class SearchOr(BinaryOperation):
    def generateSetExpression(self):
        expr = ""
        for oper in self.operands:
            if isinstance(oper, SearchTerm): expr += "\"" + str(oper) + "\"," 
            else: expr += str(oper) + ","
        return "self.union([%s])" % expr[:-1]#(",".join(str(oper) for oper in self.operands))
    def __repr__(self):
        expr = ""
        for oper in self.operands:
            if isinstance(oper, SearchTerm): expr += "\"" + str(oper) + "\"," 
            else: expr += str(oper) + ","
        return "self.union([%s])" % expr[:-1]#(",".join(str(oper) for oper in self.operands))

class SearchNot(UnaryOperation):
    def generateSetExpression(self):
        if isinstance(self.a, SearchTerm): return "self.diff(\"%s\")" % str(self.a)
        else: return "self.diff(%s)" % str(self.a)
    
    def __repr__(self):
        if isinstance(self.a, SearchTerm): return "self.diff(\"%s\")" % str(self.a)
        else: return "self.diff(%s)" % str(self.a)

class SearchTerm(object):
    def __init__(self, tokens):
        self.term = tokens[0]
    def generateSetExpression(self):
        return "%s" % self.term

    def __repr__(self):
        return self.term



# define the grammar
and_ = CaselessLiteral("and")
or_ = CaselessLiteral("or")
not_ = CaselessLiteral("not")
searchTerm = Word(alphas) | quotedString.setParseAction( removeQuotes )
searchTerm.setParseAction(SearchTerm)
searchExpr = operatorPrecedence( searchTerm,
[
(not_, 1, opAssoc.RIGHT, SearchNot),
(and_, 2, opAssoc.LEFT, SearchAnd),
(or_, 2, opAssoc.LEFT, SearchOr),
])