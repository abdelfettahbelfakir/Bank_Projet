from myapp.Models.accountModel import * 
from myapp.Dal.cnxDal import Database
from myapp.Dal.userDal import UserDao 

class AccountDao:
    def __init__(self) -> None:
        self.cnx = Database.get_connection()
        

    def create_account(self, balance: float,userID:int) -> int:
        query = """
        INSERT INTO saving_accounts (balance, interest_rate, userid) 
        VALUES (%s, %s, %s);
        """
        lst_user = UserDao().getusers()
        if((user['id'] == userID  and user['isadmin'] != 1 for user in lst_user)):# type: ignore
            if self.cnx is not None:
                cursor = self.cnx.cursor()
                cursor.execute(query, (balance, userID))
                self.cnx.commit()
                return cursor.lastrowid  # type: ignore 
        return -1

    def getAllAccounts(self) -> list[BankAccount]:
        accounts: list[BankAccount] = []
        query = "SELECT * FROM accounts;"
        if self.cnx is not None:
            cursor = self.cnx.cursor(dictionary=True) # type: ignore
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows: # type: ignore
                account=BankAccount(balance=row['balance']) # type: ignore
                account.account_id = row['id']   # type: ignore # Utiliser les bons attributs
                accounts.append(account)
        return accounts

    def getAccountById(self, id: int) -> BankAccount | None:
        query = "SELECT * FROM accounts WHERE id = %s;"
        if self.cnx is not None:
            cursor = self.cnx.cursor(dictionary=True) # type: ignore
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            if row:
                account = BankAccount(balance=row['balance']) # type: ignore
                account.account_id = row["id"] # type: ignore
                return account
        return None

    def update_balance(self, account_id: int, new_balance: float) -> None:
        query = "UPDATE accounts SET balance = %s WHERE id = %s;"
        if self.cnx is not None:
            cursor = self.cnx.cursor()
            cursor.execute(query, (new_balance, account_id))
            self.cnx.commit()
            
    def update_account(self, account_id: int, new_balance: float) -> None:
        query = "UPDATE accounts SET balance = %s, WHERE id = %s;"
        if self.cnx is not None:
            cursor = self.cnx.cursor()
            cursor.execute(query, (new_balance, account_id))  # Corrigé l'ordre des paramètres
            self.cnx.commit()
        

    def delete_account(self, account_id: int) -> None:
        query = "DELETE FROM accounts WHERE id = %s;"
        if self.cnx is not None:
            cursor = self.cnx.cursor()
            cursor.execute(query, (account_id,))
            self.cnx.commit()

    
    
            
            

class TransactionDao:
    def __init__(self) -> None:
        self.cnx = Database.get_connection()
        
    def create_transaction(self, account_id: int,  transaction_type: str, amount: float):
        """Créer une transaction."""
        query = """
                INSERT INTO transactions (account_id,  transaction_type, amount)
                VALUES (%s, %s, %s)
                """
        if self.cnx is not None:
            cursor = self.cnx.cursor()
            cursor.execute(query, (account_id, transaction_type, amount))
            self.cnx.commit()
            
    def transactionById(self, account_id: int):
        query = """
                SELECT * FROM transactions WHERE account_id = %s 
                """
        transactionss = []        
        if self.cnx is not None:
            cursor = self.cnx.cursor(dictionary=True) # type: ignore
            cursor.execute(query, (account_id,))
            
            transactions = cursor.fetchall()
            
            for transaction in transactions: # type: ignore
                transactionn = Transactions(id=transaction['id'], account_id=transaction['account_id'], transaction_type=transaction['transaction_type'], amount=transaction['amount'], transaction_date=transaction['transaction_date'])# type: ignore
                transactionss.append(transactionn)
        return transactionss       
                    
   
            

                   
if __name__ == "__main__":
    database:Database = Database()
    database.get_connection()
    account = AccountDao()
    print(account.getAllAccounts())   
        
             
            
