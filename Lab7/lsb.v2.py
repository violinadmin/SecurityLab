import Tkinter as tk
import sys
import struct
import numpy

from PIL import Image

### -------------------------- Window ----------------------- ###

mainWindow=tk.Tk()
mainWindow.title("LSB-insertion")
heading_label=tk.Label(mainWindow,text="LSB-insertion",padx=(10),pady=(20))
heading_label.pack()
heading_label=tk.Label(mainWindow,text="Enter picturename (it must be in the same directory:")
heading_label.pack()
first_field=tk.Entry(mainWindow)
first_field.pack()
heading_label.pack()
heading_label=tk.Label(mainWindow,text="Enter data name (it must be in the same directory) or output file for data:")
heading_label.pack()
second_field=tk.Entry(mainWindow)
second_field.pack()
operation=tk.Label(mainWindow,text="Action:")
operation.pack()


### ------------------------- Trust chain ------------------------ ###

def insertion():
    imagename=first_field.get()
    data=second_field.get()
    result=embed(imagename,data)
    result_label.config(text="File with insertion:" +str(result))

encryption_button=tk.Button(mainWindow,text="Insert data",command=lambda:insertion())
encryption_button.pack()


def extraction():
    imagename=first_field.get()
    data=second_field.get()
    result=extract(imagename,data)
    result_label.config(text="Extract data in:" +str(result))

decryption_button=tk.Button(mainWindow,text="Get data fron file", command=lambda:extraction())
decryption_button.pack()

### ---------------- End Vernam ---------- ###

# Decompose a binary file into an array of bits
def decompose(data):
        v = []

        # Pack file len in 4 bytes
        fSize = len(data)
        bytes = [ord(b) for b in struct.pack("i", fSize)]

        bytes += [ord(b) for b in data]

        for b in bytes:
                for i in range(7, -1, -1):
                        v.append((b >> i) & 0x1)

        return v

# Assemble an array of bits into a binary file
def assemble(v):
        bytes = ""

        length = len(v)
        for idx in range(0, len(v)/8):
                byte = 0
                for i in range(0, 8):
                        if (idx*8+i < length):
                                byte = (byte<<1) + v[idx*8+i]
                bytes = bytes + chr(byte)

        payload_size = struct.unpack("i", bytes[:4])[0]

        return bytes[4: payload_size + 4]

# Set the i-th bit of v to x
def set_bit(n, i, x):
        mask = 1 << i
        n &= ~mask
        if x:
                n |= mask
        return n

# Embed payload file into LSB bits of an image
def embed(imgFile, payload):
        # Process source image
        img = Image.open(imgFile)
        (width, height) = img.size
        conv = img.convert("RGBA").getdata()

        max_size = width*height*3.0/8/1024              # max payload size

        f = open(payload, "rb")
        data = f.read()
        f.close()

        # Encypt
        data_enc = data

        # Process data from payload file
        v = decompose(data_enc)

        # Add until multiple of 3
        while(len(v)%3):
                v.append(0)

        payload_size = len(v)/8/1024.0
        if (payload_size > max_size - 4):
                print "[-] Cannot embed. File too large"
                sys.exit()

        # Create output image
        steg_img = Image.new('RGBA',(width, height))
        data_img = steg_img.getdata()

        idx = 0

        for h in range(height):
                for w in range(width):
                        (r, g, b, a) = conv.getpixel((w, h))
                        if idx < len(v):
                                r = set_bit(r, 0, v[idx])
                                g = set_bit(g, 0, v[idx+1])
                                b = set_bit(b, 0, v[idx+2])
                        data_img.putpixel((w,h), (r, g, b, a))
                        idx = idx + 3

        steg_img.save(imgFile + "-with-insertion.png", "BMP")
        output=(imgFile + "-with-insertion.png")

        return output

# Extract data embedded into LSB of the input file
def extract(in_file, out_file):
        # Process source image
        img = Image.open(in_file)
        (width, height) = img.size
        conv = img.convert("RGBA").getdata()

        # Extract LSBs
        v = []
        for h in range(height):
                for w in range(width):
                        (r, g, b, a) = conv.getpixel((w, h))
                        v.append(r & 1)
                        v.append(g & 1)
                        v.append(b & 1)

        data_out = assemble(v)

        # Decrypt
        data_dec = data_out

        # Write decrypted data
        out_f = open(out_file, "wb")
        out_f.write(data_dec)
        out_f.close()

        return out_file


### ---------------------------------------###

result_label=tk.Label(mainWindow, text="operations result is:")
result_label.pack()
mainWindow.mainloop()
