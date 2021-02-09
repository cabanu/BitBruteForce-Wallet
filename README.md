This is a dirty solution to speed up the original script (https://github.com/Xefrok/BitBruteForce-Wallet) by updating an MySQL-DB. There is no check if an address is a known address. Just update the address with the private key.

If the address isn't present in te database -> nothing happens. If the address is present in the databse -> update the private key.

# Script tested on Ryzen 5 3500U
371 K/s/Core - Used settings = 6 Cores - 6 * 371 * 60 * 60 * 24 = 192.326.400 addresses / day = 70.199.136.000 addresses / year)

If you like it, buy me a coffee: 3Mnf8w4oPKFyknsnAwww6kaBdMxXDQc8M4

Enable MySQL logging: 
SET global general_log = 1;
SET global log_output = 'table';

View log:
select * from mysql.general_log;

Disable log:
SET global general_log = 0;

Clear log:
TRUNCATE mysql.general_log

Don't forget to disable the log!

# MySQL:

CREATE TABLE `btc` (
	`address` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
	`secret` VARCHAR(100) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	PRIMARY KEY (`address`) USING BTREE,
	UNIQUE INDEX `address` (`address`) USING BTREE,
	INDEX `secret` (`secret`) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;

# BitBruteForce-Wallet
This is an effective script to Brute Force, the Private Key of any Bitcoin Public Address.

How does the script work? Very easy.

Every code I´ve seen for the last year just generates randomly private and public addresses and checks the balance (very, very slow for the API Request).

So, i found 123,000 Bitcoin Addresses with 1+ BTC from 2009 to 2013 and NEVER made a transaction, therefore, lost BTC... it is just like huge pirate boats in the bottom of the ocean filled with treasures.

This Script creates randomly private and public addresses without checking the balance, instead of making API Request, the created Public Address is compared with the list I own.

Long story short. Create Random Public Address (RPA) and check one by one with the Public Address (PA) at the list.

(Script tested on Ryzen 5 3500U - 371 K/s/Core - Used settings = 6 Cores - 6 * 371 * 60 * 60 * 24 = 192.326.400 / day = 70.199.136.000 / year)


# REQUIREMENTS
<li>Python 3.x (i use 3.9)</li>
<li>pip install ecdsa</li>
pip install base58
pip install mysql-connector-python
pip install pandas (If error "pip uninstall numpy" then "pip install numpy==1.19.3")
3,000,000,000 Years
