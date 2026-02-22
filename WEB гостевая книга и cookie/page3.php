<?php
header('Content-Type: text/html; charset=utf-8');

$userName = isset($_POST['UserName']) ? htmlspecialchars($_POST['UserName']) : 'Гость';
$product = isset($_POST['product']) ? htmlspecialchars($_POST['product']) : 'не выбран';
$quantity = isset($_POST['quantity']) ? intval($_POST['quantity']) : 1;

echo "<h2>Спасибо за покупку, $userName!</h2>";
echo "<p>Вами приобретен товар: <strong>$product</strong> ($quantity штук)</p>";
echo '<br><br>';
echo '<a href="form.html">Вернуться на главную</a>';
?>