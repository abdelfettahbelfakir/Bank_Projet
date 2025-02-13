from flask import (Flask, Response,
                   request,
                   render_template,
                   jsonify,
                   abort,
                   session,
                   redirect,
                   url_for,
                   send_file,
                   after_this_request,
                   Blueprint
                   )

bankaccount=Blueprint('bankaccount',__name__)
from myapp.Models.accountModel import *
from myapp.Services.accountServices import *
account_dao:AccountService = AccountService()
from datetime import datetime
import os

@bankaccount.route('/create_account', methods=['POST'])
def create_account():
    balance = request.form['balance']
    userID = request.form['userID']
    if(account_dao.create_account(float(balance),int(userID))!= -1):
        return redirect(url_for('bankaccount.get_all_accounts'))
    return "Erreur lors de la création du compte", 400
@bankaccount.route('/accounts', methods=['GET'])
def get_all_accounts():
    
    accounts = account_dao.getAllAccounts()
    return render_template('accounts.html',accounts=accounts)


@bankaccount.route('/get_account', methods=['GET'])
def get_account():
    account_id = request.args.get('account_id')
    if account_id:
        try:
            account_id = int(account_id)
            account = account_dao.getAccount(account_id)
            if account:
                return render_template('accounts.html', accounts=[account])
            else:
                return render_template('accounts.html', error="Aucun compte trouvé avec cet ID.")
        except ValueError:
            return render_template('accounts.html', error="ID invalide.")
    return render_template('accounts.html', error="Veuillez fournir un ID de compte.")

@bankaccount.route('/edit_account', methods=['POST'])
def edit_account():
    account_id = request.form['account_id']
    new_balance = float(request.form['balance'])
    
    account_dao.update_account_balance(int(account_id), new_balance)

    return redirect(url_for('bankaccount.get_all_accounts'))

@bankaccount.route('/delete_account/<int:account_id>', methods=['POST'])
def delete_account(account_id):
    account_dao.delete_account(account_id)
    return redirect(url_for('bankaccount.get_all_accounts'))  # Redirection vers la liste des comptes 

@bankaccount.route('/log_account', methods=['POST'])
def log_account():
    try:
        account_id = int(request.form['account_id'])
        accounts = account_dao.log_account(account_id)
        print(accounts)
        return render_template('transactions_log.html', transactions=accounts)
    except ValueError:
        return "Invalid account ID provided", 400

@bankaccount.route('/deposit', methods=['POST'])
def deposit():
    account_id = int(request.form['account_id'])
    amount = float(request.form['amount'])
    account_dao.deposit(account_id, amount)
    return redirect(url_for('bankaccount.get_all_accounts'))

@bankaccount.route('/withdraw', methods=['POST'])
def withdraw():
    account_id = int(request.form['account_id'])
    amount = float(request.form['amount'])
    account_dao.withdraw(account_id, amount)
    return redirect(url_for('bankaccount.get_all_accounts'))

@bankaccount.route('/transfer', methods=['POST'])
def transfer():
    account_id = int(request.form['account_id'])
    amount = float(request.form['amount'])
    recipient_account = int(request.form['recipient_account'])
    account_dao.transfer(account_id, recipient_account, amount)
    return redirect(url_for('bankaccount.get_all_accounts'))


import pandas as pd
from matplotlib import pyplot as plt
from io import BytesIO
import matplotlib

@bankaccount.route('/dashboard', methods=['GET'])
def dashboard():
    transactions = account_dao.log_account(1)
    df = pd.DataFrame(transactions)
    df[['transaction_type','amount']].plot(kind='line')
    img=BytesIO()
    
    plt.savefig(img,format='png')
    img.seek(0)
    return Response(img,content_type='image/png')
    #return render_template('dashboard.html', table_data=df.to_html(classes='table table-striped', index=False))
    











