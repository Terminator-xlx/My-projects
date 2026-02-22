import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog


def select_image():
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно
    file_path = filedialog.askopenfilename(
        title="Выберите изображение",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    return file_path


# Функция для добавления импульсного шума
def add_salt_and_pepper_noise(image, prob):
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
    if len(image.shape) == 3:
        h, w, c = image.shape
        noise = np.random.normal(mean, std_dev, (h, w, c)).astype(np.uint8)
    else:
        h, w = image.shape
        noise = np.random.normal(mean, std_dev, (h, w)).astype(np.uint8)
    return cv2.add(image, noise)


# Функция для применения гауссова фильтра
def apply_gaussian_filter(image, kernel_size, sigma):
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)


# Выбор изображения через проводник
image_path = select_image()

if not image_path:
    print("Изображение не выбрано.")
else:
    # Загрузка изображения
    image = cv2.imread(image_path)

    if image is None:
        print(f"Не удалось загрузить изображение {image_path}.")
    else:
        # Добавление шумов и применение фильтров
        salt_and_pepper_noise = add_salt_and_pepper_noise(image, prob=0.02)
        gaussian_noise = add_gaussian_noise(image, mean=0, std_dev=0.6)

        gaussian_filtered_salt = apply_gaussian_filter(salt_and_pepper_noise, 7, 1)
        gaussian_filtered_gauss = apply_gaussian_filter(gaussian_noise, 7, 1.7)

        # Сохранение результатов
        cv2.imwrite('salt_and_pepper_noise.jpg', salt_and_pepper_noise)
        cv2.imwrite('gaussian_noise.jpg', gaussian_noise)
        cv2.imwrite('gaussian_filtered_salt.jpg', gaussian_filtered_salt)
        cv2.imwrite('gaussian_filtered_gauss.jpg', gaussian_filtered_gauss)

        print("Обработка завершена. Результаты сохранены.")