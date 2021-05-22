#
# Password Manager by Warren Lim
# Version 1.0
#
import sqlite3, hashlib

def main():
    db = sqlite3.connect('passwords.db')
    c = db.cursor()
    # Create db if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            site text,
            username text,
            password text
        );
    ''')
    hashPass('testpassword'.encode(encoding='utf-8'))

def hashPass(password):
    hash = hashlib.md5(password)
    hash = hash.hexdigest()
    print(hash)
    return hash    

main()