from Database import connect_to_database
import string
import hashlib
import random

#encrypt and varify pin
def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

def verify_pin(input_pin, stored_hash):
    return hash_pin(input_pin) == stored_hash


#db tables initialize
def initilize_tables():
    connection = connect_to_database()
    if not connection:
        return False
    try:
        cursor = connection.cursor()
        
        create_account_table = '''
        create table if not exists accounts(
            account_number varchar(50) primary key,
            name varchar(100) not null,
            pin varchar(64) not null,
            balance decimal(15,2) default 0.00,
            create_at timestamp default CURRENT_TIMESTAMP
        );
        '''
        create_audit_table = '''
        create table if not exists audit(
            id serial primary key,
            account_number varchar(50),
            holder_name varchar(100),
            action varchar(100) not null,
            amount decimal(15,2) default 0.00,
            time_stamp timestamp default CURRENT_TIMESTAMP,
            foreign key (account_number) references accounts(account_number)
        );
        '''
        cursor.execute(create_account_table)
        cursor.execute(create_audit_table)
        connection.commit()
        cursor.close()
        return True
        
        
    except Exception as e:
        print(f'Error occured while intilizing table {e}')
        return False

#account class
class Account:
    def __init__(self, name="",pin="",account_number=""):
        self.__account_number = (
            account_number if account_number else  self.__generate_account_number()           
        )
        self.__name = name
        self.__pin =hash_pin(pin)
        self.__balance = 0.0
        
    @staticmethod
    def __generate_account_number():
        return "".join(random.choices(string.ascii_uppercase+string.digits,k=10))  
    
    #getters
    def get_account_number(self):
        return self.__account_number
    def get_name(self):
        return self.__name  
    def get_pin_hash(self):
        return self.__pin
    def get_balance(self):
        return self.__balance
    
    #setters
    
    def set_name(self,name):
        self.__name = name  
    def set_pin_hash(self,pin_hash):
        self.__pin = pin_hash
    def set_pin(self, pin):
        self.__pin= hash_pin(pin)
    def set_balance(self,balance):
        self.__balance = balance
    
    #utility
    def deposit(self,amount):
        if amount <=0:
            return False
        self.__balance += amount
        return True
    
    def withdraw(self,ammount):
        if ammount <=0 or ammount > self.__balance:
            return False
        self.__balance -= ammount
        return True
    
    #database crud
    @classmethod
    def load_from_db(cls,account_number,pin):
        connection = connect_to_database()
        if not connection:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute('select account_number, name, pin, balance from accounts where account_number=%s',(account_number,))
            result = cursor.fetchone()
            connection.commit()
            cursor.close()
            if result:
                stored_pin_hash = result[2]
                if verify_pin(pin,stored_pin_hash):
                    account = cls(result[1],"",result[0])
                    account.set_pin_hash(stored_pin_hash)
                    account.set_balance(float(result[3]))
                    return account
            
        except Exception as error:
            print(f'Error loading account {error}')
            return None
    
    def save_to_db(self):
        connection = connect_to_database()
        if not connection:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute(
                '''
                insert into accounts (account_number, name, pin, balance)
                values (%s,%s,%s,%s)
                on conflict(account_number)
                do update set name = %s , pin = %s, balance= %s
                ''',
                (self.__account_number, self.__name, self.__pin, self.__balance,self.__name, self.__pin, self.__balance )
                
            )
            connection.commit()
            cursor.close()
            return True
        except Exception as error:
            print(f'Error occured while save {error}')
            return False
    
    def delete_from_db(self):
        connection = connect_to_database()
        
        if not connection:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute("delete from audit where account_number = %s",(self.__account_number,))
            cursor.execute('delete from accounts where account_number = %s',(self.__account_number,))
            connection.commit()
            cursor.close()
            return True
        except Exception as error:
            print(f'Error occured in delete as {error}')
            return None

