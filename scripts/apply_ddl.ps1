param([string]$Db="olist",[string]$User="postgres")
psql -U $User -d $Db -f db/ddl/000_base.sql
psql -U $User -d $Db -f db/ddl/010_categories.sql
psql -U $User -d $Db -f db/ddl/020_geo_zip.sql
psql -U $User -d $Db -f db/ddl/030_fk_v2_1.sql
psql -U $User -d $Db -f db/ddl/040_indexes.sql
Write-Host "DDL applied."