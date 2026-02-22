<?php
// Устанавливаем cookie ДО любого вывода
setcookie("UserName", "Student", time() + 3600, "/"); // Действует 1 час
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Cookie - Установка</title>
</head>
<body>
    <h2>Cookie установлены!</h2>
    <p>Имя пользователя "Student" сохранено в cookie на 1 час.</p>
    
    <form method="get" action="cookie2.php">
        <input type="submit" value="Перейти на следующую страницу >>">
    </form>
    
    <br>
    <a href="cookie2.php">Проверить cookie</a>
</body>
</html>