"""
Interactive MySQL connection tester.
This will help you find the correct credentials.
"""
import mysql.connector
import getpass

HOST = "127.0.0.1"
PORT = 3306

print("="*70)
print("MySQL Connection Tester")
print("="*70)
print(f"Host: {HOST}")
print(f"Port: {PORT}")
print()

# Try different common passwords
common_passwords = ["", "root", "admin", "password", "mysql"]

user = input("Enter MySQL username [root]: ").strip() or "root"
print()

print("Trying common passwords...")
for pwd in common_passwords:
    try:
        pwd_display = "(empty)" if pwd == "" else pwd
        print(f"  Trying password: {pwd_display}...", end=" ")
        conn = mysql.connector.connect(
            host=HOST,
            port=PORT,
            user=user,
            password=pwd
        )
        print("✓ SUCCESS!")
        print()
        print(f"✓ Found working credentials:")
        print(f"  DB_USER={user}")
        print(f"  DB_PASS={pwd}")
        print()
        print("Update your .env file with these values.")
        conn.close()
        exit(0)
    except mysql.connector.Error:
        print("✗ failed")

print()
print("None of the common passwords worked.")
print()
manual_pwd = getpass.getpass("Enter the MySQL password manually (or press Enter to skip): ")
if manual_pwd:
    try:
        conn = mysql.connector.connect(
            host=HOST,
            port=PORT,
            user=user,
            password=manual_pwd
        )
        print()
        print("✓ SUCCESS!")
        print()
        print(f"✓ Working credentials:")
        print(f"  DB_USER={user}")
        print(f"  DB_PASS={manual_pwd}")
        print()
        print("Update your .env file with these values.")
        conn.close()
    except mysql.connector.Error as e:
        print(f"✗ Failed: {e}")
else:
    print()
    print("Please check your MySQL Workbench connection settings")
    print("or reset the root password following MySQL documentation.")
