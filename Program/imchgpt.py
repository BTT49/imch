from PIL import Image

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(b, 2)) for b in chars)

def encode_image(input_image_path, output_image_path, secret_message):
    image = Image.open(input_image_path)
    binary_message = text_to_binary(secret_message) + '1111111111111110'  # EOF marker
    binary_index = 0

    if image.mode != 'RGB':
        image = image.convert('RGB')

    encoded_image = image.copy()
    pixels = encoded_image.load()

    for y in range(image.height):
        for x in range(image.width):
            r, g, b = pixels[x, y]
            if binary_index < len(binary_message):
                r = (r & ~1) | int(binary_message[binary_index])
                binary_index += 1
            if binary_index < len(binary_message):
                g = (g & ~1) | int(binary_message[binary_index])
                binary_index += 1
            if binary_index < len(binary_message):
                b = (b & ~1) | int(binary_message[binary_index])
                binary_index += 1
            pixels[x, y] = (r, g, b)

            if binary_index >= len(binary_message):
                break
        if binary_index >= len(binary_message):
            break

    encoded_image.save(output_image_path)
    print("Message encoded and saved to", output_image_path)

def decode_image(image_path):
    print("Decoding image:", image_path)
    image = Image.open(image_path)
    binary_data = ''
    pixels = image.load()

    for y in range(image.height):
        for x in range(image.width):
            r, g, b = pixels[x, y]
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

    eof_index = binary_data.find('1111111111111110')
    if eof_index != -1:
        binary_data = binary_data[:eof_index]
        return binary_to_text(binary_data)
    else:
        return "No hidden message found."

