<?php
$hostname = 'localhost';
$database = 'srv89577_b8';
$username = 'srv89577_user8';
$password = '1234';

@mysql_connect($hostname, $username, $password);
@mysql_select_db($database);

$q = "CREATE TABLE Goods (
    id INT(11) UNSIGNED AUTO_INCREMENT,
    Name VARCHAR(50) DEFAULT 'нет',
    Price INT(11) UNSIGNED DEFAULT '0',
    Producer VARCHAR(50) DEFAULT 'неизвестен',
    Phone INT(6) UNSIGNED DEFAULT '0',
    PRIMARY KEY(id)
)";

$r = mysql_query($q);

if ($r) {
    echo "Таблица Goods успешно создана.";
} else {
    echo "Ошибка при создании таблицы: " . mysql_error();
}

@mysql_free_result($r);
mysql_close();
?>