import database.dbfunctions as db
from database.dbfunctions import DbCell

import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import json
import os
import datetime


def read_image(image_path):
    if not os.path.exists(image_path):
        print(f"file: '{image_path}' can't be found")
        return None

    image = cv2.imread(image_path)
    if image is None:
        print("image is none")
        return None

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

#TODO: cook
def rotate(image, rotation_angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)
    rotated_image = cv2.warpAffine(image, M, (w, h))

    return rotated_image


def standardize(image):
    mean = np.mean(image)
    stdev = np.std(image)

    print(f"BEFORE: mean: {mean} || stdev: {stdev}")

    standardized_image = ((image - mean) / stdev) * 25 + 120
    standardized_image = np.clip(standardized_image, 0, 255).astype(np.uint8)

    print(f"AFTER: mean: {np.mean(standardized_image)} || stdev: {np.std(standardized_image)}")

    return standardized_image


def process_image(image, rotation_angle):
    processed_image = rotate(image, rotation_angle)
    processed_image = standardize(processed_image)
    return processed_image


def display_image(image):
    plt.imshow(image, cmap="gray")
    plt.axis("off")
    plt.show()


def save_image(image, filename="output.jpg"):
    success = cv2.imwrite(filename, image)
    if success:
        print(f"image has been saved in {filename}")
    else:
        print("error, image not saved")
    return success


def darken_image(image, factor=0.1, base=10):
    # FOR TESTING PURPOSES ONLY
    darkened_image = np.zeros_like(image, dtype=np.uint8)
    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            pixel_value = image[row][col]
            # print(pixel_value)
            darkened_image[row][col] = np.clip(int(pixel_value * factor - base), 0, 255)
    return darkened_image


def lat_to_km(lat_val):
    return lat_val * 110.574


def long_to_km(long_val, lat_val):
    return long_val * 111.320 * np.cos(math.radians(lat_val))


def km_to_lat(km):
    return km / 110.57


def km_to_long(km, lat_val):
    return km / (111.32 * math.cos(math.radians(lat_val)))


def closest_square(n, square_size):
    if n >= 0:
        return n - (n % square_size)
    else:
        if (n % square_size == 0):
            return n
        return n + (square_size - (-n % square_size))


def map_value(n, old_start, old_stop, new_start, new_stop):
    return ((n - old_start) / (old_stop - old_start)) * (new_stop - new_start) + new_start


# Assumption: Image takes 48km by 27km
height = 27.0
width = 48.0
# TODO: Crop image to kilometer values (grid format, define it)
def crop_image(normal_image, lat_val, long_val, km=3):
    center_km = (lat_to_km(lat_val), long_to_km(long_val, lat_val))
    print(f"Center km: {center_km}")

    top_left_km = (center_km[0] - width / 2, center_km[1] - height / 2)
    print(f"Top left km: {top_left_km}")
    bottom_right_km = (center_km[0] + width / 2, center_km[1] + height / 2)
    print(f"Bottom right km: {bottom_right_km}")

    new_top_left = (closest_square(top_left_km[0], km), closest_square(top_left_km[1], km))
    print(f"New top left km: {new_top_left}")

    new_bottom_right = (closest_square(bottom_right_km[0], km), closest_square(bottom_right_km[1], km))
    print(f"New bottom right km: {new_bottom_right}")

    pixel_top_left = (map_value(new_top_left[0], top_left_km[0], bottom_right_km[0], 0, normal_image.shape[0]),
                      map_value(new_top_left[1], top_left_km[1], bottom_right_km[1], 0, normal_image.shape[1]),)
    pixel_bottom_right = (map_value(new_bottom_right[0], top_left_km[0], bottom_right_km[0], 0, normal_image.shape[0]),
                          map_value(new_bottom_right[1], top_left_km[1], bottom_right_km[1], 0, normal_image.shape[1]),)

    new_center = ((pixel_top_left[0] + pixel_bottom_right[0]) / 2, (pixel_top_left[1] + pixel_bottom_right[1]) / 2)
    lat_long_center = (km_to_lat(new_center[0]), km_to_long(new_center[1], km_to_lat(new_center[0])))
    
    pixel_top_left = (math.floor(pixel_top_left[0]), math.floor(pixel_top_left[1]))
    pixel_bottom_right = (math.floor(pixel_bottom_right[0]), math.floor(pixel_bottom_right[1]))
    print(f"New pixel top left km: {pixel_top_left}")
    print(f"New pixel bottom right km: {pixel_bottom_right}")

    new_size_km = (new_top_left[0] - new_bottom_right[0], new_top_left[1] - new_bottom_right[1])

    return normal_image[pixel_top_left[0]:pixel_bottom_right[0], pixel_top_left[1]:pixel_bottom_right[1]], lat_long_center, new_size_km


