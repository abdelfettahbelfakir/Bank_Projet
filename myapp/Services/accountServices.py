from myapp.Dal.accountsDal import *



class AccountService:
    def __init__(self) -> None:
        self.dao = AccountDao()
        self.transaction_dao = TransactionDao()

    def create_account(self, balance: float,userID:int) -> int:
        """Créer un compte d'épargne."""
        if balance < 100:
            raise ValueError("Le solde doit être supérieur ou égal à 100.")
        
        account_id = self.dao.create_account(balance,userID)
            
        return account_id
    
    def getAllAccounts(self) -> list[BankAccount]:
        
    
        accounts = self.dao.getAllAccounts()
        if accounts:
                return accounts
        else:
                print("No saving accounts found.")
                return []
        
    
    
    def getAccount(self, account_id: int) -> BankAccount | None:
        
            account = self.dao.getAccountById(account_id)
            if account:
                return account
            else:
                print(f" account with ID {account_id} not found.")
                return None
        
        
    def update_account_balance(self, account_id: int, new_balance: float) -> None:
        if new_balance < 0:
            raise ValueError("Le solde doit être positif.")
        
        self.dao.update_account(account_id, new_balance) 
        
    def delete_account(self, account_id: int) -> None:
        self.dao.delete_account(account_id)     

    def deposit(self, account_id: int, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Le montant du dépôt doit être supérieur à 0.")
        
        account = self.dao.getAccountById(account_id)
        if not account:
            raise ValueError("Compte  introuvable.")
        
        new_balance = account.deposit(amount)
        
        self.dao.update_balance(account_id, new_balance)
        
        self.transaction_dao.create_transaction(
            account_id=account_id,
            transaction_type='Deposit',
            amount = amount
        )
        
        return new_balance

    def withdraw(self, account_id: int, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Le montant du retrait doit être supérieur à 0.")
        
        account = self.dao.getAccountById(account_id)
        if not account:
            raise ValueError("Compte d'épargne introuvable.")
        
        new_balance = account.withdraw(amount)
        
        self.dao.update_balance(account_id, new_balance)
        
        self.transaction_dao.create_transaction(
            account_id=account_id,
            transaction_type='Withdraw',
            amount= amount
        )
        
        return new_balance
    
    def transfer(self, source_account_id: int, target_account_id: int, amount: float):
        
        if amount <= 0:
            raise ValueError("Le montant du transfert doit être supérieur à 0.")
        
        source_account = self.dao.getAccountById(source_account_id)
        target_account = self.dao.getAccountById(target_account_id)
        
        if not source_account:
            raise ValueError("Compte source  introuvable.")
        
        if not target_account:
            raise ValueError("Compte destinataire  introuvable.")
        
        
        source_account.transfer(amount,target_account)
        print("from services",amount)
        self.dao.update_balance(source_account_id, source_account.balance)
        self.dao.update_balance(target_account_id, target_account.balance)
        
        self.transaction_dao.create_transaction(
            account_id=source_account_id,
            transaction_type='Transfer Sortie',
            amount=amount
        )
        
        self.transaction_dao.create_transaction(
            account_id=target_account_id,
            transaction_type='Transfer Entree',
            amount=amount
        )
        


    
    
    def log_account(self, account_id:int)->list:
        try:
            accounts = self.transaction_dao.transactionById(account_id)
            return accounts
        except Exception as e:
            print(f"Error fetching checking accounts: {e}")
            return []


    
    

        
