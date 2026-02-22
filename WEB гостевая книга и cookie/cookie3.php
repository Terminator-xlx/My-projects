<?php
// Удаляем cookie (устанавливаем время в прошлом)
setcookie("UserName", "", time() - 3600, "/");
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Cookie - Удаление</title>
</head>
<body>
    <h2>Cookie удалены!</h2>
    <p>Cookie "UserName" были удалены.</p>
    
    <a href="cookie2.php">Проверить удаление</a> |
    <a href="cookie1.php">Установить заново</a>
</body>
</html>