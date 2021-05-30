import sqlite3, hashlib, os

if not os.path.exists('db'): # make folder if it does not exists
    os.makedirs('db')

database = 'db\passwords.db'

def createDB():
    db = sqlite3.connect(database)
    c = db.cursor()
    # Create db if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            service text,
            username text,
            password text,
            account text,
            PRIMARY KEY (service,username)
        );
    ''')
    db.commit()
    db.close()
    

def checkMaster(username, password):
    # check if master record exists
    db = sqlite3.connect(database)
    c = db.cursor()
    hashedPass = hashPassword(password)
    c.execute('''
        SELECT username, password
        FROM passwords
        WHERE service = 'MasterPassword'
        AND username = :username;
    ''',{'username':username})
    masterPass = c.fetchone()
    db.close()

    # check password
    if not masterPass:
        return -1 # record does not exist
    elif hashedPass == masterPass[1]:
        return 0 # login successful
    else: return -2 # login unsuccessful

def storeDB(service, username, password, account):
    db = sqlite3.connect(database)
    c = db.cursor()
    c.execute('''
        INSERT INTO passwords
        VALUES (:service, :username, :password, :account)
    ''',{'service':service,'username':username,'password':password, 'account':account})
    db.commit()
    db.close()

def hashPassword(password):
    hash = hashlib.md5(password.encode())
    hash = hash.hexdigest()
    print(hash)
    return hash

def retrieveDB(service, account):
    db = sqlite3.connect(database)
    c = db.cursor()
    c.execute('''
        SELECT *
        FROM passwords
        WHERE service = :service
        AND service <> 'MasterPassword'
        AND account = :account
    ''',{'service':service,'account':account})
    records = c.fetchall()
    db.close()
    return records

def getServices(account):
    db = sqlite3.connect(database)
    c = db.cursor()
    c.execute('''
        SELECT service
        FROM passwords
        WHERE service <> 'MasterPassword'
        AND account = :account
    ''',{'account':account})
    services = c.fetchall()
    db.close()
    return services

def updateDB(account, service, username, password):
    db = sqlite3.connect(database)
    c = db.cursor()
    c.execute('''
        UPDATE passwords
        SET password = :password
        WHERE service = :service
        AND username = :username
        AND account = :account
    ''',{'password':password,'service':service,'username':username,'account':account})
    db.commit()
    db.close()

def deleteEntry(account, service, username):
    db = sqlite3.connect(database)
    c = db.cursor()
    try:
        c.execute('''
            DELETE FROM passwords
            WHERE service = :service
            AND username = :username
            AND account = :account
        ''',{'service':service,'username':username,'account':account})
        db.commit()
    except:
        return -1
    db.close()
    return 0
    