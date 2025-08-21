NUM_LEDS = 7
BIT_POS_SKIPPED = 3

def render_bitmap(data, start, length, num_bits=NUM_LEDS, bit_pos_skipped=BIT_POS_SKIPPED):
    try:
        # Convert to binary representation (LSB first)
        binary_rows = [''] * num_bits

        for byte in reversed(data[start:start+length]):
            for bit_pos in range(8):
                # Extract each bit (LSB first for typical bitmap fonts)
                if bit_pos == bit_pos_skipped:
                    continue
                bit = (byte >> bit_pos) & 1
                char = '█' if bit else ' '
                binary_rows[bit_pos if bit_pos < bit_pos_skipped else bit_pos-1] += char

        # Print the decoded bitmap
        print("-" * len(binary_rows[0]))
        for row in binary_rows:
            print(row)
        print("-" * len(binary_rows[0]))

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error reading file: {e}")

def render_section(data):
    length = data[0]
    settings = data[1]
    print(f"Section length: {length}, settings: {settings} (7 == number of LEDs?)")
    render_bitmap(data, 2, length)
    return length + 2

def decode_data(data):
    num_messages = data[0]
    print(f"Number of messages: {num_messages}")
    print()
    offset = 1
    for i in range(num_messages):
        print(f"Message {i+1}:")
        offset += render_section(data[offset:])

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python decode.py <filename>")
        print("Example: python decode.py message.bin")
    else:
        filename = sys.argv[1]
        with open(filename, 'rb') as f:
            data = f.read()

        print(f"Read {len(data)} bytes from {filename}")
        print()

        decode_data(data)
