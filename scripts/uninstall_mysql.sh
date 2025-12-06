#!/bin/bash
# Complete MySQL Uninstall Script for macOS
# This removes all MySQL files and folders

echo "======================================"
echo "MySQL Complete Uninstall for macOS"
echo "======================================"
echo ""
echo "This will completely remove MySQL from your system."
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Uninstall cancelled."
    exit 0
fi

echo ""
echo "Step 1: Stopping MySQL..."
sudo /usr/local/mysql/support-files/mysql.server stop 2>/dev/null
sudo killall mysqld 2>/dev/null
sleep 2

echo "Step 2: Removing MySQL files..."

# Remove MySQL application
sudo rm -rf /usr/local/mysql
sudo rm -rf /usr/local/mysql*

# Remove MySQL data
sudo rm -rf /Library/MySQL
sudo rm -rf /var/db/receipts/com.mysql.*

# Remove preference pane
sudo rm -rf /Library/PreferencePanes/My*

# Remove startup items
sudo rm -rf /Library/StartupItems/MySQLCOM

# Remove LaunchDaemons and LaunchAgents
sudo rm -f /Library/LaunchDaemons/com.mysql.mysql.plist
sudo rm -f /Library/LaunchDaemons/com.oracle.oss.mysql.mysqld.plist
sudo rm -f ~/Library/LaunchAgents/com.mysql.mysql.plist
sudo rm -f ~/Library/LaunchAgents/com.oracle.oss.mysql.mysqld.plist

# Remove configuration files
sudo rm -f /etc/my.cnf
sudo rm -f /etc/mysql/my.cnf
sudo rm -f ~/.my.cnf

# Remove from PATH
sudo rm -f /etc/paths.d/mysql

echo ""
echo "✓ MySQL uninstalled successfully!"
echo ""
echo "======================================"
echo "Next Steps:"
echo "======================================"
echo ""
echo "Install MySQL using Homebrew (recommended):"
echo "  1. brew install mysql"
echo "  2. brew services start mysql"
echo "  3. mysql_secure_installation"
echo ""
echo "OR download from mysql.com:"
echo "  Visit: https://dev.mysql.com/downloads/mysql/"
echo "  Download the macOS DMG installer"
echo ""
