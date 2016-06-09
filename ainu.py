#! /usr/bin/env python3

from trommer2010 import VI, GenRule, Language, draw_paradigm, feat


morphemes = [
    VI('en-',  [['Acc', '+1', '-pl']]),
    VI('un-',  [['Acc', '+1', '+pl']]),
    VI('eci-', [['+2', '+pl']]),
    VI('e-',   [['+2', '-pl'], ['+3']]),
    VI('ku-',  [['Nom', '+1', '-pl'], ['+3']]),
    VI('ci-',  [['Nom', '+1', '+pl'], ['Acc', '+3']]),
    VI('-as',  [['Nom', '+1', '+pl', '+intr']])]

rules = [
    GenRule(['+pl'], [['Nom', '+1'], ['Acc', '+2', '-pl']]),
    GenRule(['+3'],  [['Nom', '-3', '-pl', '+intr']])]

ainu = Language(morphemes, rules, 'Ainu', trans=True)

draw_paradigm(ainu)


def derivation(s):
    ainu.realise_cell(feat(s), verbose=True)