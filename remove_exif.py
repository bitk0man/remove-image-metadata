import os
from PIL import Image
import pillow_heif

# Регистрируем поддержку HEIC/HEIF
pillow_heif.register_heif_opener()

def remove_metadata_in_place():
    """
    Сканирует все файлы в текущей директории.
    Попытается открыть каждый файл как изображение
    и, если открылось, удаляет возможные метаданные,
    перезаписывая тот же файл на месте.
    """
    # Получим список всех файлов в папке
    all_files = os.listdir('.')
    # Для отладки выведем список всех файлов
    print("Все файлы в папке:")
    for file in all_files:
        print("  " + file)
    print("\n")

    # Фильтр: Только те, что можно открыть с помощью Pillow как изображение
    image_files = []
    for file in all_files:
        # Пробуем открыть файл как изображение
        try:
            with Image.open(file) as img:
                # Если открыли без ошибок, считаем, что это изображение
                image_files.append(file)
        except:
            # Если не получилось открыть, пропускаем
            pass

    if not image_files:
        print("Не обнаружено ни одного файла, который PIL распознаёт как изображение!")
        return
    else:
        print("Найденные изображения:")
        for img_name in image_files:
            print("  " + img_name)
        print("\nНачинаем обработку...\n")

    # Обработка
    for filename in image_files:
        try:
            old_size = os.path.getsize(filename)
            # Открываем изображение
            with Image.open(filename) as img:
                # Проверяем, есть ли EXIF (актуально для JPEG, TIFF, WEBP, HEIC...)
                exif_data = img.info.get('exif')

                # Считываем пиксели
                data = list(img.getdata())
                
                # Создаём «чистую» копию
                img_no_meta = Image.new(img.mode, img.size)
                img_no_meta.putdata(data)

                # Перезаписываем исходный файл
                # Предпочтительно указывать format=img.format, чтобы сохранить исходный формат
                # (включая HEIC, если оно было определено).
                img_no_meta.save(filename, format=img.format)

            new_size = os.path.getsize(filename)

            if exif_data:
                print(
                    f"Файл: {filename}\n"
                    f"  Был EXIF, размер до: {old_size} байт, "
                    f"после: {new_size} байт\n"
                    "  Метаданные (EXIF) удалены.\n"
                )
            else:
                print(
                    f"Файл: {filename}\n"
                    f"  EXIF (или других метаданных) не обнаружено, "
                    f"размер был {old_size}, стал {new_size} байт\n"
                )

        except Exception as e:
            print(f"Ошибка при обработке «{filename}»: {e}\n")

if __name__ == "__main__":
    remove_metadata_in_place()
    print("Обработка завершена.")