# TODO: Return 4 lists: pixel rows (top), latitude vals (top),
#                       pixel cols (left), longitude vals (left)
# At same index, the values should match up
def get_square_locations(cropped_image, center_lat_long, size_km, km=3):
    pixel_rows = [0, 20, 40]
    pixel_cols = [0, 20, 40]
    lat_vals = [0.01, 0.02, 0.03]
    long_vals = [0.01, 0.02, 0.03]
    row_index = 0
    '''
    for row in range(0, cropped_image.shape[0], cropped_image.shape[0]/size_km[0]):
        pixel_rows.append(row)
        lat_vals.append(center_lat_long[0] - width / 2 + km_to_lat(row_index))
        row_index += 3
    col_index = 0
    for col in range(0, cropped_image.shape[1], cropped_image.shape[1]/size_km[1]):
        pixel_cols.append(col)
        long_vals.append(center_lat_long[1] - height / 2 + km_to_long(col_index))
        col_index += 3
    '''
    return pixel_rows, pixel_cols, lat_vals, long_vals


def count_bright_pixels(section, threshold=120):
    bright_pixels = np.sum(section > threshold)
    total_pixels = section.size
    return bright_pixels, total_pixels

SQUARE_SIZE = 3
def split_image(normal_image, lat_val, long_val):
    # split into 16*9 sections
    '''
    The approximate conversions are:
    * Latitude: 1 deg = 110.574 km
    * Longitude: 1 deg = 111.320*cos(latitude) km
    '''
    
    # returns cropped image
    image, new_lat_long, new_size_km = crop_image(normal_image, lat_val, long_val, SQUARE_SIZE)
    # returns latitude values (top of rows),
    # longitude values (left of columns)
    pixel_rows, pixel_cols, lat_vals, long_vals = get_square_locations(image, new_lat_long, new_size_km, SQUARE_SIZE)

    section_list = []
    for row_index in range(len(pixel_rows)):
        for col_index in range(len(pixel_cols)):
            if (col_index == len(pixel_cols) - 1 or row_index == len(pixel_rows) - 1):
                pass
            else:
                section = image[pixel_rows[row_index] : pixel_rows[row_index + 1], pixel_cols[col_index] : pixel_cols[col_index + 1]]
                bright_pixels, total_pixels = count_bright_pixels(section)
                lat_val = lat_vals[row_index]
                long_val = long_vals[col_index]
                now = datetime.datetime.now()
                data = {
                    "bright_pixels": bright_pixels,
                    "total_pixels": total_pixels,
                    "lat": lat_val,
                    "long": long_val,
                    "date": now
                }
                section_list.append(data)
    return section_list


def detect_outage(section_bright, section_total, normal_bright, normal_total, threshold=0):
    return (section_bright / section_total - normal_bright / normal_total) > threshold


def send_json(section):
    
    data = {
        "time": section["date"].strftime('%s'),
        "latitude": section["lat"],
        "longitude": section["long"],
        "image path": f"capture-{1}.png",
        "confidence interval": 0.1 # currently, this value is the threshold, not the confidence interval. not sure what it's for?
    }

    filename = "outage.json"

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"JSON data saved to {filename}")



def determine_outage(section_list, threshold=0.8):
    for section in section_list:
        # find previous section from database
        prev_section = db.get_one(section["lat"], section["long"])
        if prev_section and detect_outage(section["bright_pixels"], section["total_pixels"], prev_section["bright_pixels"], prev_section["total_pixels"]):
            # THERE HAS BEEN AN OUTAGE!!
            # Send json to ground station!
            send_json(section)
        else:
            db.write_one(section["lat"], section["long"], section["bright_pixels"], section["total_pixels"], section["date"])
            # THERE HAS NOT BEEN AN OUTAGE!!
            # Save current data to database (cause no outage)


def main():
    db.create()
    arr = np.random.randint(0, 255, (270, 480))
    # print(f"Original array: {arr}")
    print(f"Original array shape: {arr.shape}")
    print("---")
    arr1, new_center, new_size = crop_image(arr, 0, 0)
    # print(f"Cropped array: {arr1}")
    print(f"Cropped array shape: {arr1.shape}")
    print(f"Cropped array center: {new_center}")
    print(f"Cropped array squares shape: {new_size}")
    print("---")
    section_list = split_image(arr1, 0, 0)
    for section in section_list:
        print(section)

    section = section_list[0]
    # send_json(section)
    determine_outage(section_list)
    db.print_all()


if __name__ == "__main__":
    main()
    pass