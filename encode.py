import argparse
from PIL import Image

NUM_LEDS = 7
BIT_POS_SKIPPED = 3

def convert_bitmap(path):
    img = Image.open(path)
    
    # Ensure it's greyscale
    if img.mode != 'L':
        img = img.convert('L')
    
    width, height = img.size
    if height != NUM_LEDS:
        raise ValueError(f"Bitmap height ({height}) must match NUM_LEDS ({NUM_LEDS})")
    
    data = bytearray()
    data.append(width)
    data.append(17) # ??
    
    # Process each column
    for col in reversed(range(width)):
        byte_val = 0
        
        # Process each row (pixel) in the column
        for row in range(height):
            pixel = img.getpixel((col, row))
            bit = 1 if pixel > 127 else 0
            
            # Map to correct bit position, skipping BIT_POS_SKIPPED
            bit_pos = row if row < BIT_POS_SKIPPED else row + 1
            byte_val |= (bit << bit_pos)
        
        data.append(byte_val)
    
    return data


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', action='append', required=True)
    parser.add_argument('output', help='Output file')
    
    args = parser.parse_args()

    num_inputs = len(args.input)
    print(f"Writing from {num_inputs} input files to {args.output}")

    data = bytearray()
    data.append(num_inputs)
    for input_file in args.input:
        data.extend(convert_bitmap(input_file))

    padding_length = 128 - 3 - len(data)
    if padding_length < 0:
        raise ValueError("Encoded data exceeds 128 bytes")
    
    data.extend([0] * padding_length)

    # some kind of end marker?
    data.append(90)
    data.append(0)
    data.append(0)
    
    with open(args.output, 'wb') as f:
        f.write(data)
