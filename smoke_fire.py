import cv2
import numpy as np
import random
import os


def overlay_smoke(image, smoke, position, scale=1.0):
    # Resize the smoke image based on the scale
    smoke_resized = cv2.resize(smoke, (0, 0), fx=scale, fy=scale)

    # Get dimensions of the smoke and image
    h, w, _ = smoke_resized.shape
    y, x = position

    # Ensure the smoke is within image boundaries
    if x + w > image.shape[1]:
        w = image.shape[1] - x
        smoke_resized = smoke_resized[:, :w]
    if y + h > image.shape[0]:
        h = image.shape[0] - y
        smoke_resized = smoke_resized[:h, :]

    # Split the smoke into its channels (including alpha for transparency)
    b, g, r, a = cv2.split(smoke_resized)

    # Create a mask using the alpha channel and apply it to the smoke
    alpha_mask = a / 255.0
    for c in range(0, 3):
        image[y:y+h, x:x+w, c] = (1.0 - alpha_mask) * image[y:y+h, x:x+w, c] + alpha_mask * smoke_resized[:, :, c]

    return image


def add_random_smoke(image_path, smoke_path, output_path, num_smoke=random.choice([1, 2, 3])):
    # Load the image and the smoke image
    image = cv2.imread(image_path)
    # cv2.imshow('image', image)
    smoke = cv2.imread(smoke_path, cv2.IMREAD_UNCHANGED)  # Load with transparency (alpha channel)
    for _ in range(num_smoke):
        # Random scale factor for smoke size
        scale = random.uniform(0.2, 1.0)

        # Random position for placing smoke
        max_y = image.shape[0] - int(smoke.shape[0] * scale)
        max_x = image.shape[1] - int(smoke.shape[1] * scale)
        y = random.randint(0, max_y)
        x = random.randint(0, max_x)

        # Overlay the smoke onto the image
        image = overlay_smoke(image, smoke, (y, x), scale)

    # Save the output image
    cv2.imwrite(output_path, image)


if __name__ == "__main__":
    # Paths to your images
    image_path = r"E:\CapstoneB\new_dataset\RMIT Data"  # folder
    smoke_path = r"E:\CapstoneB\new_dataset\fire"    # folder
    output_path = r"E:\CapstoneB\new_dataset\output_mod_pic\fire_mod"   # folder
    count = 1
    for file in os.listdir(image_path):
        images = os.path.join(image_path, file)
        smokes = os.path.join(smoke_path, random.choice(os.listdir(smoke_path)))
        output_img_path = os.path.join(output_path, f'{str(count)}.jpg')
        add_random_smoke(images, smokes, output_img_path)
        print(output_img_path)
        # print(f"Count = {count}")
        count += 1
    # add_random_smoke(image_path, smoke_path, output_path)
