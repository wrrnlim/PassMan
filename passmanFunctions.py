import sqlite3, hashlib

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

def storeDB(service, username, password):
    db = sqlite3.connect(database)
    c = db.cursor()
    c.execute('''
        INSERT INTO passwords
        VALUES (:service, :username, :password)
    ''',{'service':service,'username':username,'password':password})
    db.commit()
    db.close()

def hashPassword(password):
    hash = hashlib.md5(password.encode())
    hash = hash.hexdigest()
    print(hash)
    return hash