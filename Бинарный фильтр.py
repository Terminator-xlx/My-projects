import cv2
import numpy as np

# Загрузка изображения
image = cv2.imread('lots of zebras.jpg', cv2.IMREAD_GRAYSCALE)

# Проверка на наличие изображения
if image is None:
    print("Ошибка: изображение не найдено.")
    exit()

# Нанесение импульсного шума
def add_salt_and_pepper_noise(image, prob=0.02):
    output = np.copy(image)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = np.random.random()
            if rdn < prob:
                output[i][j] = 0  # Salt noise
            elif rdn > thres:
                output[i][j] = 255  # Pepper noise
    return output

noisy_image = add_salt_and_pepper_noise(image)

# Бинарная фильтрация
def binary_filter(image, threshold=128):
    _, binary_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return binary_image

# Фильтрация исходного изображения
binary_original = binary_filter(image)

# Фильтрация зашумленного изображения
binary_noisy = binary_filter(noisy_image)

# Сохранение изображений
cv2.imwrite('original_image.jpg', image)
cv2.imwrite('noisy_image.jpg', noisy_image)
cv2.imwrite('binary_original.jpg', binary_original)
cv2.imwrite('binary_noisy.jpg', binary_noisy)

print("Изображения сохранены.")