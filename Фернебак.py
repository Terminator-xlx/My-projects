import cv2
import numpy as np
import time
import os

def calculate_ferneback_flow(prev_frame, next_frame):
    # Преобразуем кадры в оттенки серого
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    next_gray = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)

    # Вычисляем оптический поток с помощью алгоритма Фернебака
    flow = cv2.calcOpticalFlowFarneback(prev_gray, next_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    return flow

def visualize_flow_farneback(frame, flow, step=16):
    h, w = frame.shape[:2]
    y, x = np.mgrid[step / 2:h:step, step / 2:w:step].reshape(2, -1).astype(int)
    fx, fy = flow[y, x].T

    lines = np.vstack([x, y, x + fx, y + fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)

    vis = frame.copy()
    cv2.polylines(vis, lines, 0, (0, 255, 0))

    for (x1, y1), (x2, y2) in lines:
        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)

    return vis

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
    print('Разрешение кадра: ', frame_width, 'x', frame_height)

    # Создаем объект для записи видео
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output_video.mp4', fourcc, fps, (frame_width, frame_height))

    # Открываем файл для записи данных
    with open('ferneback_flow_data.txt', 'w') as file:
        # Считываем первый кадр
        ret, prev_frame = cap.read()
        if not ret:
            print("Ошибка: Не удалось прочитать первый кадр.")
            return

        frame_number = 1
        start_time = time.time()  # Запускаем секундомер

        while True:
            # Считываем следующий кадр
            ret, next_frame = cap.read()
            if not ret:
                print("Ошибка: Не удалось прочитать кадр.")
                break

            # Вычисляем оптический поток
            flow = calculate_ferneback_flow(prev_frame, next_frame)

            # Визуализация оптического потока
            vis = visualize_flow_farneback(next_frame, flow)

            # Записываем данные в файл
            elapsed_time = time.time() - start_time
            file.write(f'Frame {frame_number}; Time: {elapsed_time:.2f}s\n')

            for y in range(0, frame_height, 10):  # Шаг 10 для уменьшения количества данных
                for x in range(0, frame_width, 10):
                    fx, fy = flow[y, x]
                    file.write(f'({x:4}, {y:4}) dx: {fx:.2f} dy: {fy:.2f}\n')

            file.write('\n')

            # Записываем обработанный кадр в видеофайл
            out.write(vis)

            # Обновляем предыдущий кадр
            prev_frame = next_frame

            # Отображаем текущий кадр
            cv2.imshow('Video Stream', vis)

            # Выход по нажатию клавиши 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            frame_number += 1

        cap.release()
        out.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = 'Nascar.gif'  # Укажите путь к вашему видеофайлу или гифке
    main(video_path)