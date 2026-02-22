import os
import numpy as np
import cv2
from PIL import Image
import time
import pandas as pd


def select_new_points(img, num_points=5, min_distance=50):
    """
    Выбор новых ключевых точек с минимальным расстоянием между ними
    """
    height, width = img.shape

    points = cv2.goodFeaturesToTrack(img,
                                     maxCorners=num_points * 3,
                                     qualityLevel=0.01,
                                     minDistance=min_distance,
                                     blockSize=7)

    if points is None:
        points = []
        step_x = width // (num_points + 1)
        step_y = height // (num_points + 1)
        for i in range(1, num_points + 1):
            for j in range(1, num_points + 1):
                if len(points) < num_points:
                    points.append([i * step_x, j * step_y])
        points = np.array(points, dtype=np.float32).reshape(-1, 1, 2)

    selected_points = points[:num_points]
    return selected_points.reshape(-1, 2)


def calculate_optical_flow_lucas_kanade(prev_img, curr_img, points, window_size=15):
    """
    Вычисление оптического потока Лукаса-Канаде для заданных точек
    """
    if len(points) == 0:
        return np.array([]), np.array([])

    prev_pts = np.array(points, dtype=np.float32).reshape(-1, 1, 2)

    next_pts, status, _ = cv2.calcOpticalFlowPyrLK(
        prev_img, curr_img, prev_pts, None,
        winSize=(window_size, window_size),
        maxLevel=3,
        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
    )

    good_new = next_pts[status == 1]
    good_old = prev_pts[status == 1]
    flow_vectors = good_new - good_old

    return good_new.reshape(-1, 2), flow_vectors.reshape(-1, 2)


