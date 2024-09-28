import os
import shutil
import random
import sys


def get_files_with_extension(folder, extensions):
    return [f for f in os.listdir(folder) if f.lower().endswith(extensions)]


def match_files(main_folder):
    extensions = ('jpg', 'jpeg', 'png', 'gif', 'bmp')
    matched_pairs = []
    count = 0
    count_2 = 0

    for subfolder in ['train', 'test', 'valid']:
        image_folder = os.path.join(main_folder, subfolder, 'images')
        label_folder = os.path.join(main_folder, subfolder, 'labels')

        # image_folder = os.path.join(main_folder, 'images')
        # label_folder = os.path.join(main_folder, 'labels')

        images = get_files_with_extension(image_folder, extensions)
        texts = get_files_with_extension(label_folder, '.txt')
        lines = []
        for image in images:
            base_name = os.path.splitext(image)[0]
            corresponding_text = f"{base_name}.txt"
            pth2lbl = os.path.join(label_folder, corresponding_text)
            # print(f"path to label: {pth2lbl}")
            if corresponding_text in texts:
                # new part
                with open(pth2lbl, 'r') as file:
                    content = file.read()
                    # print(f"content: {content}")
                    if content != '':
                        matched_pairs.append((os.path.join(subfolder, 'images', image),
                                              os.path.join(subfolder, 'labels', corresponding_text)))
                        count += 1
                    elif content == '':
                        count_2 += 1
                    # for lines in content:
                    #     lines = content.split('\n')
                    #     # print(f"line: {lines}")
                    #     if not lines:
                    #         continue
                    # print(f"line: {lines}")
                    # for first_char in lines:
                    #     first_char = lines[0][0]
                        # print(f"first_char: {first_char}")

                        # rest_of_line = lines[1:]
                        # if first_char == '0':   # smoke = 1, fire = 0
                            # matched_pairs.append((os.path.join(subfolder, 'images', image),
                            #                       os.path.join(subfolder, 'labels', corresponding_text)))
                            # count += 1
                        # elif first_char == '':
                        #     continue
    print(f"count = {count}")
    print(f"count_2 = {count_2}")
    print(f"sum: {count+count_2}")
    return matched_pairs


def move_files(input_folder, pairs_, output_folder, category):
    count = 0
    # print(f"input folder: {input_folder}")
    # print(f'Output folder: {output_folder}')
    image_dir = os.path.join(output_folder, category, 'images')
    label_dir = os.path.join(output_folder, category, 'labels')
    # print(f"img_dir = {image_dir}")
    # print(f"label_dir = {label_dir}")
    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(label_dir, exist_ok=True)

    # print(f'Image path: {image_dir}')
    # print(f'Label path: {label_dir}')
    print(f"length of pair: {len(pairs_)}")
    for image, text in pairs_:
        # Get the base names of the image and text files
        base_image_name = os.path.basename(image)
        base_text_name = os.path.basename(text)

        # Define the source paths
        image_path = os.path.join(input_folder, image)
        text_path = os.path.join(input_folder, text)
        print(f"image_path = {image_path}")
        print(f"text_path = {text_path}")
        # Define the destination paths
        dest_image_path = os.path.join(image_dir, base_image_name)
        dest_text_path = os.path.join(label_dir, base_text_name)

        # Copy the files
        shutil.copy(image_path, dest_image_path)
        shutil.copy(text_path, dest_text_path)
        count += 1
        print(f"Copy {image} to {dest_image_path}")
        print(f"Copy {text} to {dest_text_path}")
    print(f"Copied {count}")

def distribute_file_quantity(input_folder, pairs, output_folder, train_qty, val_qty, test_qty):
    random.shuffle(pairs)
    types = ['train', 'valid', 'test']
    print(f"length of pairs: {len(pairs)}")
    train_pairs = pairs[:train_qty]
    val_pairs = pairs[test_qty:val_qty+44]
    test_pairs = pairs[val_qty:val_qty+44]

    move_files(input_folder, train_pairs, output_folder, types[0])
    move_files(input_folder, val_pairs, output_folder, types[1])
    move_files(input_folder, test_pairs, output_folder, types[2])


    print("Completed distributed pairs")


def main():
    ip_folder = r"E:\CapstoneB\new_dataset\custom_data_smoke_only"
    op_folder = r"E:\CapstoneB\new_dataset\output_distribution"
    matched_pair = match_files(ip_folder)   # matched with classes only 0=fire or 1=smoke
    # for pair in matched_pair:
    #     print(f"matched pair: {pair}")
    output_img = r"E:\CapstoneB\new_dataset\extractdata_op\fire\images"
    output_label = r"E:\CapstoneB\new_dataset\extractdata_op\fire\labels"

    distribute_file_quantity(ip_folder, matched_pair, op_folder, 924, 205, 44)

    # match file that have label, ignore file that have no label
    # relabel the smoke from 0 to 1
    # distribute the image and label into the tempo dataset
    '''
    # copy file out
    count = 0
    for image, text in matched_pair:
        print(f"count = {count}")
        count += 1
        shutil.copy(os.path.join(ip_folder, image),
                    os.path.join(output_img, os.path.basename(image)))
        shutil.copy(os.path.join(ip_folder, text),
                    os.path.join(output_label, os.path.basename(text)))
        if count > 44:
            break
        else:
            count += 1
    '''


if __name__ == "__main__":
    main()

