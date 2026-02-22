import cv2
import numpy as np
import time
import os

def calculate_lucas_kanade_flow(prev_frame, next_frame, points_to_track):
    # Преобразуем кадры в оттенки серого
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    next_gray = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)

    # Вычисляем оптический поток с помощью алгоритма Лукаса-Канаде
    new_points, status, error = cv2.calcOpticalFlowPyrLK(prev_gray, next_gray, points_to_track, None)

    return new_points, status, error

def main(video_path):
    # Проверяем существование файла
    if not os.path.exists(video_path):
        print(f"Ошибка: Файл {video_path} не найден.")
        return

    # Открываем видеофайл или гифку
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Ошибка: Не удалось открыть видеофайл или гифку.")
        return

    # Запрашиваем разрешение кадра
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    wait_time = int(1000/fps)
    print('Разрешение кадра: ', frame_width, 'x', frame_height)

    # Инициализация объекта для записи видео
    output_video_path = 'output_video.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, 30.0, (frame_width, frame_height))

    # Открываем файл для записи данных
    with open('lucas_kanade_flow_data.txt', 'w') as file:
        # Считываем первый кадр
        ret, prev_frame = cap.read()
        if not ret:
            print("Ошибка: Не удалось прочитать первый кадр.")
            return

        # Выбираем точки для отслеживания
        points_to_track = cv2.goodFeaturesToTrack(cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY), maxCorners=100, qualityLevel=0.01, minDistance=10)

        frame_number = 1
        start_time = time.time()  # Запускаем секундомер

        while True:
            # Считываем следующий кадр
            ret, next_frame = cap.read()
            if not ret:
                print("Ошибка: Не удалось прочитать кадр.")
                break

            # Вычисляем оптический поток
            new_points, status, error = calculate_lucas_kanade_flow(prev_frame, next_frame, points_to_track)

            # Записываем данные в файл
            elapsed_time = time.time() - start_time
            file.write(f'Frame {frame_number}; Time: {elapsed_time:.2f}s\n')

            for i, (new, old) in enumerate(zip(new_points, points_to_track)):
                a, b = new.ravel()
                c, d = old.ravel()
                file.write(f'Point ({c:4}, {d:4}) dx: {a-c:.2f} dy: {b-d:.2f}\n')

                # Отображаем отслеживаемые точки на кадре
                next_frame = cv2.circle(next_frame, (int(a), int(b)), 5, (0, 255, 0), -1)

            file.write('\n')

            # Обновляем предыдущий кадр и точки для отслеживания
            prev_frame = next_frame.copy()
            points_to_track = new_points

            # Записываем обработанный кадр в видео
            out.write(next_frame)

            # Отображаем текущий кадр
            cv2.imshow('Video Stream', next_frame)

            # Выход по нажатию клавиши 'q'
            if cv2.waitKey(wait_time) & 0xFF == ord('q'):
                break

            frame_number += 1

        cap.release()
        out.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = 'Nascar.gif'  # Укажите путь к вашему видеофайлу или гифке
    main(video_path)