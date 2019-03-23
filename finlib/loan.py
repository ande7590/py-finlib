from typing import NamedTuple, Union, Generator

class LoanBalance(NamedTuple):
    current_period: int
    current_balance: float
    last_payment: float

class LoanAmortization(object):    
    """Computes the balance and repayment schedule of loans and similar debts."""

    def __init__(self, term: int, interest: float, loan_amt: float, first_pmt_now:bool=False):
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

    def amortization(self) -> Generator[LoanBalance, None, None]:
        """Performs a projection using the payment implied by the parameters 
        in the constructor, which results in zero ending balance (loan fully repaid)"""
        return self.amortization_from_pmts(self.level_pmt)

    def amortization_from_pmts(self, pmts: Union[float, list]) \
            -> Generator[LoanBalance, None, None]:
        """Performs a projection using a schedule of arbitrary payments."""        
        return self.amortization_from_balance(self.loan_amt, 0, pmts)
                
    def amortization_from_balance(self, current_balance: float, 
        current_period: int=0, pmts: Union[float, list]=None) \
            -> Generator[LoanBalance, None, None]:
        """Performs a projection starting from the supplied balance and utilizing the pmts"""        
        
        remaining_loan_periods = self.term - current_period
        if pmts is not list:
            pmts = [pmts if pmts is float else self.level_pmt] * remaining_loan_periods

        while len(pmts) > 0:
            current_payment = pmts.pop(0)            
            current_balance *= (1 + self.interest)
            current_balance -= current_payment
            yield LoanBalance(
                current_period = self.term - len(pmts),
                current_balance = current_balance,
                last_payment = current_payment)        

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
