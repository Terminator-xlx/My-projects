<?php
$hostname = 'localhost';
$database = 'srv89577_b8';
$username = 'srv89577_user8';
$password = '1234';

@mysql_connect($hostname, $username, $password);
@mysql_select_db($database);

echo "<html><head><title>Проверка таблицы</title>";
echo "<style>body {font-family: Arial; padding: 20px;} .success {color: green;} .error {color: red;}</style>";
echo "</head><body>";
echo "<h2>Проверка состояния таблицы Goods</h2>";

// Проверяем существование таблицы
$result = mysql_query("SHOW TABLES LIKE 'Goods'");
if (mysql_num_rows($result) > 0) {
    echo "<p class='success'>✓ Таблица Goods существует</p>";
    
    // Проверяем структуру таблицы
    $desc = mysql_query("DESCRIBE Goods");
    echo "<h3>Структура таблицы:</h3>";
    echo "<table border='1' cellpadding='5'>";
    echo "<tr><th>Поле</th><th>Тип</th><th>NULL</th><th>Ключ</th><th>По умолчанию</th><th>Extra</th></tr>";
    while ($row = mysql_fetch_assoc($desc)) {
        echo "<tr>";
        echo "<td>" . $row['Field'] . "</td>";
        echo "<td>" . $row['Type'] . "</td>";
        echo "<td>" . $row['Null'] . "</td>";
        echo "<td>" . $row['Key'] . "</td>";
        echo "<td>" . $row['Default'] . "</td>";
        echo "<td>" . $row['Extra'] . "</td>";
        echo "</tr>";
    }
    echo "</table>";
    
    // Подсчитываем количество записей
    $count = mysql_query("SELECT COUNT(*) as total FROM Goods");
    $row = mysql_fetch_assoc($count);
    echo "<p>Количество записей в таблице: <strong>" . $row['total'] . "</strong></p>";
} else {
    echo "<p class='error'>✗ Таблица Goods не существует</p>";
    echo "<p><a href='table.php'>Создать таблицу Goods</a></p>";
}

echo "<br><a href='menu.html'>Вернуться в главное меню</a>";
echo "</body></html>";

mysql_close();
?>