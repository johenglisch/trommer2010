#! /usr/bin/env python3

from trommer2010 import VI, GenRule, Language, draw_paradigm, feat


limbu = Language(name='Limbu', trans=True, dual=True, incl=True)

limbu.morphemes = [VI('a-',  [['Abs', '+1'], ['+2'], ['-sg']])]

limbu.rules = [GenRule(['Abs'], [['Abs', '+3']])]

draw_paradigm(limbu, ergative=True)


def derivation(s):
    limbu.realise_cell(feat(s, ergative=True), verbose=True)
