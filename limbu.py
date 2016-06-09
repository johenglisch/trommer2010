#! /usr/bin/env python3

"""Verb agreement in Limbu (Tibeto-Burman; Bhutan, India, Nepal)."""

from trommer2010 import *


limbu = Language(name='Limbu', trans=True, dual=True, incl=True)

limbu.morphemes = [
    VI('a-',  [['Abs', '+1'], ['+2'], ['-sg']])]

limbu.rules = [
    GenRule(['Abs'], [['Abs', '+3']])]

draw_paradigm(limbu, ergative=True)


def derivation(s):
    limbu.realise_cell(parse_features(s, ergative=True), verbose=True)
