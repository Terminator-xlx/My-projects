<?php
$hostname = 'localhost';
$database = 'srv89577_b8';
$username = 'srv89577_user8';
$password = '1234';

@mysql_connect($hostname, $username, $password);
@mysql_select_db($database);

$q = "INSERT INTO Goods (Name, Price, Producer, Phone) 
      VALUES ('ГАЗ-3110-411', '154000', 'РусАвтоПАЗ', '993705')";

$r = mysql_query($q);

if ($r) {
    echo "Запись успешно добавлена в таблицу Goods.";
} else {
    echo "Ошибка при добавлении записи: " . mysql_error();
}

mysql_close();
?>