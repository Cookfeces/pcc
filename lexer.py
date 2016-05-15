#!/usr/bin/python
# -*- coding: UTF-8 -*-


class Tag:
    NUM = 256
    ID = 257
    TRUE = 258
    FALSE = 259


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

    def scan(self):
        while self.index < len(self.input):
            if self.peek() == ' ' or self.peek() == '\t':
                self.index += 1
                continue
            elif self.peek() == '\n':
                self.index += 1
                self.line += 1
            else:
                break
        if self.input[self.index].isdigit():
            num_start = self.index
            while self.index < len(self.input):
                if not(self.peek().isdigit()):
                    break
                else:
                    self.index += 1
            return Num(int(self.input[num_start:self.index]))
        if self.peek().isalpha():
            str_start = self.index
            while self.index < len(self.input):
                if not(self.peek().isalpha() or self.peek().isdigit):
                    break
                else:
                    self.index += 1
            str = self.input[str_start:self.index]
            if self.words.get(str) != None:
                return self.words.get(str)
            else:
                w = Word(Tag.ID, str)
                self.reserve(w)
                return w
        t = Token(ord(self.peek()))
        if self.index < len(self.input):
            self.index += 1
        return t

lexer = Lexer(" 821")
print(lexer.scan())
lexer2 = Lexer(" s821")
print(lexer2.scan())
lexer2 = Lexer(" #s821")
print(lexer2.scan())