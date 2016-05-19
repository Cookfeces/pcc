#!/usr/bin/python
# -*- coding: UTF-8 -*-


class Tag:
    NUM = 256
    ID = 257
    TRUE = 258
    FALSE = 259
    REL = 260
    FLOAT = 261


#  无法错误异常类
class SyntaxException(BaseException):
    def __init__(self, arg="Syntax Error!"):
        self.error_message = arg


class Token:
    def __init__(self, t):
        self.tag = t


class Num(Token):
    def __init__(self, v):
        Token.__init__(self, Tag.NUM)
        self.value = v


class Word(Token):
    def __init__(self, t, s):
        Token.__init__(self, t)
        self.lexeme = s


class Rel(Token):
    def __init__(self, s):
        Token.__init__(self, Tag.REL)
        self.content = s


class Float(Token):
    def __init__(self, v):
        Token.__init__(self, Tag.FLOAT)
        self.value = v


class Lexer:
    index = 0
    line = 1
    words = dict()
    input = ""

    def reserve(self, t):
        self.words.setdefault(t.lexeme, t)

    def __init__(self, s):
        self.reserve(Word(Tag.TRUE, "true"))
        self.reserve(Word(Tag.FALSE, "false"))
        self.input = s

    def peek(self):
        return self.input[self.index]

    #  做词法分析,分析完之后index停留在返回词法的末尾
    def scan(self):
        #  跳过空字符串
        while self.index < len(self.input):
            if self.peek() == ' ' or self.peek() == '\t':
                self.index += 1
                continue
            elif self.peek() == '\n':
                self.index += 1
                self.line += 1
            else:
                break
        #  处理注释
        if self.peek() == '/':
            self.index += 1
            #  单行注释
            if self.peek() == '/':
                self.index += 1
                while self.index < len(self.input):
                    if self.peek() == '\n':
                        break
                    else:
                        self.index += 1
            #  多行注释
            elif self.peek() == '*':
                is_found = False
                self.index += 1
                while self.index < (len(self.input) - 1):
                    if self.peek() == '*':
                        self.index += 1
                        if self.peek() == '/':
                            is_found = True
                            break
                    else:
                        self.index += 1
                if not is_found:
                    raise SyntaxException("Cannot find the end of comment '*/'. ")
            else:
                raise SyntaxException()
        #  处理比较符号
        if self.peek() in "<=!>":
            rel_content = self.peek()
            if self.index < (len(self.input) - 1) and self.input[self.index+1] == "=":
                self.index += 1
                rel_content += self.peek()
            return Rel(rel_content)
        #  数字
        if self.peek().isdigit() or self.peek() == ".":
            num_start = self.index
            is_dot_exist = False
            while self.index < len(self.input):
                if self.peek() == ".":
                    if is_dot_exist:
                        self.index -= 1
                    else:
                        is_dot_exist = True
                if not(self.peek().isdigit() or self.peek() == "."):
                    break
                else:
                    self.index += 1
            if is_dot_exist:
                return Float(float(self.input[num_start:self.index]))
            else:
                return Num(int(self.input[num_start:self.index]))
        if self.peek().isalpha():
            str_start = self.index
            while self.index < len(self.input):
                if not(self.peek().isalpha() or self.peek().isdigit):
                    break
                else:
                    self.index += 1
            token_str = self.input[str_start:self.index]
            #  关键字
            if self.words.get(token_str) != None:
                return self.words.get(token_str)
            #  标识符
            else:
                w = Word(Tag.ID, token_str)
                self.reserve(w)
                return w
        t = Token(ord(self.peek()))
        if self.index < len(self.input):
            self.index += 1
        return t

lexer = Lexer(" 821")
print(lexer.scan())
lexer = Lexer(" s821")
print(lexer.scan())
lexer = Lexer(" #s821")
print(lexer.scan())
lexer = Lexer(" s821//dasd")
print(lexer.scan())
lexer = Lexer('//dasd\ns821')
print(lexer.scan())
lexer = Lexer("/**/")
print(lexer.scan())
lexer = Lexer("<=")
res = lexer.scan()
print(res, res.content)
lexer = Lexer(".1")
res = lexer.scan()
print(res, res.value)
