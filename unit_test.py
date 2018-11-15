#! encoding = utf-8

''' unit tests '''

import mylib
import unittest

class GenSearchSQLStr(unittest.TestCase):
    ''' Test gen_search_sql_str '''

    # Know input & output
    # (mol1, mol2, yr_start, yr_end, checked_lit_types)

    test_pairs = [
        (('', '', None, None, []), ("SELECT * FROM lit", [])),
        (('', '', None, None, ['MW']), ("SELECT * FROM lit WHERE lit_type in (?)", ['MW'])),
        (('', '', None, None, ['MW', 'IR', 'Theory']), ("SELECT * FROM lit WHERE lit_type in (?, ?, ?)", ['MW', 'IR', 'Theory'])),
        (('Ar', '', None, None, ['MW']), ("SELECT * FROM lit WHERE (mol1 = ? OR mol2 = ?) AND lit_type in (?)", ['Ar', 'Ar', 'MW'])),
        (('', 'Kr', None, None, ['MW']), ("SELECT * FROM lit WHERE (mol1 = ? OR mol2 = ?) AND lit_type in (?)", ['Kr', 'Kr', 'MW'])),
        (('Ar', 'H2O', None, None, ['MW']), ("SELECT * FROM lit WHERE (mol1 = ? AND mol2 = ?) OR (mol1 = ? AND mol2 = ?) AND lit_type in (?)", ['Ar', 'H2O', 'H2O', 'Ar', 'MW'])),
        (('', '', 1990, None, ['MW']), ("SELECT * FROM lit WHERE year >= ? AND lit_type in (?)", [1990, 'MW'])),
        (('', '', None, 2000, ['MW']), ("SELECT * FROM lit WHERE year <= ? AND lit_type in (?)", [2000, 'MW'])),
        (('', '', 1990, 2000, ['MW']), ("SELECT * FROM lit WHERE year >= ? AND year <= ? AND lit_type in (?)", [1990, 2000, 'MW'])),
        (('Ar', 'H2O', 1990, 2000, ['MW', 'IR']), ("SELECT * FROM lit WHERE (mol1 = ? AND mol2 = ?) OR (mol1 = ? AND mol2 = ?) AND year >= ? AND year <= ? AND lit_type in (?, ?)", ['Ar', 'H2O', 'H2O', 'Ar', 1990, 2000, 'MW', 'IR']))
    ]

    def test(self):

        print('\nTest search SQL option generator')

        for (i, j) in self.test_pairs:
            test_out = mylib.gen_search_sql_str(i)
            self.assertEqual(j, test_out)



if __name__ == '__main__':
    unittest.main()
