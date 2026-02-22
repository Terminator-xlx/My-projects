<?php
$hostname = 'localhost';
$database = 'srv89577_b8';
$username = 'srv89577_user8';
$password = '1234';

@mysql_connect($hostname, $username, $password);
@mysql_select_db($database);

echo "<!DOCTYPE html>
<html>
<head>
    <meta charset='UTF-8'>
    <title>Список товаров</title>
    <style>
        body {font-family: Arial; padding: 20px;}
        table {border-collapse: collapse; width: 100%; margin: 20px 0;}
        th, td {border: 1px solid #ddd; padding: 8px; text-align: left;}
        th {background-color: #4CAF50; color: white;}
        tr:nth-child(even) {background-color: #f2f2f2;}
        .nav {background: #f0f0f0; padding: 10px; margin-bottom: 20px;}
        .radio-form {background: #e8f5e9; padding: 20px; margin-top: 30px;}
    </style>
</head>
<body>";

// Навигация
echo "<div class='nav'>";
echo "<a href='menu.html'>Главное меню</a> | ";
echo "<a href='add_goods.html'>Добавить товар</a> | ";
echo "<a href='show.php'>Обновить список</a>";
echo "</div>";

echo "<h2>Сегодня в продаже</h2>";

$q = "SELECT id, Name, Price, Producer, Phone FROM Goods ORDER BY id";
$r = mysql_query($q);

if (mysql_num_rows($r) == 0) {
    echo "<p>В базе данных нет товаров.</p>";
    echo "<p><a href='add_goods.html'>Добавить первый товар</a></p>";
} else {
    // Табличное представление
    echo "<table>";
    echo "<tr>
            <th>ID</th>
            <th>Наименование</th>
            <th>Цена</th>
            <th>Производитель</th>
            <th>Телефон</th>
          </tr>";
    
    while ($row = mysql_fetch_assoc($r)) {
        echo "<tr>";
        echo "<td>" . $row['id'] . "</td>";
        echo "<td>" . htmlspecialchars($row['Name']) . "</td>";
        echo "<td>" . number_format($row['Price'], 0, ',', ' ') . " руб.</td>";
        echo "<td>" . htmlspecialchars($row['Producer']) . "</td>";
        echo "<td>" . $row['Phone'] . "</td>";
        echo "</tr>";
    }
    echo "</table>";
    
    // Радиокнопки для выбора (как в методичке)
    echo "<div class='radio-form'>";
    echo "<h3>Выберите товар:</h3>";
    echo "<form action='myscript.php' method='post'>";
    mysql_data_seek($r, 0); // Возвращаем указатель на начало
    
    while ($row = mysql_fetch_assoc($r)) {
        $name = htmlspecialchars($row['Name']);
        $id = $row['id'];
        echo "<input type='radio' name='R' value='$id'> $name (ID: $id)<br>";
    }
    
    echo "<br><input type='submit' value='Выбрать товар'>";
    echo "</form>";
    echo "</div>";
}

echo "<br><div class='nav'>";
echo "<a href='menu.html'>Главное меню</a> | ";
echo "<a href='add_goods.html'>Добавить товар</a>";
echo "</div>";

echo "</body></html>";

mysql_close();
?>