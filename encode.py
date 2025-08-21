import argparse
from font import font

NUM_LEDS = 7
CHARACTER_WIDTH = 5
BIT_POS_SKIPPED = 3

def convert_bitmap(content):

    print(content)

    data = bytearray()
    data.append(len(content) * CHARACTER_WIDTH)
    data.append(17) # ??

    for char in reversed(content):
        if char not in font:
            raise ValueError(f"Character '{char}' not found in font mapping")
        pixels = font[char]
        print(pixels)
        for x in reversed(range(CHARACTER_WIDTH)):
            byte_val = 0
            for y in range(NUM_LEDS):
                bit = 1 if pixels[y][x] == '#' else 0
                
                # Map to correct bit position, skipping BIT_POS_SKIPPED
                bit_pos = y if y < BIT_POS_SKIPPED else y + 1
            
                byte_val |= (bit << bit_pos)
            
            data.append(byte_val)
    
    return data

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', action='append', required=True)
    parser.add_argument('output', help='Output file')
    
    args = parser.parse_args()
    num_inputs = len(args.input)

    data = bytearray()
    data.append(num_inputs)
    for content in args.input:
        data.extend(convert_bitmap(content))

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