#audit class
class Audit:    
    @staticmethod
    def log_action(account_number, holder_name,action, amount=0.0):
        connection = connect_to_database()
        if not connection:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute('''
                           insert into audit (account_number, holder_name, action,amount) values 
                           (%s,%s,%s,%s)
                           ''',(account_number,holder_name,action,amount))
            connection.commit()
            cursor.close()
            return True
        except Exception as error:
            print(f'Error occured in log actions as {error}')
            return None

    @staticmethod
    def get_single_audit_log(account_number):
        connection = connect_to_database()
        if not connection:
            return []
        try:
            cursor = connection.cursor()
            cursor.execute('''
                           select id, holder_name, action, amount, time_stamp from audit where account_number = %s
                           order by time_stamp desc
                           ''',(account_number,))
            results = cursor.fetchall()
            connection.commit()
            cursor.close()
            logs =[]
            for row in results:
                logs.append({
                    "id":row[0],
                    "holder_name":row[1],
                    "action":row[2],
                    "amount" :row[3],
                    "time_stamp":row[4]
                })
            return logs
        except Exception as error:
            print(f'Error occured in log in{account_number} actions as {error}')
            return None

    @staticmethod
    def get_all_audit_log():
        connection = connect_to_database()
        if not connection:
            return []
        try:
            cursor = connection.cursor()
            cursor.execute('''
                           select id, holder_name, action, amount, time_stamp from audit
                           order by time_stamp desc
                           ''')
            results = cursor.fetchall()
            connection.commit()
            cursor.close()
            logs =[]
            for row in results:
                logs.append({
                    "id":row[0],
                    "holder_name":row[1],
                    "action":row[2],
                    "amount" :row[3],
                    "time_stamp":row[4]
                })
            return logs
        except Exception as error:
            print(f'Error occured in all logs audits as {error}')
            return None
    
    @staticmethod
    def clear_single_audit_log(account_number):
        connection = connect_to_database()
        if not connection:
            return []
        try:
            cursor = connection.cursor()
            cursor.execute('''
                           delete from audit where account_number = %s
                           ''',(account_number,))
           
            connection.commit()
            cursor.close()
            return True
        except Exception as error:
            print(f'Error occured in delete log in{account_number} audits as {error}')
            return None

    @staticmethod
    def clear_all_audit_log():
        connection = connect_to_database()
        if not connection:
            return []
        try:
            cursor = connection.cursor()
            cursor.execute('''
                           delete from audit
                           ''')
            connection.commit()
            cursor.close()
            return True
        except Exception as error:
            print(f'Error occured in clear all audits as {error}')
            return None
    

#banksystem class

class BankSystem:
    def __init__(self):
        result = initilize_tables()
        print("Table initialization result:", result)

        if not result:
            raise Exception("Database tables could not be initialized")
    def create_account(self, name, pin):
        account = Account(name, pin)
        if account.save_to_db():
            Audit.log_action(account.get_account_number(), account.get_name(),"account creatd",0.0)
            return account
        return None
    def read_account(self, account_number, pin):
        account = Account.load_from_db(account_number, pin)
        if account:
            Audit.log_action(
                account_number,account.get_name(), "Details Checked",0.0 )
            return account
        return None
        
    def update_account(self, account):
        return account.save_to_db()
    
    def delete_account(self, account_number, pin):
        account = Account.load_from_db(account_number, pin)
        if account:
            success = account.delete_from_db()
            if success:
                Audit.log_action(
                account_number,account.get_name(), "Account Deleted",0.0 )
            return True
        return False
   
    def deposit(self, account_number, pin,amount):
        account = Account.load_from_db(account_number, pin)
        if account and account.deposit(amount):
            if account.save_to_db():
                Audit.log_action(
                account_number,account.get_name(), "amount deposited",amount )
                return True
        return False
    
    def withdraw(self, account_number, pin,amount):
        account = Account.load_from_db(account_number, pin)
        if account and account.withdraw(amount):
            if account.save_to_db():
                Audit.log_action(
                account_number,account.get_name(), "amount withdrawn",amount )
                return True
        return False
    
    def get_account_balance(self, account_number, pin):
            account = Account.load_from_db(account_number, pin)
            if account:
                Audit.log_action(
                    account_number,account.get_name(), "Balance Checked",0.0)
                return account.get_balance()
            return None
    
    def get_single_audit_logs(self, account_number):
                return Audit.get_single_audit_log(account_number)
        
    def get_all_audit_logs(self):
                return Audit.get_all_audit_log()
            
    def clear_single_audit_logs(self, account_number):
                return Audit.clear_single_audit_log(account_number)
        
    def clear_all_audit_logs(self):
                return Audit.clear_all_audit_log()
            
    
        
