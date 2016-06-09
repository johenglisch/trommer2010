#! /usr/bin/env python3

"""Verb agreement in Limbu (Tibeto-Burman; Bhutan, India, Nepal)."""

from trommer2010 import *


morphemes = [
    VI('a-',  [['Abs', '+1'], ['+2'], ['-sg']])]

rules = [
    GenRule(['Abs'], [['Abs', '+3']])]


limbu = Language(
    morphemes, rules, dual=True, inclusive=True, transitive=True, ergative=True)
limbu.draw_paradigm()
