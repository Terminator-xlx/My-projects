<?php
function displayNavigation() {
    echo '<div style="background: #f0f0f0; padding: 10px; margin: 10px 0; border-radius: 5px;">';
    echo '<strong>Навигация:</strong> ';
    echo '<a href="menu.html">Главное меню</a> | ';
    echo '<a href="add_goods.html">Добавить товар</a> | ';
    echo '<a href="show.php">Просмотр товаров</a> | ';
    echo '<a href="check_table.php">Проверка БД</a>';
    echo '</div>';
}
?>