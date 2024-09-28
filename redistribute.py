import os
import random
import shutil
import zipfile

'''
def get_files_with_extension(folder, extension):
    return [f for f in os.listdir(folder) if f.endswith(extension)]


def match_files(image_folder, text_folder):
    extensions = ('jpg', 'jpeg', 'png', 'gif', 'bmp')  # extension of file
    images = get_files_with_extension(image_folder, extensions)
    texts = get_files_with_extension(text_folder, '.txt')

    matched_pairs = []
    for image in images:
        base_name = os.path.splitext(image)[0]
        corresponding_text = f"{base_name}.txt"
        if corresponding_text in texts:
            matched_pairs.append((image, corresponding_text))

    return matched_pairs


def distribute_files_percent(pairs, image_folder, label_folder, output_folder):
    random.shuffle(pairs)
    total_pairs = len(pairs)

    split_80 = int(total_pairs * 0.80)
    split_95 = int(total_pairs * 0.95)

    # split into 80, 15, 5 for train, valid, test accordingly
    train_pairs = pairs[:split_80]
    valid_pairs = pairs[split_80:split_95]
    test_pairs = pairs[split_95:]

    def copy_files(pair, img_folder, lb_folder, output_image_folder, output_label_folder):
        os.makedirs(output_image_folder, exist_ok=True)
        os.makedirs(output_label_folder, exist_ok=True)

        for image, text in pair:
            shutil.copy(os.path.join(img_folder, image), os.path.join(output_image_folder, image))
            shutil.copy(os.path.join(lb_folder, text), os.path.join(output_label_folder, text))

    copy_files(train_pairs, image_folder, label_folder, os.path.join(output_folder, 'train', 'images'),
               os.path.join(output_folder, 'train', 'labels'))
    copy_files(valid_pairs, image_folder, label_folder, os.path.join(output_folder, 'valid', 'images'),
               os.path.join(output_folder, 'valid', 'labels'))
    copy_files(test_pairs, image_folder, label_folder, os.path.join(output_folder, 'test', 'images'),
               os.path.join(output_folder, 'test', 'labels'))
'''


def get_file_from_zip(zip_ref, extension):
    return [f for f in zip_ref.namelist() if f.endswith(extension)]


def match_files_from_zip(zip_file, max_pairs):
    print(f"Zip file: {zip_file}")
    extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')  # Add any other extensions you need
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        images = get_file_from_zip(zip_ref, extensions)
        texts = get_file_from_zip(zip_ref, '.txt')

        print(f"Found {len(images)} images in {zip_ref}")
        print(f"Found {len(texts)} text files in {zip_ref}")

        random.shuffle(images)
        matched_pairs = []

        for image in images:
            # only the name of the file in the sub folder
            base_name = os.path.splitext(os.path.basename(image))[0]
            corresponding_text = [text for text in texts if os.path.splitext(os.path.basename(text))[0] == base_name]
            # print(f'corresponding text: {corresponding_text}')
            if corresponding_text:
                matched_pairs.append((image, corresponding_text[0]))
                # print(f"Matched: {image} with {corresponding_text}")
            if len(matched_pairs) >= max_pairs:
                break
    print("Completed matching pairs")
    return matched_pairs


def create_directories(dirs):
    for dir_ in dirs:
        if not os.path.exists(dir_):
            os.makedirs(dir_)


def move_files(zip_file_, pairs_, output_folder, category):
    print(f'output_folder: {output_folder}')
    image_dir = os.path.join(output_folder, category, 'images')
    label_dir = os.path.join(output_folder, category, 'labels')

    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(label_dir, exist_ok=True)

    print(f'image path: {image_dir}')
    print(f'label_path: {label_dir}')

    with zipfile.ZipFile(zip_file_, 'r') as zip_ref:
        for image, text in pairs_:
        #     zip_ref.extract(image, image_dir)
        #     zip_ref.extract(text, label_dir)
        #
        #     print(f"Extracted {image} to {image_dir}")
        #     print(f"Extracted {text} to {label_dir}")
            base_image_name = os.path.basename(image)
            base_text_name = os.path.basename(text)

            image_path = os.path.join(image_dir, base_image_name)
            text_path = os.path.join(label_dir, base_text_name)

            with zip_ref.open(image) as img_file:
                with open(image_path, 'wb') as out_img_file:
                    out_img_file.write(img_file.read())

            with zip_ref.open(text) as txt_file:
                with open(text_path, 'wb') as out_txt_file:
                    out_txt_file.write(txt_file.read())

            print(f"Moved {image} to {image_path}")
            print(f"Moved {text} to {text_path}")


def distribute_file_quantity(zip_file, pairs, output_folder,  train_qty, val_qty, test_qty):
    random.shuffle(pairs)

    types = ['train', 'valid', 'test']

    train_pairs = pairs[:train_qty]
    val_pairs = pairs[train_qty:train_qty + val_qty]
    test_pairs = pairs[train_qty + val_qty:train_qty + val_qty + test_qty]

    move_files(zip_file, train_pairs, output_folder, types[0])
    move_files(zip_file, val_pairs, output_folder, types[1])
    move_files(zip_file, test_pairs, output_folder, types[2])
    print("Completed distributed pairs")

