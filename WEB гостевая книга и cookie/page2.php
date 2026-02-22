<?php
header('Content-Type: text/html; charset=utf-8');

$userName = isset($_POST['UserName']) ? htmlspecialchars($_POST['UserName']) : 'Гость';
$product = isset($_POST['product']) ? htmlspecialchars($_POST['product']) : 'не выбран';

echo "<h2>Привет, $userName!</h2>";
echo "<p>Вы выбрали: <strong>$product</strong></p>";
echo '<form method="post" action="page3.php">';
echo '<input type="hidden" name="UserName" value="' . $userName . '">';
echo '<input type="hidden" name="product" value="' . $product . '">';
echo 'Укажите количество товара: ';
echo '<input type="number" name="quantity" min="1" max="100" value="1" required>';
echo '<br><br>';
echo '<input type="submit" value="Купить >>">';
echo '</form>';
?>