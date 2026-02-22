<?php
if (isset($_POST['R'])) {
    $selected_goods = $_POST['R'];
    echo "Вы выбрали товар: <strong>" . htmlspecialchars($selected_goods) . "</strong><br>";
    echo "<a href='show.php'>Вернуться к списку товаров</a>";
} else {
    echo "Товар не выбран! <a href='show.php'>Вернуться</a>";
}
?>