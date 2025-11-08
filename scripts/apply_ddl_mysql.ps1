# Run this after MySQL is installed and accessible
param([string]$Db="olist",[string]$User="root",[string]$Pass="")
$PassArg = if ($Pass) { "-p$Pass" } else { "" }
mysql -u $User $PassArg -e "CREATE DATABASE IF NOT EXISTS $Db;"
mysql -u $User $PassArg $Db < db/ddl_mysql/000_base.sql
mysql -u $User $PassArg $Db < db/ddl_mysql/010_categories.sql
mysql -u $User $PassArg $Db < db/ddl_mysql/020_geo_zip.sql
mysql -u $User $PassArg $Db < db/ddl_mysql/030_fk_v2_1.sql
mysql -u $User $PassArg $Db < db/ddl_mysql/040_indexes.sql
Write-Host "MySQL DDL applied."
