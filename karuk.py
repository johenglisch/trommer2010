#! /usr/bin/env python3

"""Verb agreement in Karuk (Hokan; USA)."""

from trommer2010 import *


morphemes = [
    VI('-ap',  [['Acc', '+2', '+pl']])]

rules = [
    GenRule(['+pl'], [['Nom', '+3'], ['Acc', '+2']])]


print('Positive indicative')

karuk = Language(morphemes, rules, transitive=True)
karuk.draw_paradigm()


print('Negative')

karuk.rules.extend([
    GenRule(['Acc', '+2'], [['Nom', '-1'], ['-3', '+pl']]),
    GenRule(['Acc', '+2'], [['Nom', '+3']])])
karuk.draw_paradigm()
