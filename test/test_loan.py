import unittest
from finlib.loan import LoanAmortization


class TestLoanAmortization(unittest.TestCase):

    def test_constructor(self):
        self.assertIsNotNone(LoanAmortization(12, 0.01, 1000))

    def test_immutable(self):
        amort = LoanAmortization(12, 0, 100)
        with self.assertRaises(AttributeError):
            amort.interest = 0.5

    def test_level_pmt_single_zero_int(self):
        amort = LoanAmortization(1, 0, 1000, True)
        self.assertAlmostEqual(amort.level_pmt, 1000)

    def test_level_pmt_multi_zero_int(self):
        amort = LoanAmortization(10, 0, 100)
        self.assertAlmostEquals(amort.level_pmt, 10)

    def test_level_pmt_single_nonzero_int(self):
        amort = LoanAmortization(1, 0.05, 100)
        self.assertAlmostEqual(amort.level_pmt, 105)

    def test_level_pmt_single_immediate_due(self):
        amort = LoanAmortization(1, 0.05, 100, True)
        self.assertAlmostEquals(amort.level_pmt, 100)

    def test_level_pmt_multi_nonzero_int(self):
        amort = LoanAmortization(36, 0.05, 10000)
        self.assertAlmostEqual(round(amort.level_pmt, 5), round(10000 / 16.54685171, 5))

    def test_level_pmt_multi_nonzero_int_due(self):
        amort = LoanAmortization(17, 0.012, 7431, first_pmt_now=True)
        self.assertAlmostEqual(round(amort.level_pmt, 5), round(7431 / 15.47911475, 5))

    def test_amort_balance_long_term(self):
        n_term = 250
        amort = LoanAmortization(n_term, 0.005, 10000)
        schedule = [x.current_balance for x in amort.amortize()]
        self.assertEqual(len(schedule), n_term)
        for x in schedule[0:(n_term - 1)]:
            self.assertGreater(x, 0)
        self.assertAlmostEqual(schedule[n_term - 1], 0.0)

    def test_amort_balance_short_term(self):
        expected_values = [9577.30092, 9133.466886,\
        8667.441151, 8178.114129, 7664.320755,\
        7124.837713, 6558.380519, 5963.600466,\
        5339.081409, 4683.3364, 3994.80414,\
        3271.845267, 2512.738451, 1715.676293,\
        878.7610284, 0]        
        rnd_exp_val = tuple(map(lambda x: round(x, 2), expected_values))
        amort = LoanAmortization(16, 0.05, 10000)
        rnd_act_val = tuple(map(lambda x: round(x.current_balance, 2), amort.amortize()))
        self.assertEqual(rnd_exp_val, rnd_act_val)
    
    def test_amort_balance_short_term_due(self):
        self.assertTrue(False)

    def test_amort_balance_pmts(self):
        self.assertTrue(False)

    def test_amort_nonzero_balance(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
