<?php
// Устанавливаем кодировку
header('Content-Type: text/html; charset=utf-8');

// Имя файла для хранения отзывов
$file = "guest.txt";
// Максимальное количество отображаемых отзывов
$max_messages = 50;

// Обработка данных формы
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $email = isset($_POST['email']) ? trim($_POST['email']) : '';
    $name = isset($_POST['name']) ? trim($_POST['name']) : '';
    $msg = isset($_POST['msg']) ? trim($_POST['msg']) : '';
    
    // Проверка и обрезка данных
    if ($email == "") $email = "нет";
    $msg = substr($msg, 0, 999);
    $email = substr($email, 0, 39);
    $name = substr($name, 0, 39);
    
    // Если есть имя и сообщение - сохраняем
    if ($msg != "" && $name != "") {
        // Форматируем время
        $time = date("H:i d.m.Y");
        // Заменяем переносы строк на <br>
        $msg_formatted = str_replace("\n", "<br>", $msg);
        
        // Формируем строку для записи
        $entry = "\n<b>$time $name (<a href=\"mailto:$email\">$email</a>)</b><br>$msg_formatted<hr>";
        
        // Записываем в файл
        $fp = fopen($file, "a+");
        fwrite($fp, $entry);
        fclose($fp);
        
        // Перенаправляем, чтобы избежать повторной отправки формы
        header("Location: guest.php");
        exit();
    }
}
?>

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Гостевая книга</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background-color: #f9f9f9;
        }
        .container {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h2 {
            color: #333;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }
        form {
            margin-bottom: 30px;
        }
        label {
            display: block;
            margin: 10px 0 5px;
            font-weight: bold;
        }
        input[type="text"], textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        textarea {
            height: 150px;
            resize: vertical;
        }
        input[type="submit"] {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
        }
        input[type="submit"]:hover {
            background: #45a049;
        }
        .messages {
            border-top: 1px solid #eee;
            padding-top: 20px;
            margin-top: 20px;
        }
        .message {
            margin-bottom: 20px;
            padding: 15px;
            background: #f8f8f8;
            border-radius: 5px;
            border-left: 4px solid #4CAF50;
        }
        .message-info {
            color: #666;
            font-size: 14px;
            margin-bottom: 10px;
        }
        .no-messages {
            color: #999;
            text-align: center;
            padding: 40px;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Гостевая книга магазина</h2>
        
        <form action="guest.php" method="post">
            <label for="email">Введите e-mail:</label>
            <input type="text" name="email" id="email" placeholder="example@mail.ru">
            
            <label for="name">Ваше имя:</label>
            <input type="text" name="name" id="name" placeholder="Иван Иванов" required>
            
            <label for="msg">Отзыв о посещении нашего магазина:</label>
            <textarea name="msg" id="msg" placeholder="Напишите ваш отзыв здесь..." required></textarea>
            
            <input type="submit" value="Сохранить отзыв">
        </form>
        
        <div class="messages">
            <h3>Последние отзывы:</h3>
            
            <?php
            // Чтение и вывод отзывов
            if (file_exists($file)) {
                $lines = file($file);
                $total = count($lines);
                
                if ($total > 0) {
                    $start = max(0, $total - $max_messages);
                    
                    // Выводим отзывы в обратном порядке (новые сверху)
                    for ($i = $total - 1; $i >= $start; $i--) {
                        if (trim($lines[$i]) != '') {
                            echo '<div class="message">' . $lines[$i] . '</div>';
                        }
                    }
                } else {
                    echo '<div class="no-messages">Пока нет отзывов. Будьте первым!</div>';
                }
            } else {
                echo '<div class="no-messages">Пока нет отзывов. Будьте первым!</div>';
            }
            ?>
        </div>
    </div>
</body>
</html>