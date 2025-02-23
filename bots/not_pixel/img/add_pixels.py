from PIL import Image
import os


def create_image_with_selected_area(src_image_path, dst_image_path, a, b, fill_color):
    # Если файл существует, откройте его и получите изображение
    if os.path.exists(dst_image_path):
        existing_image = Image.open(dst_image_path).convert("RGB")
    else:
        # Если файла нет, создаем новое пустое изображение с заданным цветом
        existing_image = Image.new("RGB", (1024, 1024), fill_color)

    # Создаем новое изображение с цветом fill_color
    new_image = Image.new("RGB", (1024, 1024), fill_color)

    # Переносим пиксели из existing_image, кроме тех, что закрашены в fill_color
    for x in range(1024):
        for y in range(1024):
            if existing_image.getpixel((x, y)) != fill_color:
                new_image.putpixel((x, y), existing_image.getpixel((x, y)))

    # Переносим выбранные пиксели из src_image в new_image
    src_image = Image.open(src_image_path).convert("RGB")
    for x in range(a[0], b[0]):
        for y in range(a[1], b[1]):
            pixel = src_image.getpixel((x, y))  # Получаем пиксель из исходного изображения
            new_image.putpixel((x, y), pixel)  # Устанавливаем пиксель в новое изображение

    # Сохраняем новое изображение
    new_image.save(dst_image_path)
    print(f'Новое изображение сохранено как: {dst_image_path}')


if __name__ == "__main__":
    # Путь к исходному изображению
    src_image_path = 'download_img.png'
    # Путь к новому изображению
    dst_image_path = 'ready_image.png'

    # Ввод координат (левая верхняя и правая нижняя точка)
    left_top = input("Введите координату X, Y левого верхнего угла: ").split(', ')
    top_left_x, top_left_y = int(left_top[0]), int(left_top[1])
    # top_left_x = int(input("Введите координату X левого верхнего угла: "))
    # top_left_y = int(input("Введите координату Y левого верхнего угла: "))
    right_bottom = input("Введите координату X, Y правого нижнего угла: ").split(', ')
    bottom_right_x, bottom_right_y = int(right_bottom[0]), int(right_bottom[1])
    # bottom_right_y = int(input("Введите координату Y правого нижнего угла: "))
    #
    # Проверка на допустимость координат
    if (0 <= top_left_x < 1024 and 0 <= top_left_y < 1024 and
            0 < bottom_right_x <= 1024 and 0 < bottom_right_y <= 1024 and
            top_left_x < bottom_right_x and top_left_y < bottom_right_y):

        # Цвет заполнения
        fill_color = (153, 21, 21)  # Код цвета #991515 в формате RGB
        create_image_with_selected_area(src_image_path, dst_image_path,
                                        (top_left_x, top_left_y),
                                        (bottom_right_x, bottom_right_y),
                                        fill_color)
    else:
        print("Ошибка: Проверьте корректность введенных координат.")