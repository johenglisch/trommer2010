"""trommer2010.py

This is an implementation of Trommer's (2010)[1] theory of Paradigmatic
Generalisation of Morphemes.

 [1] Trommer, Jochen (2010):  Paradigmatic Generalization of Morphemes.  In:
     Sebastian Bank, Doreen Georgi & Jochen Trommer (eds.), 2 in Agreement,
     Linguistische Arbeits Berichte 88.  Leipzig, University of Leipzig,
     227-246.

"""


from copy import deepcopy

__all__ = ['VI', 'GenRule', 'Language', 'parse_features']


def value(boolean):
    """Return binary feature value."""
    return '+' if boolean else '-'


def feature_structure(string, case, intr=False):
    """Convert person-number string to a single feature structure.

    Examples:

    >>> feature_structure('1s', 'Nom', True)
    ['Nom', '+1', '-2', '-3', '+sg', '-pl', '+intr']
    >>> feature_structure('2p', 'Abs', True)
    ['Abs', '-1', '+2', '-3', '-sg', '+pl', '+intr']
    >>> feature_structure('3d', 'Erg')
    ['Erg', '-1', '-2', '+3', '-sg', '-pl']
    >>> feature_structure('1pi', 'Nom')
    ['Nom', '+1', '+2', '-3', '-sg', '+pl']

    """
    first = '{}1'.format(value('1' in string))
    second = '{}2'.format(value('2' in string or 'i' in string))
    third = '{}3'.format(value('3' in string))
    sg = '{}sg'.format(value('s' in string))
    pl = '{}pl'.format(value('p' in string))

    struct = [case, first, second, third, sg, pl]
    if intr:
        struct.append('+intr')
    return struct


def parse_features(string, ergative=False):
    """Convert a person-number string into to a list of feature structures.

    Strings like 'EXT>INT' are considered transitive, whereas strings like 'ARG'
    are considered intranstive.

    Examples:

     * Default: nominative-accusative alignment

    >>> parse_features('1s>3s')
    [['Nom', '+1', '-2', '-3', '+sg', '-pl'], ['Acc', '-1', '-2', '+3', '+sg', '-pl']]
    >>> parse_features('1di')
    [['Nom', '+1', '+2', '-3', '-sg', '-pl', '+intr']]

     * Option: ergative-absolutive alignment

    >>> parse_features('1s>3s', ergative=True)
    [['Erg', '+1', '-2', '-3', '+sg', '-pl'], ['Abs', '-1', '-2', '+3', '+sg', '-pl']]
    >>> parse_features('1di', ergative=True)
    [['Abs', '+1', '+2', '-3', '-sg', '-pl', '+intr']]
    >>> parse_features('')
    []

    """
    if ergative:
        sarg = parg = 'Abs'
        aarg = 'Erg'
    else:
        sarg = aarg = 'Nom'
        parg = 'Acc'
    if not string:
        return list()
    args = string.split('>', 1)
    if len(args) == 1:
        return [feature_structure(string.lower(), sarg, True)]
    return [feature_structure(args[0].lower(), aarg),
            feature_structure(args[1].lower(), parg)]


def bundle_to_str(features):
    """Create string representation of a feature structure."""
    return '[{}]'.format(' '.join(features))

def feat_to_str(feature_sets):
    """Create string representation of a series of feature structures."""
    return '[{}]'.format(' '.join(map(bundle_to_str, feature_sets)))


def subsumes(paradigm_cell, morpheme):
    """Check if a vocabulary item subsumes the features in a paradigm cell.

    >>> cell = [['Nom', '+1', '-pl'], ['Acc', '+3', '-pl']]
    >>> subsumes(cell, [['+1', '-pl']])
    True
    >>> subsumes(cell, [['+3', '-pl']])
    True
    >>> subsumes(cell, [['+3'], ['+1']])
    True
    >>> subsumes(cell, [['+1', '+3']])
    False
    >>> subsumes(cell, [['+3'], ['+2']])
    False
    >>> subsumes([['+intr', '+1', '-2', '-3', '-sg', '+pl']],
    ...          [['+1', '+pl', '+intr']])
    True

    """
    for mstruct in morpheme:
        if not any(set(mstruct) <= set(pstruct) for pstruct in paradigm_cell):
            return False
    return True


def make_row(row, lens):
    """Create a single row for an ascii table."""
    cells = ('{row:<{len}}'.format(row=str(row[i]), len=lens[i])
             for i in range(len(row)))
    return '  {0}  '.format('  '.join(cells))


def make_table(array):
    """Create an ascii table from an array."""
    width = len(array[0])
    height = len(array)
    lens = [max(len(array[row][col]) for row in range(height))
            for col in range(width)]
    head = make_row(array[0], lens)
    dline = '=' * (len(head))
    sline = '-' * (len(head))
    table = [dline, head]
    if len(array) > 1:
        table.append(sline)
        table.extend(make_row(row, lens) for row in array[1:])
    table.append(dline)
    return '\n'.join(table)


