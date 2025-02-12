from abc import ABC, abstractmethod
from sqlite3 import Date
from typing import Final

from dataclasses import dataclass

class BankAccount(ABC):
    
    def __init__(self, balance: float = 0.0) -> None:
        self.balance = balance
        self.account_id = None
    
    def deposit(self, amount: float) -> float:
        self.balance += amount
        return self.balance  
    
    @abstractmethod
    def withdraw(self, amount: float) -> float:
        if self.balance - amount >= 0: # type: ignore
            self.balance -= amount # type: ignore
            return amount
    
    def transfer(self, amount: float, other: 'BankAccount') -> float:
        withdraw_amount = self.withdraw(amount)
        other.deposit(amount)
        return self.balance  # Retourner le solde actuel après transfert

    
@dataclass
class Transactions:
    id:int
    account_id:int
    transaction_type:str
    amount:float
    transaction_date:Date   
    
    