def real_time_optical_flow(image_folder, output_csv, num_points=5):
    """
    Визуализация оптического потока в реальном времени
    """

    print("Запуск реального времени...")
    print("Управление:")
    print("  SPACE - пауза/продолжить")
    print("  ESC - выход")
    print("  R - перевыбрать точки")

    # Создаем CSV файл с заголовками для Excel
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        # точка с запятой как разделитель
        f.write("frame;image_name;point_id;x;y;u;v;magnitude;direction;status\n")

    image_files = [f for f in os.listdir(image_folder)
                   if f.startswith("orig_") and f.lower().endswith('.jpg')]
    image_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

    prev_img = None
    points = None
    paused = False

    colors = [(0, 255, 0), (0, 255, 255), (255, 255, 0),
              (255, 0, 255), (0, 165, 255)]

    for frame_idx, image_file in enumerate(image_files):
        if not paused:
            img_path = os.path.join(image_folder, image_file)

            try:
                with Image.open(img_path) as pil_img:
                    if pil_img.mode != 'RGB':
                        pil_img = pil_img.convert('RGB')

                    if pil_img.size != (640, 480):
                        pil_img = pil_img.resize((640, 480))

                    img_rgb = np.array(pil_img)
                    display_img = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
                    img_gray = cv2.cvtColor(display_img, cv2.COLOR_BGR2GRAY)
                    curr_img = img_gray

            except Exception as e:
                print(f"Ошибка загрузки {image_file}: {e}")
                continue

            if points is None or len(points) == 0:
                points = select_new_points(curr_img, num_points)
                prev_img = curr_img

                # Визуализация
                for i, (x, y) in enumerate(points):
                    color = colors[i % len(colors)]
                    cv2.circle(display_img, (int(x), int(y)), 5, color, -1)
                    cv2.putText(display_img, f"P{i}", (int(x) + 5, int(y)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                    window_size = 15
                    cv2.rectangle(display_img,
                                  (int(x) - window_size // 2, int(y) - window_size // 2),
                                  (int(x) + window_size // 2, int(y) + window_size // 2),
                                  color, 1)

                # Записываем начальные точки
                with open(output_csv, 'a', newline='', encoding='utf-8') as f:
                    for i, (x, y) in enumerate(points):
                        f.write(f"{frame_idx};{image_file};{i};{x:.1f};{y:.1f};0;0;0;0;initial\n")

            else:
                new_points, flow_vectors = calculate_optical_flow_lucas_kanade(
                    prev_img, curr_img, points)

                # Визуализация
                for i, ((x_old, y_old), (x_new, y_new), (u, v)) in enumerate(
                        zip(points, new_points, flow_vectors)):
                    color = colors[i % len(colors)]

                    cv2.circle(display_img, (int(x_old), int(y_old)), 3, color, -1)
                    """
                    cv2.arrowedLine(display_img,
                                    (int(x_old), int(y_old)),
                                    (int(x_new), int(y_new)),
                                    color, 2, tipLength=0.3)
                    cv2.circle(display_img, (int(x_new), int(y_new)), 5, color, -1)
                    """
                    info = f"P{i}: U={u:.1f}, V={v:.1f}"
                    cv2.putText(display_img, info, (int(x_new) + 10, int(y_new)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

                    window_size = 15
                    cv2.rectangle(display_img,
                                  (int(x_new) - window_size // 2, int(y_new) - window_size // 2),
                                  (int(x_new) + window_size // 2, int(y_new) + window_size // 2),
                                  color, 1)

                points = new_points
                prev_img = curr_img

                # Записываем данные
                with open(output_csv, 'a', newline='', encoding='utf-8') as f:
                    for i, ((x, y), (u, v)) in enumerate(zip(points, flow_vectors)):
                        magnitude = np.sqrt(u ** 2 + v ** 2)
                        direction = np.degrees(np.arctan2(v, u))


                        f.write(f"{frame_idx};{image_file};{i};{x:.1f};{y:.1f};"
                                f"{u:.3f};{v:.3f};{magnitude:.3f};{direction:.1f};tracked\n")

                        # ВАРИАНТ 2: Табуляция
                        # f.write(f"{frame_idx}\t{image_file}\t{i}\t{x:.1f}\t{y:.1f}\t"
                        #         f"{u:.3f}\t{v:.3f}\t{magnitude:.3f}\t{direction:.1f}\tracked\n")

            # Информационная панель
            info_text = [
                f"Frame: {frame_idx}/{len(image_files)}",
                f"File: {image_file}",
                f"Points: {len(points) if points is not None else 0}/{num_points}",
                "SPACE: pause, R: reset points, ESC: exit"
            ]

            for i, text in enumerate(info_text):
                cv2.putText(display_img, text, (10, 30 + i * 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                cv2.putText(display_img, text, (10, 30 + i * 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

            cv2.imshow('Optical Flow - Lucas-Kanade', display_img)

            key = cv2.waitKey(30) & 0xFF
            if key == 27:
                break
            elif key == 32:
                paused = not paused
                print("Пауза" if paused else "Продолжить")
            elif key == ord('r'):
                points = None
                print("Перевыбор точек")

        else:
            key = cv2.waitKey(100) & 0xFF
            if key == 27:
                break
            elif key == 32:
                paused = not paused
                print("Продолжить")
            elif key == ord('r'):
                points = None
                paused = False
                print("Перевыбор точек")

    cv2.destroyAllWindows()
    print(f"Данные сохранены в: {output_csv}")
    return True


def process_optical_flow_batch(image_folder, output_csv, num_points=5):
    """
    Пакетная обработка без визуализации в реальном времени
    """

    print(f"Анализ оптического потока для {num_points} точек")

    # Создаем CSV файл с заголовками для Excel
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        f.write("frame;image_name;point_id;x;y;u;v;magnitude;direction;status\n")

    image_files = [f for f in os.listdir(image_folder)
                   if f.startswith("orig_") and f.lower().endswith('.jpg')]
    image_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

    prev_img = None
    points = None

    for frame_idx, image_file in enumerate(image_files):
        print(f"Обработка кадра {frame_idx + 1}/{len(image_files)}: {image_file}")

        img_path = os.path.join(image_folder, image_file)

        try:
            with Image.open(img_path) as pil_img:
                img_gray = pil_img.convert('L')
                if img_gray.size != (640, 480):
                    img_gray = img_gray.resize((640, 480))
                curr_img = np.array(img_gray, dtype=np.uint8)
        except Exception as e:
            print(f"Ошибка загрузки {image_file}: {e}")
            continue

        if points is None or len(points) == 0:
            points = select_new_points(curr_img, num_points)
            prev_img = curr_img

            with open(output_csv, 'a', newline='', encoding='utf-8') as f:
                for i, (x, y) in enumerate(points):
                    f.write(f"{frame_idx};{image_file};{i};{x:.1f};{y:.1f};0;0;0;0;initial\n")
            continue

        new_points, flow_vectors = calculate_optical_flow_lucas_kanade(
            prev_img, curr_img, points)

        tracked_count = len(new_points)

        if tracked_count < num_points:
            print(f"Потеряно {num_points - tracked_count} точек, выбираем новые")

            if tracked_count > 0:
                points = new_points
            else:
                points = np.array([])

            additional_points_needed = num_points - tracked_count
            new_additional_points = select_new_points(curr_img, additional_points_needed)

            if len(points) > 0:
                points = np.vstack([points, new_additional_points])
            else:
                points = new_additional_points

            with open(output_csv, 'a', newline='', encoding='utf-8') as f:
                for i in range(tracked_count, len(points)):
                    x, y = points[i]
                    f.write(f"{frame_idx};{image_file};{i};{x:.1f};{y:.1f};0;0;0;0;new_point\n")

        else:
            points = new_points

        with open(output_csv, 'a', newline='', encoding='utf-8') as f:
            for i, ((x, y), (u, v)) in enumerate(zip(points, flow_vectors)):
                magnitude = np.sqrt(u ** 2 + v ** 2)
                # Учитываем что v положительное = движение вниз (отрицательное по Y)
                direction = np.degrees(np.arctan2(-v, u))  # Инвертируем v

                f.write(f"{frame_idx};{image_file};{i};{x:.1f};{y:.1f};"
                        f"{u:.3f};{v:.3f};{magnitude:.3f};{direction:.1f};tracked\n")

        prev_img = curr_img

    print(f"\nОбработка завершена")
    print(f"Файл: {output_csv}")
    return True


# Запуск программы
if __name__ == "__main__":
    image_folder = r"E:\VUZ\Science\Обработка с самолета"
    output_csv = "optical_flow_results.csv"

    print("Выберите режим:")
    print("1 - Режим реального времени с визуализацией")
    print("2 - Пакетная обработка (быстрее)")

    choice = input("Введите 1 или 2: ").strip()

    if choice == "1":
        success = real_time_optical_flow(image_folder, output_csv, num_points=5)
    else:
        success = process_optical_flow_batch(image_folder, output_csv, num_points=5)

    if success:
        print(f"Анализ оптического потока завершен успешно")

        # Показываем пример данных
        try:
            # Читаем CSV с указанием разделителя
            sample_df = pd.read_csv(output_csv, delimiter=';', nrows=10)
            print("\nПример данных оптического потока:")
            print(sample_df)

            # Сохраняем также в формате Excel
            excel_file = output_csv.replace('.csv', '.xlsx')
            full_df = pd.read_csv(output_csv, delimiter=';')
            full_df.to_excel(excel_file, index=False)
            print(f"Данные сохранены: {excel_file}")

        except Exception as e:
            print(f"Ошибка при чтении CSV: {e}")
    else:
        print(f"Анализ завершен с ошибками!")