#! /usr/bin/env python3

"""Verb agreement in Kulung (Tibeto-Burman; Nepal)."""

from trommer2010 import *


morphemes = [
    VI('-o',  [['Abs', '+1', '+sg']]),
    VI('-na', [['Erg', '+1', '+sg'], ['Abs', '-1', '+2', '-pl']]),
    VI('-n',  [['Abs', '-1', '+2', '+pl']]),
    VI('-c',  [['Abs', '-3', '-sg', '-pl']]),
    VI('-i',  [['Abs', '-3', '-sg']]),
    VI('-u',  [['Erg', '-3', '-sg'], ['Abs', '+3']]),
    VI('-am', [['Erg', '-3', '+pl'], ['Abs', '+3']]),
    VI('-ka', [['Abs', '+1', '-2', '-sg']])]

rules = [
    GenRule(['Abs'], [['Abs', '+1', '+sg']]),
    GenRule(['Abs'], [['Abs', '+3']]),
    GenRule(['-3'],  [['Erg', '+3'], ['Abs', '+3']]),
    GenRule(['-3'],  [['Erg', '+sg'], ['Abs', '+3']]),
    GenRule(['-pl'], [['Erg', '+3'], ['Abs', '+3']]),
    GenRule(['-pl'], [['Erg', '+sg'], ['Abs', '+3']])]


print('Paradigm with predicted ranges.')

kulung = Language(
    morphemes, dual=True, inclusive=True, transitive=True, ergative=True)
kulung.draw_paradigm()


print('Paradigm with actual ranges.')

kulung.rules = rules
kulung.draw_paradigm()
