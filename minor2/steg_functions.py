import cv2
import numpy as np

def msgtobinary(pixel):
    if len(pixel) >= 3:
        r, g, b = pixel[:3]  # Take the first three values from the pixel tuple
        r_binary = format(r, "08b")
        g_binary = format(g, "08b")
        b_binary = format(b, "08b")
        return r_binary, g_binary, b_binary
    else:
        raise ValueError("Pixel tuple must have at least three values")

def encode_img_data(img, data, filename):
    if len(data) == 0:
        raise ValueError('Data entered to be encoded is empty')
    
    # Calculate available bytes and check capacity
    no_of_bytes = (img.shape[0] * img.shape[1] * 3) // 8
    print("\t\nMaximum bytes to encode in Image: ", no_of_bytes)
    if len(data) > no_of_bytes - 3:  # Account for end marker
        raise ValueError("Insufficient bytes Error, Need Bigger Image or give Less Data !!")

    # Add end marker to data
    data += '^^*' 
    binary_data = ''.join(format(ord(i), "08b") for i in data)
    print("\n", binary_data)
    
    length_data = len(binary_data)
    print("\nThe Length of Binary data", length_data)

    index_data = 0
    for row in img:
        for pixel in row:
            r, g, b = msgtobinary(pixel)
            if index_data < length_data:
                pixel[0] = int(r[:-1] + binary_data[index_data], 2)  # Modify LSB of red
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + binary_data[index_data], 2)  # Modify LSB of green
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + binary_data[index_data], 2)  # Modify LSB of blue
                index_data += 1
            if index_data >= length_data:
                break  # Stop if all data is embedded

    cv2.imwrite(filename, img)
    print("\nEncoded the data successfully in the Image and the image is successfully saved with name ", filename) 
def decode_img_data(img):
    data_binary = ""

    # Extract LSBs from each color channel
    for row in img:
        for pixel in row:
            r, g, b = msgtobinary(pixel)
            data_binary += r[-1]  # Extract LSB of red
            data_binary += g[-1]  # Extract LSB of green
            data_binary += b[-1]  # Extract LSB of blue

    # Group into bytes and decode characters
    decoded_data = ""
    i = 0
    while i < len(data_binary):
        byte = data_binary[i:i+8]
        if byte == "11101010":
            break
        decoded_data += chr(int(byte, 2))
        i += 8

    # Handle potential absence of end marker
    if "^^*" not in decoded_data:
        print("Warning: End marker not found. Data might be incomplete or corrupted.")
    else:
        decoded_data = decoded_data.split("^^*")[0]

    return decoded_data

