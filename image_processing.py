import cv2
import numpy as np
import matplotlib.pyplot as plt

threshold = 70

def process_image(img, top_left_lat=0, top_left_lon=0, bot_right_lat=0.180018002, bot_right_lon=0.180018002, sections=(20, 20), km_per_section = (3, 3)):

    height, width = img.shape
    print(img.shape)

    height, width = img.shape[:2]
    section_height = height // sections[0]
    section_width = width // sections[1]

    avg_brightness = np.zeros(sections, dtype=np.float32)
    num_bright_pixels = np.zeros(sections, dtype=np.float32)
    data_array = []

    bright_percent = {}
    for y in range(0, section_height*sections[0], section_height):
        for x in range(0, section_width*sections[1], section_width):
            section = img[y : y + section_height, x : x + section_width]
            #plt.imshow(section, cmap='gray')
            #plt.show()
            avg = np.mean(section)
            count = np.count_nonzero(section > threshold)
            num_bright_pixels[x//section_width, y//section_height] = count/ (section_height * section_width)
            print("count: " + str(count) + " total: " + str(section_height * section_width))
            print("%: " + str(count/ (section_height * section_width)))
            print("avg: " + str(avg))
            data = {}
            data["lat"] = top_left_lat
            data["lon"] = top_left_lon
            data["x_offset"] = km_per_section[1] * x //section_width
            data["y_offset"] = km_per_section[0] * y //section_height
            data["bright_percent"] = count/ (section_height * section_width)
            data["avg"] = avg;
            data_array.append(data)


            #print(x)
            #print(width)
            #need to return an array of key-value pairs. 4 items: date/time, lat, lon, offset NS, offset EW, pixels, avg
            avg_brightness[x // section_width, y // section_height] = avg

    return data_array;



def display_color_matrix(matrix):
    plt.figure(figsize=(8, 8))
    #print("Matrix shape before RGB conversion:", matrix.shape)
    #matrix = np.stack((matrix,) * 3, axis=-1)
    plt.imshow(matrix, cmap='gray')
    plt.axis('off')
    plt.title('20x20 Color Matrix')
    plt.show()

#Crop image to round lat and lon to the nearest hundredth
def crop_image(img, top_left_lat, top_left_lon, bot_right_lat, bot_right_lon):
  new_top_left_lat = round(top_left_lat, 2)
  new_top_left_lon = round(top_left_lon, 2)
  new_bot_right_lat = round(bot_right_lat, 2)
  new_bot_right_lon = round(bot_right_lon, 2)
  print("uncropped image data")
  print(img.shape)
  print(new_top_left_lat)
  print(new_top_left_lon)
  print(new_bot_right_lat)
  print(new_bot_right_lon)
  vertical_pixel_per_deg = abs(top_left_lat - bot_right_lat)/img.shape[0]
  horizontal_pixel_per_deg = abs(top_left_lon - bot_right_lon)/img.shape[1]
  print("pixels per degree, vertical, horizontal")
  print(vertical_pixel_per_deg)
  print(horizontal_pixel_per_deg)
  new_top_left_y = int(abs(new_top_left_lat-top_left_lat)/vertical_pixel_per_deg)
  new_top_left_x = int(abs(new_top_left_lon-top_left_lon)/horizontal_pixel_per_deg)
  new_bot_right_y = int(img.shape[0] - abs(new_bot_right_lat-bot_right_lat)/vertical_pixel_per_deg)
  new_bot_right_x = int(img.shape[1] - abs(new_bot_right_lon-bot_right_lon)/horizontal_pixel_per_deg)
  print("new image bounds:")
  print(new_top_left_y)
  print(new_top_left_x)
  print(new_bot_right_y)
  print(new_bot_right_x)
  new_img = img[new_top_left_y:new_bot_right_y, new_top_left_x:new_bot_right_x]
  return new_img, new_top_left_lat, new_top_left_lon, new_bot_right_lat, new_bot_right_lon

#calculate section size
def calculate_section_size(top_left_lat, top_left_lon, bot_right_lat, bot_right_lon, size_in_km = (1, 1)):
  total_km_lat = abs(top_left_lat - bot_right_lat) * 110.574
  total_km_lon = abs(top_left_lon - bot_right_lon) * 111.320 * np.cos(top_left_lat*np.pi/180)
  print("total km")
  print(total_km_lat)
  print(total_km_lon)
  return (int(total_km_lat // size_in_km[0]), int(total_km_lon // size_in_km[1]))

image_path = '45LosAngeles_1.png'
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
if img is None:
    raise FileNotFoundError(f"Image not found at path: {image_path}")
top_left_lat = 34.19
top_left_lon = -118.53
bot_right_lat = 33.78
bot_right_lon = -118.04


img, top_left_lat, top_left_lon, bot_right_lat, bot_right_lon = crop_image(img, top_left_lat, top_left_lon, bot_right_lat, bot_right_lon)

sections = calculate_section_size(top_left_lat, top_left_lon, bot_right_lat, bot_right_lon, (3, 3))
print("sections:" + str(sections))

data = process_image(img, top_left_lat, top_left_lon, bot_right_lat, bot_right_lon, sections, (3, 3))
print(data)
#contrast = brightness_matrix.std()
#display_color_matrix(test_matrix)
#display_color_matrix(brightness_matrix, sections)

#print(test_matrix)
#print(brightness_matrix)
