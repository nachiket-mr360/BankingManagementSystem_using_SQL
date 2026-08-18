from Database import connect_to_database
import string
import hashlib

#encrypt and varify pin
def __hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

def __verify_pin(input_pin, stored_hash):
    return __hash_pin(input_pin) == stored_hash


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
                create_at timestamp default currect_timestamp
            );
            '''
            create_audit_table = '''
            create table if not exists audit(
                id serial primary key,
                account_number varchar(50),
                holder_name varchar(100),
                action varchar(100) not null,
                amount decimal(15,2) default 0.00,
                time_stamp timestamp default currect_timestamp,
                foreign key (account_number) references accounts(account_number)
            );
            '''
            cursor.execute(create_account_table)
            cursor.execute(create_audit_table)
            connection.commit()
            cursor.close()
            
            
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
        self.__pin =__hash_pin(pin)
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
    def set_pin_hash(self,pin):
        self.__pin = __hash_pin(pin)
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
            cursor.execute('select account_number, name, pin, balance from accounts where account_number=%s',(account_number))
            result = cursor.fetchone()
            connection.commit()
            cursor.close()
            if result:
                stored_pin_hash = result[2]
                if __verify_pin(pin,stored_pin_hash):
                    account = cls(result[1],"",result[0])
                    account_number.set_balance(float(result[3]))
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
                vales (%s,%s,%s,%s)
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
            return None
    
    def delete_from_db(self):
        connection = connect_to_database()
        if not connection:
            return False
        try:
            cursor = connection.cursor()
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
                           inset into audit (account_number, holder_name, action,amount) vales 
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
                           select id, holder_name, actionm amount, time_stamp from audit where account_number = %s
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
                           select id, holder_name, actionm amount, time_stamp from audit
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
        pass
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
    
    def read_account(self, account_number, pin):
        account = Account.load_from_db(account_number, pin)
        if account:
            success = account.delete_from_db()
            if success:
                Audit.log_action(
                account_number,account.get_name(), "Account Deleted",0.0 )
            return True
        return False