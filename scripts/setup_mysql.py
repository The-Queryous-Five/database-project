#!/usr/bin/env python3
"""
Interactive MySQL Password Setup
This script helps you connect to MySQL and set up the olist database
"""
import sys
import getpass
import mysql.connector
from mysql.connector import Error

def test_connection(password):
    """Test MySQL connection with given password"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=password
        )
        if connection.is_connected():
            print("✓ Successfully connected to MySQL!")
            return connection
    except Error as e:
        print(f"✗ Connection failed: {e}")
        return None

def create_database(connection):
    """Create the olist database"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS olist")
        print("✓ Database 'olist' created successfully!")
        cursor.execute("SHOW DATABASES")
        print("\nAvailable databases:")
        for (db,) in cursor:
            print(f"  - {db}")
        cursor.close()
        return True
    except Error as e:
        print(f"✗ Failed to create database: {e}")
        return False

def main():
    print("=" * 50)
    print("MySQL Connection Test & Database Setup")
    print("=" * 50)
    print()
    
    # Try common passwords first
    common_passwords = ['', 'root', 'password', 'mysql']
    
    print("Trying common passwords...")
    connection = None
    for pwd in common_passwords:
        print(f"Trying: {'(empty)' if pwd == '' else pwd}")
        connection = test_connection(pwd)
        if connection:
            password = pwd
            break
    
    # If common passwords don't work, ask user
    if not connection:
        print("\nCommon passwords didn't work. Please enter your MySQL root password:")
        for attempt in range(3):
            password = getpass.getpass("MySQL root password: ")
            connection = test_connection(password)
            if connection:
                break
            print(f"Attempt {attempt + 1}/3 failed\n")
    
    if not connection:
        print("\n✗ Could not connect to MySQL.")
        print("\nPlease:")
        print("1. Check if MySQL is running: sudo /usr/local/mysql/support-files/mysql.server status")
        print("2. Reset your password using MySQL System Preferences")
        print("3. Or follow the manual reset instructions in scripts/reset_mysql_password.sh")
        sys.exit(1)
    
    # Create database
    print()
    if create_database(connection):
        print(f"\n✓ Setup complete!")
        print(f"\nUpdate your .env file with:")
        print(f"DB_PASS={password if password else '(leave empty)'}")
        
        # Update .env file
        try:
            with open('.env', 'r') as f:
                content = f.read()
            
            # Update DB_PASS line
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('DB_PASS='):
                    lines[i] = f'DB_PASS={password}'
                    break
            
            with open('.env', 'w') as f:
                f.write('\n'.join(lines))
            
            print("✓ .env file updated automatically!")
        except Exception as e:
            print(f"Note: Could not auto-update .env: {e}")
    
    connection.close()

if __name__ == "__main__":
    main()
