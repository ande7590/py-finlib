from typing import NamedTuple, Union, Generator

PMT_TYPE = Union[float, list]
AMORT_TYPE = Generator[LoanBalance]

class LoanAmortization(object):    
    """Computes the balance and repayment schedule of loans and similar debts."""

    def __init__(self, term: int, interest: float, loan_amt: float, first_pmt_now:bool=False):
        self.__mutable = True
        self.term = term 
        self.interest = interest
        self.loan_amt = loan_amt
        self.ending_balance = ending_balance
        self.first_pmt_now = first_pmt_now
        self.__mutable = False

    def __setattr__(self, name, value):
        if self.__mutable:
            super.__setattr__(name, value)
        else:
            raise AttributeError("LoanAmortization is immutable, cannot set %s" % (name))            

    def amortization(self) -> AMORT_TYPE:
        """Performs a projection using the payment implied by the parameters 
        in the constructor, which results in zero ending balance (loan fully repaid)"""
        self.project_from_balance(self, self.loan_amt)

    def amortization_from_pmts(self, pmts: PMT_TYPE) -> AMORT_TYPE:
        """Performs a projection using a schedule of arbitrary payments."""        
        self.project_from_balance(self, self.loan_amt, current_period=0, pmts=pmts)
                
    def amortization_from_balance(self, current_balance: float, current_period: int=0, pmts: PMT_TYPE=None) -> AMORT_TYPE:
        """Performs a projection starting from the supplied balance.  The payment
        is assumed to be the level amount implied by the constructor."""        
        
        remaining_loan_periods = self.term - current_period
        
        if pmts is not list:
            pmts = [if pmts is float pmts else self.level_pmt] * remaining_loan_periods                

        while len(pmts) > 0:
            current_payment = pmts.pop(0)            
            current_balance *= (1 + self.interest)
            current_balance -= current_payment
            yield LoanBalance(current_period = self.term - len(pmts),
             current_balance = current_balance,
             last_payment = current_payment)
        
        raise StopIteration()
    
    @property
    def level_pmt(self):
        disc_factor = pow(self.interest, -1 * self.term)
        annuity_factor = (1 - disc_factor) / self.interest
        if self.first_pmt_now == False:
            annuity_factor *= (1 + self.interest)
        return annuity_factor


class LoanBalance(NamedTuple):
    current_period: int
    current_balance: float
    last_payment: float

