from typing import NamedTuple, Union, Generator, Iterable

class LoanBalance(NamedTuple):
    current_period: int
    current_balance: float
    last_payment: float

class LoanAmortization(object):    
    """Computes the balance and repayment schedule of loans and similar debts."""

    def __init__(self, term: int, interest: float, loan_amt: float, first_pmt_now:bool=False):
        """Constructors a LoanAmortization object. 
         + term (int) - the number of periods for the loan
         + interest (float) - the interest rate applied in each period of the term
         + loan_amt (float) - the initial balance of the loan
         + first_pmt_now (bool) - payment at beginning (True) or end (False) of period
        """
        self.__mutable = True
        self.term = term 
        self.interest = interest
        self.loan_amt = loan_amt
        self.first_pmt_now = first_pmt_now
        self.__mutable = False

    def __setattr__(self, name, value):
        if not hasattr(self, '_LoanAmortization__mutable') or self.__mutable:
            super.__setattr__(self, name, value)
        else:
            raise AttributeError("LoanAmortization is immutable, cannot set %s" % (name))            
                
    def amortize(self, current_balance: float=None, 
        current_period: int=0, pmts: Union[float, Iterable]=None) \
            -> Generator[LoanBalance, None, None]:
        """Performs an amortization projection.  
         + current_balance (float) - Remaining balance of loan. Defaults to initial_balance
            supplied in constructor.
         + pmts (float or Iterable) - schedule of payments to apply to loan.  Defaults to level
            payments implied by constructor arguments.
         + current_period (int) - if supplied, applies used to compute the number of remaining level_payments,
            IF pmts are not supplied.  Also provides starting time index to LoanBalance items returned.
        """ 
        remaining_loan_periods = self.term - current_period
        if pmts is not Iterable:
            pmts = [pmts if pmts is float else self.level_pmt] * remaining_loan_periods

        if current_balance is None:
            current_balance = self.loan_amt

        for current_pmt in pmts:                      
            if self.first_pmt_now:
                current_balance -= current_pmt
                current_balance *= (1 + self.interest)
            else:    
                current_balance *= (1 + self.interest)
                current_balance -= current_pmt

            current_period += 1
            yield LoanBalance(
                current_period = current_period,
                current_balance = current_balance,
                last_payment = current_pmt)        

    @property
    def level_pmt(self):
        """Computes the level payment implied by the parameters passed to the constructor"""
        disc_factor = pow(1 + self.interest, -1 * self.term)
        if self.interest == 0:
            annuity_factor = self.term
        else:
            annuity_factor = (1 - disc_factor) / self.interest
            if self.first_pmt_now == True:
                annuity_factor *= (1 + self.interest)
        return self.loan_amt / annuity_factor
