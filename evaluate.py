import os
import shutil
import redistribute
ip_path = r'C:\Users\nhatn\Downloads\tempo2.0\tempo2.0'
# ip_path = r'E:\CapstoneB\new_dataset\custom_data_2.0'
sub_path = [r'train\labels',
            r'test\labels',
            r'valid\labels']
no_lbl_path = r'E:\CapstoneB\new_dataset\tempo\No_labels'


def open_folder(path, subpath):
    directory = os.path.join(path, subpath)
    return directory


def print_result(subpaths, c0, c1, t, file, f_fire, f_smoke, f_both, f_empty):
    print(f"Folder: {ip_path}")
    print("+=======================================================================================+")
    print(f"|\t\t| Instances \t\t\t| Images with instances \t\t|")
    print("+---------------+---------------+---------------+-------+-------+-------+---------------+")
    print("| Directory\t| Fire\t| Smoke\t|    Totals\t| Files | Fire\t| Smoke\t| Both \t| Empty\t|")
    print("+---------------+---------------+---------------+-------+-------+-------+---------------+")
    for x in range(3):
        t[x] = c0[x] + c1[x]
        print(f"| {subpaths[x]}\t"
              f"| {c0[x]}\t"  # fire
              f"| {c1[x]}\t"  # smoke
              f"|    {c0[x] + c1[x]}  \t"
              f"| {file[x]}\t"
              f"| {f_fire[x]}\t | {f_smoke[x]}\t| {f_both[x]} \t| {f_empty[x]}\t|"
              )
    print("+---------------+-------+-------+---------------+-------+-------+-------+---------------+")
    print(f"| Total \t| {sum(c0)}\t| {sum(c1)}\t|    {sum(t)}\t| "
          f"{sum(file)}\t| {sum(f_fire)}\t| {sum(f_smoke)}\t| "
          f"{sum(f_both)}\t| {sum(f_empty)}\t|")
    print("+=======================================================================================+")


def main():
    # open each folder to read the txt file
    class_id = []
    f_count = [0, 0, 0]
    f_empty = [0, 0, 0]

    # count for files
    f_fire = [0, 0, 0]
    f_smoke = [0, 0, 0]
    f_both = [0, 0, 0]

    # count for instances
    count0 = [0, 0, 0]  # fire
    count1 = [0, 0, 0]  # smoke
    total_instances = [0, 0, 0]
    lines = []
    for i in range(0, len(sub_path)):
        folder = open_folder(ip_path, sub_path[i])
        # print(f"folder: {folder}")
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            # print(f" file_path: {file_path}")

            with open(file_path, 'r') as f:
                f_count[i] += 1
                content = f.read()
                if content == '':
                    # match_file = redistribute.match_files(ip_path)
                    f_empty[i] += 1
                    continue        # skip over empty file
                # print(f"content: {content}")
                for lines in content:
                    lines = content.split('\n')

                    # check for file if empty
                    # if not lines:
                    #     f_empty[i] += 1
                    #     # print(f"file with no line: {f}")
                    #     continue
                # print(f"each line: {lines} in folder {file_path}")

                for first_char in lines:
                    if first_char == '':
                        continue
                    if first_char[0] == '0':
                        count0[i] += 1
                    elif first_char[0] == '1':
                        count1[i] += 1
                    class_id.append(first_char[0])   # append the first char into the array

                # print(f"class id: {class_id}")

                # check for which file have 0 or 1 only or both
                if all(x == '0' for x in class_id):
                    f_fire[i] += 1
                elif all(x == '1' for x in class_id):
                    f_smoke[i] += 1
                else:
                    f_both[i] += 1

                class_id.clear()

    # for file in match_file:
    #     shutil.move(os.path.join(ip_path, file[0]), no_lbl_path)
    #     shutil.move(os.path.join(ip_path, file[1]), no_lbl_path)
    #     print(f"move {file} to {no_lbl_path}")
    # print(f"length of match file = {len(match_file)}")
    print_result(sub_path, count0, count1, total_instances, f_count, f_fire, f_smoke, f_both, f_empty)

    # open each file and read each line of the txt file
    # find about the number of instance base on the number of line
    # find the total files belong in each folder
    # find the file which have only one labels or both


if __name__ == '__main__':
    main()
