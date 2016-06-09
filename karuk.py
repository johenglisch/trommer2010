#! /usr/bin/env python3

"""Verb agreement in Karuk (Hokan; USA)."""

from trommer2010 import *


karuk = Language(name='Karuk', trans=True)

karuk.morphemes = [
    VI('-ap',  [['Acc', '+2', '+pl']])]

karuk.rules = [
    GenRule(['+pl'], [['Nom', '+3'], ['Acc', '+2']])]

print('Positive indicative')
draw_paradigm(karuk)

karuk.rules.extend([
    GenRule(['Acc', '+2'], [['Nom', '-1'], ['-3', '+pl']]),
    GenRule(['Acc', '+2'], [['Nom', '+3']])])

print('Negative')
draw_paradigm(karuk)


def derivation(s):
    karuk.realise_cell(parse_features(s), verbose=True)
