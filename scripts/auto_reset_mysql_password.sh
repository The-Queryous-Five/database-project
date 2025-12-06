#!/bin/bash
# Automated MySQL Password Reset for macOS
# This script will reset MySQL root password to 'newpass123'

echo "======================================"
echo "Automated MySQL Password Reset"
echo "======================================"
echo ""

# Step 1: Stop all MySQL processes
echo "Step 1: Stopping MySQL..."
sudo killall mysqld 2>/dev/null
sudo /usr/local/mysql/support-files/mysql.server stop 2>/dev/null
sleep 3

# Step 2: Start MySQL in safe mode
echo "Step 2: Starting MySQL in safe mode..."
sudo /usr/local/mysql/bin/mysqld_safe --skip-grant-tables --skip-networking &
SAFE_PID=$!
echo "Waiting for MySQL to start..."
sleep 8

# Step 3: Reset password using mysql command
echo "Step 3: Resetting password..."
/usr/local/mysql/bin/mysql -u root <<EOF
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'newpass123';
FLUSH PRIVILEGES;
EOF

if [ $? -eq 0 ]; then
    echo "✓ Password reset successfully!"
else
    echo "✗ Failed to reset password"
    sudo killall mysqld
    exit 1
fi

# Step 4: Stop safe mode and restart normally
echo "Step 4: Restarting MySQL normally..."
sudo killall mysqld
sleep 3
sudo /usr/local/mysql/support-files/mysql.server start

# Step 5: Test new password
echo "Step 5: Testing new password..."
sleep 2
mysql -u root -pnewpass123 -e "SELECT 'Success!' as status;" 2>/dev/null

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✓ Password reset complete!"
    echo "======================================"
    echo "Your new MySQL root password is: newpass123"
    echo ""
    echo "Updating .env file..."
    
    # Update .env file
    if [ -f ".env" ]; then
        sed -i.bak 's/^DB_PASS=.*/DB_PASS=newpass123/' .env
        echo "✓ .env file updated!"
    fi
    
    echo ""
    echo "You can now run: mysql -u root -pnewpass123"
else
    echo "✗ Password test failed. Please try manual reset."
    exit 1
fi
