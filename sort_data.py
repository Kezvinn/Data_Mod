import os
import shutil
# Define the folder path

# Loop through all files in the specified folder
# if not os.path.exists(test_path_destination):
#     os.makedirs(valid_path_destination)
# else:
#     print(os.path.isdir(valid_path_destination))


# Loop through all files in the specified input folder
# loop through 3 folder input and output
# modify labels and copy
def relabels(ip_parent, op_parent, sub_folder):
    new_first_char = ''
    for n in range(3):
        ip = os.path.join(ip_parent, sub_folder[n])
        op = os.path.join(op_parent, sub_folder[n])
        if not os.path.exists(op):
            os.makedirs(op)
        for filename in os.listdir(ip):
            if filename.endswith('.txt'):
                input_file_path = os.path.join(ip, filename)
                output_file_path = os.path.join(op, filename)
                try:
                    # Read the content of the file
                    with open(input_file_path, 'r') as file:
                        lines = file.readlines()

                    # Modify the lines
                    modified_lines = []
                    for line in lines:
                        if line:
                            # Get the first character and the rest of the line
                            first_char = line[0]
                            rest_of_line = line[1:]

                            # Modify the first character based on the condition
                            if first_char == '0':   # 1-> skip
                                new_first_char = '1'
                                # continue
                            # elif first_char == '0':
                                # new_first_char = '1'
                            # elif first_char == '2':     # 2 -> 1
                            #     new_first_char = '1'
                            # Construct the modified line
                            modified_line = new_first_char + rest_of_line
                            modified_lines.append(modified_line)
                        else:
                            modified_lines.append(line)

                    # Write the modified content to the output file
                    with open(output_file_path, 'w') as file:
                        file.writelines(modified_lines)

                    print(f"Labels in {filename} have been modified and saved to {output_file_path}.")
                except FileNotFoundError:
                    print(f"The file {filename} does not exist.")
                except Exception as e:
                    print(f"An error occurred while processing {filename}: {e}")
    print("Label modification complete for all .txt files in the input folder.")


# copy images
def copy_lbl(ip_parent, op_parent, sub_lbl):
    for n in range(3):
        ip = os.path.join(ip_parent, sub_lbl[n])
        op = os.path.join(op_parent, sub_lbl[n])
        if not os.path.exists(op):
            os.makedirs(op)
        for filename in os.listdir(ip):
            input_path = os.path.join(ip, filename)
            output_path = os.path.join(op, filename)
            try:
                # Copy the image file to the output directory
                shutil.copy(input_path, output_path)
                print(f"File {input_path} has been copied to {output_path}.")
            except FileNotFoundError:
                print(f"The file {input_path} does not exist.")
            except Exception as e:
                print(f"An error occurred while processing {input_path}: {e}")
    print("Labels copying complete for all specified image files.")


def copy_img(ip_parent, op_parent, sub_img):
    for n in range(3):
        ip = os.path.join(ip_parent, sub_img[n])
        op = os.path.join(op_parent, sub_img[n])
        if not os.path.exists(op):
            os.makedirs(op)
        for filename in os.listdir(ip):
            input_path = os.path.join(ip, filename)
            output_path = os.path.join(op, filename)
            try:
                # Copy the image file to the output directory
                shutil.copy(input_path, output_path)
                print(f"Image {input_path} has been copied to {output_path}.")
            except FileNotFoundError:
                print(f"The image file {input_path} does not exist.")
                continue
            except Exception as e:
                print(f"An error occurred while processing {input_path}: {e}")
    print("Image copying complete for all specified image files.")


def main():
    # E:\CapstoneB\dataset\fire ->  relabel: delete smoke-1, make smoke from 2-1 and copy images -> done
    # E:\CapstoneB\new_dataset\Used\continuous_fire.yolov8 -> copy image and labels -> done
    # E:\CapstoneB\new_dataset\Used\fire and smoke detector.v14i.yolov8 -> copy image and labels -> done
    # E:\CapstoneB\new_dataset\Used\Fire Smoke Detection.v3i.yolov8  -> copy image and labels -> done
    # E:\CapstoneB\new_dataset\Used\fire_and_smoke.yolov8 -> copy image and labels -> done
    # E:\CapstoneB\new_dataset\Used\FireDectection.v2i.yolov8 ->copy image and labels -> done
    ip_parent_dir = r'E:\CapstoneB\new_dataset\output_distribution'
    op_parent_dir = r'E:\CapstoneB\new_dataset\output_distribution'

    img_sub_path = [r"train\images",
                    r"test\images",
                    r"valid\images"]
    lbl_sub_path = [r"train\labels",
                    r"test\labels",
                    r"valid\labels"]
    relabels(ip_parent_dir, op_parent_dir, lbl_sub_path)
    # copy_img(ip_parent_dir, op_parent_dir, img_sub_path)
    # copy_lbl(ip_parent_dir, op_parent_dir, lbl_sub_path)


if __name__ == "__main__":
    main()