# ===========Used for distribute file==================================


def get_files_with_extension(folder, extensions):
    return [f for f in os.listdir(folder) if f.lower().endswith(extensions)]


def is_file_empty(file_path):
    """Check if a file is empty."""
    return os.path.getsize(file_path) == 0


def match_files(main_folder):   # match from image to label
    extensions = ('jpg', 'jpeg', 'png', 'gif', 'bmp')
    matched_pairs = []

    for subfolder in ['train', 'test', 'valid']:
        image_folder = os.path.join(main_folder, subfolder, 'images')
        label_folder = os.path.join(main_folder, subfolder, 'labels')

        images = get_files_with_extension(image_folder, extensions)
        texts = get_files_with_extension(label_folder, '.txt')

        for image in images:
            base_name = os.path.splitext(image)[0]
            corresponding_text = f"{base_name}.txt"

            label_path = os.path.join(label_folder, corresponding_text)
            if corresponding_text in texts and is_file_empty(label_path):
                matched_pairs.append((os.path.join(subfolder, 'images', image),
                                      os.path.join(subfolder, 'labels', corresponding_text)))
        # for txt in texts:
        #     base_name = os.path.splitext(txt)[0]
        #     corresponding_img = f"{base_name}.jpg"
        #     if corresponding_img in images and is_file_empty(txt):
        #         matched_pairs.append((os.path.join(subfolder, 'labels', txt),
        #                               os.path.join(subfolder, 'images', corresponding_img)))

    return matched_pairs


def distribute_files_percent(pairs, ip_folder, output_folder):
    random.shuffle(pairs)
    total_pairs = len(pairs)
    print(f"total pairs: {total_pairs} pairs")

    split_80 = int(total_pairs * 0.80)
    split_95 = int(total_pairs * 0.95)

    train_pairs = pairs[:split_80]
    valid_pairs = pairs[split_80:split_95]
    test_pairs = pairs[split_95:]

    # print(f"length of train_pairs: {len(train_pairs)}")
    # print(f"length of valid_pairs: {len(valid_pairs)}")
    # print(f"length of test_pairs: {len(test_pairs)}")

    def copy_files(pair, input_folder, output_image_folder, output_label_folder):
        # print(f"main folder: {len(main_folder)}")
        os.makedirs(output_image_folder, exist_ok=True)
        os.makedirs(output_label_folder, exist_ok=True)
        # count = 0
        for image, text in pair:
            shutil.copy(os.path.join(ip_folder, image),
                        os.path.join(output_image_folder, os.path.basename(image)))
            shutil.copy(os.path.join(input_folder, text),
                        os.path.join(output_label_folder, os.path.basename(text)))
            # count += 1
        # print(f"Copied {count} images and {count} labels")
    copy_files(train_pairs, ip_folder,
               os.path.join(output_folder, 'train', 'images'),
               os.path.join(output_folder, 'train', 'labels'))
    copy_files(valid_pairs, ip_folder,
               os.path.join(output_folder, 'valid', 'images'),
               os.path.join(output_folder, 'valid', 'labels'))
    copy_files(test_pairs, ip_folder,
               os.path.join(output_folder, 'test', 'images'),
               os.path.join(output_folder, 'test', 'labels'))
    total_copies = len(train_pairs) + len(valid_pairs) + len(test_pairs)
    print(f"Total copies: {total_copies}")
# ========================================================================


def main():
    # input
    input_zip = r'E:\CapstoneB\new_dataset\New\unsort'
    # output
    output_folder = r'E:\CapstoneB\new_dataset\New\sort'

    matched_pair = match_files(input_zip)
    distribute_files_percent(matched_pair, input_zip, output_folder)
    print("Completed")

# used to extract and distribute data into a folder
#     train_qty = int(4000)
#     valid_qty = int(750)
#     test_qty = int(250)
#
#     matched_pairs = match_files_from_zip(input_zip, 5000)
#     print(f"Total matched pairs: {len(matched_pairs)}")
#
#     total_qty = train_qty + valid_qty + test_qty
#
#     if total_qty > len(matched_pairs):
#         print("The total number of specified files exceeds the number of available matched pairs.")
#         return
#
#     # distribution on quantity
#     distribute_file_quantity(input_zip, matched_pairs, output_folder, train_qty, valid_qty, test_qty)
#     print(f"Distributed {train_qty} pairs for training, {valid_qty} pairs for validation, and {test_qty} "
#           f"pairs for testing.")

    # matched_pairs = match_files_from_zip(input_image_folder, input_label_folder)

    # distribute on percentage
    # distribute_files_percent(matched_pairs, input_image_folder, input_label_folder, output_folder)
    # print(f"Distributed {len(matched_pairs)} pairs into train (80%), val (15%), and test (5%) sets.")


if __name__ == "__main__":
    main()
