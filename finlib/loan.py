from typing import NamedTuple, Union, Generator, Iterable
from math import log, ceil

class LoanBalance(NamedTuple):
    current_balance: float
    last_payment: float

class LoanAmortization(object):    
    """Amortizes a loan.  Specify loan parameters in constructor. Generate
     the amortization schedule via the amortize() method.
     + term - length of loan term
     + interest - interest applied in each period of term
     + loan_amt - total loan balance at start
     + pmt_beg_term - Annuity immediate (False) or annuity due (True)
     """

    def __init__(self, term: int, interest: float, loan_amt: float, pmt_beg_term:bool=False):
        self.__mutable = True
        self.term = term 
        self.interest = interest
        self.loan_amt = loan_amt
        self.pmt_beg_term = pmt_beg_term
        self.__mutable = False

    def __setattr__(self, name, value):
        if not hasattr(self, '_LoanAmortization__mutable') or self.__mutable:
            super.__setattr__(self, name, value)
        else:
            raise AttributeError("LoanAmortization is immutable, cannot set %s" % (name))            
                
    def amortize(self, current_balance: float=None, pmts: Iterable=None)\
            -> Generator[LoanBalance, None, None]:
        """Performs an amortization projection:
        + pmts - Schedule of payments to apply to loan.  Defaults to level payments implied by constructor arguments.
        + current_balance - Remaining loan balance.  Defaults to loan_amt (constructor arg).
        """

        # No params, apply default amortization
        if current_balance is None and pmts is None:
            current_balance = self.loan_amt
            pmts = [self.level_pmt] * self.term 
        # Current balance greater than zero, amortize using original pmts
        # and solve for the number of remaining payments
        elif current_balance is float and current_balance > 0.0 and pmts is None:
            i = self.interest
            v = pow(1+i, -1)
            int_fctr = i/(1+i) if self.pmt_beg_term else i
            num_pmts = log(int_fctr * (current_balance/self.level_pmt) - 1) / log(v)
            pmts = [self.level_pmt] * ceil(num_pmts)
        # if the payments are specified, use the current_balance if supplied, otherwise
        # use the initial loan balance
        elif isinstance(pmts, Iterable):
            current_balance = self.loan_amt if current_balance is None else current_balance
        # Check if the pmts is appropriate type
        elif not isinstance(pmts, Iterable):
            raise TypeError("pmts must be None, float, or Iterable, got %s" % type(pmts))

        # Check if balance is appropriate value
        if current_balance <= 0.0:
            raise TypeError("current_balance must be STRICTLY positive (non-zero) float")

        # run the amortization
        for current_pmt in pmts:                      
            if self.pmt_beg_term:
                # annuity due
                current_balance -= current_pmt
                current_balance *= (1 + self.interest)
            else:
                # annuity immediate
                current_balance *= (1 + self.interest)
                current_balance -= current_pmt
            
            # do not allow negative loan balances
            floored_balance = max(current_balance, 0.0)
            
            # lower the payment if there is an "overpayment" (negative loan balance) 
            last_payment = current_pmt - (floored_balance - current_balance)
            
            yield LoanBalance(
                current_balance = floored_balance,
                last_payment = last_payment)

    @property
    def level_pmt(self):
        """Computes the level payment implied by the parameters passed to the constructor"""
        disc_factor = pow(1 + self.interest, -1 * self.term)
        if self.interest == 0:
            annuity_factor = self.term
        else:
            annuity_factor = (1 - disc_factor) / self.interest
            if self.pmt_beg_term == True:
                annuity_factor *= (1 + self.interest)
        return self.loan_amt / annuity_factor
