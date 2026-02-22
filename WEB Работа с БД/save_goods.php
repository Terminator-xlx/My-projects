<?php
$hostname = 'localhost';
$database = 'srv89577_b8';
$username = 'srv89577_user8';
$password = '1234';

// Проверка заполнения полей
if (empty($_POST['name']) || empty($_POST['price']) || 
    empty($_POST['producer']) || empty($_POST['phone'])) {
    die("Все поля формы должны быть заполнены! <a href='add_goods.html'>Вернуться</a>");
}

// Подключение к БД
@mysql_connect($hostname, $username, $password);
@mysql_select_db($database);

// Экранирование данных
$name = mysql_real_escape_string($_POST['name']);
$price = intval($_POST['price']);
$producer = mysql_real_escape_string($_POST['producer']);
$phone = mysql_real_escape_string($_POST['phone']);

// Вставка данных
$q = "INSERT INTO Goods (Name, Price, Producer, Phone) 
      VALUES ('$name', '$price', '$producer', '$phone')";

$r = mysql_query($q);

if ($r) {
    echo "Товар успешно добавлен в базу данных!<br>";
} else {
    echo "Ошибка при добавлении товара: " . mysql_error() . "<br>";
}

echo "<a href='add_goods.html'>Добавить еще товар</a> | ";
echo "<a href='show.php'>Просмотреть все товары</a>";

mysql_close();
?>