<?php
// Проверяем cookie
$userName = isset($_COOKIE['UserName']) ? htmlspecialchars($_COOKIE['UserName']) : 'Cookie не найдены';
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Cookie - Проверка</title>
</head>
<body>
    <h2>Проверка Cookie</h2>
    <p>Имя пользователя из cookie: <strong><?php echo $userName; ?></strong></p>
    
    <h3>Информация о всех cookie:</h3>
    <pre><?php print_r($_COOKIE); ?></pre>
    
    <br>
    <a href="cookie1.php">Вернуться на первую страницу</a> |
    <a href="cookie3.php">Удалить cookie</a>
</body>
</html>