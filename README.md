# Persistence of Vision (POV) Fan

On the board sits a AT24C01A. The datasheet explains this is a 1K SERIAL EEPROM: Internally organized with 16 pages of 8 bytes each, the 1K requires a 7-bit data word address for random word addressing.

Dumping the AT24C01A EEPROM using a XGecu T48:
```
minipro -p AT24C01 -r dump.bin
```

... or using SNANDer (https://github.com/McMCCRU/SNANDer) and a CH341a:
```
./SNANDer -E 24c01 -r dump.bin
```

Hirose MQ172X connector pinout from left to right:
1. (top left on the back of MQ172X male connector): pin 8 (VCC)
2. (bottom left on the back of MQ172X male connector): pin 6 (SCL)
3. (top right on the back of MQ172X male connector): pin 5 (SDA)
4. (bottom right on the back of MQ172X male connector): pin 7 (WP)
Sheath: GND (pin 4)

## Decoding the current image
```
python3 decode.py dump.bin
```

## Generating new text

Start by generating images, using e.g. [m5x7](https://github.com/boringcactus/m5x7/blob/master/src/m5x7.ttf) and imagemagick:

```
convert -size 55x7 xc:black -font m5x7.ttf -pointsize 16 -fill white -gravity center -annotate +0-1 "hello world" -threshold 50% hello-world.bmp
```

Create a new image, check that it looks as you expect:
```
python3 encode.py -i hello-world.bmp -i something-else.bmp test.bin
python3 decode.py test.bin
```

And finally write to the POV fan (e.g. with SNANDer)
```
./SNANDer -E 24c01 -w test.bin 
```
