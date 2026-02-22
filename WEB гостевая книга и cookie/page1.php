<?php
header('Content-Type: text/html; charset=utf-8');

// Получаем имя пользователя
$userName = isset($_POST['UserName']) ? htmlspecialchars($_POST['UserName']) : 'Гость';

echo "<h2>Привет, $userName!</h2>";
echo "<p>Выберите товар:</p>";

// Список товаров
$products = [
    'Телевизор Samsung' => 25000,
    'Смартфон iPhone' => 65000,
    'Ноутбук Asus' => 45000,
    'Наушники Sony' => 5000,
    'Планшет iPad' => 35000
];

echo '<form method="post" action="page2.php">';
echo '<input type="hidden" name="UserName" value="' . $userName . '">';
echo '<select name="product" required>';
echo '<option value="">-- Выберите товар --</option>';

foreach ($products as $name => $price) {
    echo "<option value=\"$name\">$name - $price руб.</option>";
}

echo '</select><br><br>';
echo '<input type="submit" value="Далее >>">';
echo '</form>';
?>