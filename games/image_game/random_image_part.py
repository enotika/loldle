from PIL import Image
import random
x1,y1,x2,y2 = 0,0,0,0
def crop_random_patch(image_path, patch_width, patch_height):
    # Открываем изображение
    global x1,y1,x2,y2
    image = Image.open(image_path)
    
    # Получаем размеры исходного изображения
    img_width, img_height = image.size
    print(image.size)
    # Проверяем, чтобы размеры вырезаемого фрагмента не были больше изображения
    if patch_width > img_width or patch_height > img_height:
        print("Размер фрагмента больше изображения.")
        return None

    # Генерируем случайные координаты верхнего левого угла фрагмента
    left = random.randint(200, img_width - 400)
    top = random.randint(200, img_height - 400)
    # while left < 400 or left + patch_width + 400 > img_width:
    #     left = random.randint(0, img_width - patch_width)
    # while top < 400 or top + patch_height + 400 > img_height:
    #     top = random.randint(0, img_height - patch_height)
    # Определяем координаты правого нижнего угла фрагмента
    right = left + patch_width
    bottom = top + patch_height
    
    x1 = left
    y1 = top
    x2 = right
    y2 = bottom

    # Вырезаем фрагмент
    cropped_image = image.crop((left, top, right, bottom))
    
    # Возвращаем вырезанный фрагмент
    return cropped_image

def expand_img(image_path, patch_width, patch_height, expand_sz):
    # Открываем изображение
    global x1,y1,x2,y2
    image = Image.open(image_path)
    patch_width+=expand_sz
    patch_height+=expand_sz
    
    # Получаем размеры исходного изображения
    img_width, img_height = image.size
    # Проверяем, чтобы размеры вырезаемого фрагмента не были больше изображения
    if patch_width > img_width or patch_height > img_height:
        print("Размер фрагмента больше изображения.")
        return None

    # Генерируем случайные координаты верхнего левого угла фрагмента
    left = x1 - expand_sz
    top = y1 - expand_sz
    
    # Определяем координаты правого нижнего угла фрагмента
    right = x2 + expand_sz
    bottom = y2 + expand_sz
    print(left, top, right, bottom)
    
    # Вырезаем фрагмент
    cropped_image = image.crop((left, top, right, bottom))
    
    # Возвращаем вырезанный фрагмент
    return cropped_image

# # Пример использования
# image_path = '/home/user/practice/data/champ_images/Ренгар/Ренгар_skins/Rengar_30.jpg'  # Укажите путь к изображению
# patch_width = 200  # Ширина фрагмента
# patch_height = 200  # Высота фрагмента

# # Получаем случайный фрагмент
# cropped_img = crop_random_patch(image_path, patch_width, patch_height)

# if cropped_img:
#     # Сохраняем или показываем вырезанный фрагмент
#     cropped_img.show()  # Показываем изображение
#     cropped_img.save('cropped_image.jpg')  # Сохраняем вырезанный фрагмент

# sz_exp = 0


# while True:
#     exp = int(input("expand?: "))
#     if exp != 0:
#         sz_exp+=exp
#         expanded_img=expand_img(image_path, patch_width, patch_height, sz_exp)
#         if expanded_img:
#             # Сохраняем или показываем вырезанный фрагмент
#             expanded_img.show()  # Показываем изображение
#             expanded_img.save('expanded_image.jpg')  # Сохраняем вырезанный фрагмент
#         sz_exp+=20