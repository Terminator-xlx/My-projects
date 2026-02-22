<?php
// Если форма отправлена - устанавливаем cookie с цветом
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['bgcolor'])) {
    $bgcolor = htmlspecialchars($_POST['bgcolor']);
    setcookie("bgcolor", $bgcolor, time() + 86400, "/"); // 24 часа
    header("Location: color_page1.php");
    exit();
}
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Выбор цвета фона</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f0f0f0;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
        }
        h2 {
            color: #333;
            margin-bottom: 20px;
        }
        select {
            padding: 10px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 5px;
            width: 200px;
        }
        input[type="submit"] {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 15px;
        }
        input[type="submit"]:hover {
            background: #45a049;
        }
        .color-options {
            display: flex;
            gap: 10px;
            margin: 20px 0;
        }
        .color-box {
            width: 50px;
            height: 50px;
            border-radius: 5px;
            cursor: pointer;
            border: 2px solid transparent;
        }
        .color-box:hover {
            border-color: #333;
        }
        .red { background-color: #ffcccc; }
        .blue { background-color: #cce5ff; }
        .green { background-color: #d4edda; }
        .black { background-color: #333; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Выберите удобный для Вас цвет фона страницы нашего магазина</h2>
        
        <form method="post" action="color_form.php">
            <select name="bgcolor" id="bgcolor" required>
                <option value="">-- Выберите цвет --</option>
                <option value="#ffcccc">Красный</option>
                <option value="#cce5ff">Синий</option>
                <option value="#d4edda">Зеленый</option>
                <option value="#333333">Черный</option>
            </select>
            
            <div class="color-options">
                <div class="color-box red" onclick="document.getElementById('bgcolor').value='#ffcccc'"></div>
                <div class="color-box blue" onclick="document.getElementById('bgcolor').value='#cce5ff'"></div>
                <div class="color-box green" onclick="document.getElementById('bgcolor').value='#d4edda'"></div>
                <div class="color-box black" onclick="document.getElementById('bgcolor').value='#333333'"></div>
            </div>
            
            <br>
            <input type="submit" value="Сохранить выбор цвета">
        </form>
        
        <?php
        // Показываем текущий цвет, если cookie установлены
        if (isset($_COOKIE['bgcolor'])) {
            echo '<div style="margin-top: 20px; padding: 10px; background: ' . $_COOKIE['bgcolor'] . '">';
            echo '<strong>Текущий выбранный цвет:</strong> ' . $_COOKIE['bgcolor'];
            echo '</div>';
        }
        ?>
    </div>
    
    <script>
        // Подсветка выбранного цвета
        document.getElementById('bgcolor').addEventListener('change', function() {
            document.body.style.backgroundColor = this.value;
        });
        
        // Восстанавливаем сохраненный цвет при загрузке
        window.onload = function() {
            var savedColor = "<?php echo isset($_COOKIE['bgcolor']) ? $_COOKIE['bgcolor'] : ''; ?>";
            if (savedColor) {
                document.body.style.backgroundColor = savedColor;
                document.getElementById('bgcolor').value = savedColor;
            }
        };
    </script>
</body>
</html>