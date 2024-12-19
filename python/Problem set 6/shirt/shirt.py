import sys
from PIL import Image

def main():
    try:
        if len(sys.argv)<3:
            sys.exit("Too few command-line arguments")
        if len(sys.argv)>3:
            sys.exit("Too many command-line arguments")

        before = sys.argv[1]
        after = sys.argv[2]

        if not before.endswith(".jpg") and not before.endswith(".jpeg") and not before.endswith(".png"):
            sys.exit("Invalid output")

        if (before.endswith(".jpg") and after.endswith(".jpg")) or (before.endswith(".jpeg") and after.endswith(".jpeg")) or (before.endswith(".png") and after.endswith(".png")):
            pass
        else:
            sys.exit("Input and output have different extensions")

        photo_file = Image.open(before)
        shirt_file  = Image.open("shirt.png")

        size = shirt_file.size

        photo_size = photo_file.size
        resize_photo = photo_file.resize((size[0], int((size[0]*photo_size[1])/photo_size[0])))

        photo_size = resize_photo.size
        new_photo =resize_photo.crop([0,int(photo_size[1]/2-size[1]/2),size[0],int(photo_size[1]/2+size[1]/2)])

        new_photo.paste(shirt_file, shirt_file)
        new_photo.save(after)

    except FileNotFoundError:
        sys.exit("Input does not exist")

if __name__ == "__main__":
    main()