# valid amount input
def get_valid_amount(prompt):
    while True:
        try:
            amount = float(input(prompt))
            if amount<= 0 :
                print("amount must be greater than zero")
                continue
            return amount
        except ValueError:
            print("please enter a valid amount in numbers ")



#CLI menu
def create_account_cli(bank):
    print("="*40)
    print("Create New Account")
    print("="*40)
    name = input("Enter your name: ").strip()
    if not name:
        print("Name can not be empty/ignored.")
        input("press enter to continue...")
        return        
    pin = input("Enter 4-digit pin: ").strip()
    if len(pin) !=4 or not pin.isdigit():
        print("PIN must be 4-digit number.")
        input("Press enter to continue... ")
        return
    confirm_pin = input("confirm your PIN: ").strip()
    if pin != confirm_pin:
        print("PIN is not matching.")
        print("Press enter to continue..")
        return
    account = bank.create_account(name,pin)
    if account:
        print(f"\nAccount successfully created")
        print(f"\nAccount number: {account.get_account_number()}")
        print(f"Save your Account Number and PIN securely")
        
        
    else:
        print(f"\nAccount not created , try again.")

    input("press enter to continue...")

#check balance
def check_balance_cli(bank,account,pin):
    print("="*40)
    print("Check your balance")
    print("="*40)
    name = input("Enter your name: ").strip()
    balance = bank.get_account_balance(account.get_account_number(),pin)
    
    if balance is not None:
        print(f"\nCurrent Balance: {balance:.2f}")       
        
    else:
        print(f"\nError checking balance , try again.")

    input("press enter to continue...")
    

def deposit_money_cli(bank,account,pin):
    print("="*40)
    print("Deposit Money")
    print("="*40)
    amount = get_valid_amount("Enter deposit amount: ")
    if bank.deposit(account.get_account_number(),pin, amount):
        print(f"{amount:.2f} successfully deposited") 
        balance= bank.get_account_balance(account.get_account_number(),pin)
        if balance is not None:
            print(f"New balance: {balance:.2f}") 
        else:
            print("Error checking new balance.")  
    else:
        print(f"\nError depositing balance , try again.")

    input("press enter to continue...")
        

def withdraw_money_cli(bank,account,pin):
    print("="*40)
    print("withdraw Money")
    print("="*40)
    
    amount = get_valid_amount("Enter withdraw amount: ")
    if bank.withdraw(account.get_account_number(),pin, amount):
        print(f"{amount:.2f} successfully withdrawn") 
        balance= bank.get_account_balance(account.get_account_number(),pin)
        if balance is not None:
            print(f"New balance: {balance:.2f}") 
        else:
            print("Error checking balance")
        
    else:
        print(f"\nError withdrawning balance , try again.")

    input("press enter to continue...")

def transaction_history_cli(bank,account,pin):
    print("="*40)
    print("Account Transactions")
    print("="*40)
    logs = bank.get_single_audit_logs(account.get_account_number())
    if not logs:
        print("No transaction found")
    else:
        for log in logs:
            print(f"{log['time_stamp']} {log['action']}  - {log['amount']:.2f} by {log['holder_name']}")
    input("Press enter to continue..")

def update_account_cli(bank,account,pin):
    print("="*40)
    print("Update Account Info")
    print("="*40)
    new_name = input("Enter your name: ").strip()
    if new_name:
        account.set_name(new_name)
        if bank.update_account(account):
            Audit.log_action(account.get_account_number(), account.get_name(),"Account Info updated", 0.0)
            print("name updated Successfully")
        else:
            print("error updating account")
    else:    
        print("no changes made.")

    input("press enter to continue...")