class VI(object):
    """Representation of a Vocabulary Item."""

    def __init__(self, form, meaning):
        """Create a VI with a form (phonological representation) and a meaning
        (morpho-syntactic features)."""
        self.form = form
        self.meaning = meaning

    def __str__(self):
        """Return string representation of the VI."""
        return '/{phon}/: {cat}'.format(
            phon=self.form,
            cat=feat_to_str(self.meaning))

    def del_features(self, features, leftovers=None):
        """Delete features from the Vocabulary Item."""
        dset = set(features)
        self.meaning = [[feature for feature in fset if not feature in dset]
                        for fset in self.meaning]


class GenRule(object):
    """Representation of a Generalisation Rule."""

    def __init__(self, features, context, leftovers=None):
        """Create a generalisation rule."""
        self.leftovers = leftovers if leftovers is not None else list()
        self.features = features
        self.context = context

    def __str__(self):
        """Return string representation of a generalisation rule."""
        return '{features} \u2192 \u2205 / {context}'.format(
            features=bundle_to_str(self.features),
            context=feat_to_str(self.context))

    def apply(self, morpheme_list):
        """Apply the generalisation rule to a vocabulary item."""
        for morpheme in morpheme_list:
            morpheme.del_features(self.features, self.leftovers)


class Language(object):
    """Representation of a language."""

    def __init__(self, morphemes=None, rules=None, dual=False, inclusive=False,
                 transitive=False, ergative=False):
        """Create a language.

        morphemes:  List of vocabulary items of the language
        rules:      List of generalisation rules for the language

        dual:       Set to True if the language distinguishes dual
        inclusive:  Set to True if the language distinguishes 1st person incl.
        transitive: Set to True if the language shows object agreement
        ergative:   Set to True if the language uses Erg/Abs; False for Nom/Acc.

        """
        self.morphemes = morphemes if morphemes is not None else list()
        self.rules = rules if rules is not None else list()
        self.dual = dual
        self.inclusive = inclusive
        self.transitive = transitive

    def realise_cell(self, cell, verbose=False):
        """Insert a vi into a paradigm cell"""
        if verbose:
            print('Paradigm cell:', feat_to_str(cell))
            input()

        # step one: copy
        morphemes = deepcopy(self.morphemes)
        if verbose:
            print(' 1. Creating copy of the morpheme list')
            for index, vi in enumerate(morphemes):
                print('    %c. %s' % (chr(ord('a') + index), str(vi)))
            input()

        # step two: apply generalisation rules
        if verbose:
            print(' 2. Applying rules')
        for index, rule in enumerate(self.rules):
            if verbose:
                print('    %c. %s' % (chr(ord('a') + index), str(rule)))
            if subsumes(cell, rule.context):
                rule.apply(morphemes)
        if verbose:
            print()
            print('    new VI list')
            for index, vi in enumerate(morphemes):
                print('    %c. %s' % (chr(ord('a') + index), str(vi)))
            input()

        # step three: find matching vis for the paradigm cell
        if verbose:
            print(' 3. Finding Vocabulary Items')
        insertable = [vi for vi in morphemes if subsumes(cell, vi.meaning)]
        if verbose:
            for index, vi in enumerate(insertable):
                print('    %c. %s' % (chr(ord('a') + index), vi))
            input()
        return insertable

    def draw_paradigm(self, ergative=False):
        """Print the complete paradigm of a language."""
        persons = ['1', '1i', '2', '3']
        if not self.inclusive:
            del persons[1]
        numbers = ['s', 'd', 'p']
        if not self.dual:
            del numbers[1]
        subjects = ['%s%s' % (pers, num) for pers in persons for num in numbers
                    if not (pers == '1i' and num == 's')]
        if self.transitive:
            objects = subjects[::]
            pntable = list()
            for subj in subjects:
                row = [subj]
                for obj in objects:
                    if any(('1' in subj and '1' in obj,
                            '2' in subj and '2' in obj,
                            '2' in subj and 'i' in obj,
                            'i' in subj and '2' in obj)):
                        row.append('')
                    else:
                        row.append('%s>%s' % (subj, obj))
                pntable.append(row)
        else:
            pntable = [[subj] for subj in subjects]
        paradigm = [[self.realise_cell(parse_features(cell, ergative)) for cell in row]
                    for row in pntable]
        table = [['', 'intr']]
        if self.transitive:
            table[0].extend(subjects)
        table.extend([[subjects[i]] + [''.join(vi.form for vi in cell)
                                    for cell in row]
                    for i, row in enumerate(paradigm)])
        print(make_table(table))




if __name__ == '__main__':
    import doctest
    doctest.testmod()
