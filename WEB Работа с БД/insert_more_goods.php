<?php
$hostname = 'localhost';
$database = 'srv89577_b8';
$username = 'srv89577_user8';
$password = '1234';

@mysql_connect($hostname, $username, $password);
@mysql_select_db($database);

// Массив данных для вставки
$goods_data = array(
    array('ГАЗ-3110-101', '157000', 'РусАвтоПАЗ', '993705'),
    array('ГАЗ-3302-14', '168000', 'РусАвтоПАЗ', '993705'), // Исправлено: ТАЗ на ГАЗ
    array('ЗИЛ-5301 АО', '270000', 'РусАвтоПАЗ', '993705')
);

$success_count = 0;
$error_count = 0;

foreach ($goods_data as $item) {
    $name = mysql_real_escape_string($item[0]);
    $price = $item[1];
    $producer = mysql_real_escape_string($item[2]);
    $phone = $item[3];
    
    $q = "INSERT INTO Goods (Name, Price, Producer, Phone) 
          VALUES ('$name', '$price', '$producer', '$phone')";
    
    $r = mysql_query($q);
    
    if ($r) {
        $success_count++;
    } else {
        $error_count++;
        echo "Ошибка при добавлении '$name': " . mysql_error() . "<br>";
    }
}

echo "Добавлено записей: $success_count<br>";
echo "Ошибок: $error_count";

mysql_close();
?>