def change_pin_logout_cli(bank,account,pin):
    print("="*40)
    print("Update Account PIN")
    print("="*40)
    old_pin = input("Enter current pin: ").strip()
    if old_pin !=pin:
        print("Inccorect current pin")
        print("Press enter to continue...")
        return False
    
    
    new_pin = input("Enter 4digit new pin ").strip()
    if len(new_pin) !=4 or not new_pin.isdigit():
        print("PIN must be 4-digit number.")
        input("Press enter to continue... ")
        return
    confirm_pin = input("confirm your PIN: ").strip()
    if new_pin != confirm_pin:
        print("PIN is not matching.")
        print("Press enter to continue..")
        
    account.set_pin(new_pin)
    if bank.update_account(account):
            Audit.log_action(account.get_account_number(), account.get_name(),"Account PIN updated", 0.0)
            print("PIN updated Successfully, you will be logged out")
            return True
    
    print("Error updating the pin.")
    input("press enter to continue...")
    

def delete_account_cli(bank,account,pin):
    print("="*40)
    print("Close Account")
    print("="*40)
    confirm = input("are your sure, you want to delete ths account? (yes/no) ").strip().lower()
    if confirm !="yes":
        print("Account Deletion Cancelled.")
        input("Press enter to continue..")
        return False
    
    
    re_pin = input("re-enter your Pin to confirm: ").strip()
    if re_pin != pin:
        print("PIN is not matching account not deleted.")
        print("Press enter to continue..")
    if bank.delete_account(account.get_account_number(),pin):
        print("Account closed successfully.")
        print("press enter to continue...")
    print("Error closing account pin, try again..")
    input("Press enter to continue.")
    return False    
        
def login_account_cli(bank):
    print("="*40)
    print("Create New Account")
    print("="*40)
    account_number = input("Enter your account_number: ").strip()
    if not account_number:
        print("account number can not be empty/ignored.")
        input("press enter to continue...")
        return        
    pin = input("Enter 4-digit pin: ").strip()
    account = bank.read_account(account_number,pin)
    
    if not account:
        print("Wrong Credientials.")
        input("Press enter to continue... ")
        return
    
    while True:
        print("="*40)
        print(f"Welcome, {account.get_name()}!")
        print(f"Account Number:  , {account.get_account_number()}!")
        print("="*40)
        print('''
              1. Check Balance
              2. Deposit Balance
              3. Withdraw Balance
              4. Trnsaction History
              5. Update Account Info
              6. Change PIN
              7. Delete Account
              8. logout''')
        
        print("="*40)
        choice = int(input("Enter your choice(0-6):"))
        if choice==1:
            check_balance_cli(bank,account,pin)
        elif choice ==2:
            deposit_money_cli(bank, account,pin)
        elif choice == 3:
            withdraw_money_cli(bank, account,pin)
        elif choice == 4:
            transaction_history_cli(bank, account,pin)
        elif choice == 5:
            update_account_cli(bank, account,pin)
        elif choice ==6:
            if change_pin_logout_cli(bank,account,pin):
                break
        elif choice ==7:
            if delete_account_cli(bank,account,pin):
                break   
        elif choice ==9:
            print("Thank you so much for using our services, do visit again.")
            exit()
        else:
            print("please provide a valid choice , try again.")
        
                
                

#main menu of CLI
def main_menu_cli():
    bank = BankSystem()
    
    while True:
        print("="*40)
        print("Bank Management System")
        print("="*40)
        print('''
              1. New Account
              2. Login Account
              ''')
        print("0.Exit")
        print("="*40)
        choice = int(input("Enter your choice(0-6):"))
        if choice==1:
            create_account_cli(bank)
        elif choice ==2:
            login_account_cli(bank)
        elif choice ==0:
            print("Thank you so much for using our services, do visit again.")
            exit()
        else:
            print("please provide a valid choice , try again.")
        

if __name__=="__main__":
    main_menu_cli()

