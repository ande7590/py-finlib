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
        expected_values = [9671.289027,9336.003835,8994.01294,
        8645.182226,8289.374898,7926.451423,7556.269479,
        7178.683896,6793.546602,6400.706561,6000.00972,
        5591.298942,5174.413948,4749.191255,4315.464107,
        3873.062417,3421.812692,2961.537974,2492.057761,
        2013.187943,1524.74073,1026.524572,518.3440907,0.0]
        rnd_exp_val = tuple(map(lambda x: round(x, 2), expected_values))
        amort = LoanAmortization(24, 0.02, 10000, first_pmt_now=True)
        rnd_act_val = tuple(map(lambda x: round(x.current_balance, 2), amort.amortize()))
        self.assertEqual(rnd_exp_val, rnd_act_val)

    def test_amort_balance_pmts(self):
        # setup payment to feed into amortization
        pmts = [528.7109725,0,528.7109725,0,
        528.7109725,0,0,0,1321.777431,
        528.7109725,1586.132918,528.7109725,
        2643.554863,3741.898681,528.7109725]
        # create a rounded payments for the "expected" amounts
        expected_pmts = tuple(map(
            lambda x: round(x, 2), pmts))
        # create a rounded balance for the "expected" amounts
        expected_bals = [9671.289027,
        9864.714808,9533.298132,9723.964094,
        9389.732404,9577.527052,9769.077593,
        9964.459145,8841.970896,8490.099342,
        7073.768411,6686.532806,4176.7086,
        518.3440907,0]
        expected_bals = tuple(map(
            lambda x: round(x, 2), expected_bals))
        # initialize object w/ paramters
        amort = LoanAmortization(24, 0.02, 10000)
        # run 
        amort_schedule = tuple(amort.amortize(pmts=pmts))
        actual_bals = tuple(map(
            lambda x: round(x.current_balance, 2),
            amort_schedule))
        actual_pmts = tuple(map(
            lambda x: round(x.last_payment, 2),
            amort_schedule))

        
        # verify that actuals are equal to expected
        self.assertCountEqual(expected_pmts, actual_pmts)
        self.assertTupleEqual(expected_pmts, actual_pmts)
        self.assertCountEqual(expected_bals, actual_bals)
        self.assertTupleEqual(expected_bals, actual_bals)

    def test_amort_nonzero_balance(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
