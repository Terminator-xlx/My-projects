import cv2
import numpy as np
import os

# Функция для добавления импульсного шума
def add_salt_and_pepper_noise(image, prob): #prob - степень появления шума
    output = np.zeros(image.shape, np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = np.random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

# Функция для добавления гауссова шума
def add_gaussian_noise(image, mean, std_dev):
    """
    Добавляет гауссов шум к изображению.

    :param image: Исходное изображение (numpy array).
    :param mean: Среднее значение шума (по умолчанию 0).
    :param std_dev: Стандартное отклонение шума (по умолчанию 30).
    :return: Изображение с добавленным гауссовым шумом.
    """
    # Проверка, является ли изображение цветным (3 канала) или черно-белым (1 канал)
    if len(image.shape) == 3:
        h, w, c = image.shape
        noise = np.random.normal(mean, std_dev, (h, w, c)).astype(np.uint8)
    else:
        h, w = image.shape
        noise = np.random.normal(mean, std_dev, (h, w)).astype(np.uint8)

    # Добавление шума к изображению
    noisy_image = cv2.add(image, noise)

    return noisy_image

# Функция для применения медианного фильтра
def apply_median_filter(image, kernel_size=3):
    return cv2.medianBlur(image, kernel_size)

# Путь к исходному изображению
image_path = 'Stakan.jpg'

# Проверка существования файла
if not os.path.exists(image_path):
    print(f"Файл {image_path} не найден.")
else:
    # Загрузка изображения
    image = cv2.imread(image_path)

    # Проверка на успешное загрузка изображения
    if image is None:
        print(f"Не удалось загрузить изображение {image_path}.")
    else:
        # Добавление импульсного шума
        salt_and_pepper_noise = add_salt_and_pepper_noise(image, prob=0.04)
        cv2.imwrite('salt_and_pepper_noise.jpg', salt_and_pepper_noise)

        # Добавление гауссова шума
        gaussian_noise = add_gaussian_noise(image, mean=0, std_dev=0.8)
        cv2.imwrite('gaussian_noise.jpg', gaussian_noise)

        # Применение медианного фильтра к изображению с импульсным шумом
        median_filtered_salt_and_pepper = apply_median_filter(salt_and_pepper_noise)
        cv2.imwrite('median_filtered_salt_and_pepper.jpg', median_filtered_salt_and_pepper)

        # Применение медианного фильтра к изображению с гауссовым шумом
        median_filtered_gaussian = apply_median_filter(gaussian_noise)
        cv2.imwrite('median_filtered_gaussian.jpg', median_filtered_gaussian)

        print("Обработка завершена. Результаты сохранены.")