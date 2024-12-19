def main():
    name = input("File: ").strip()
    print(media_type(name))

def media_type(name):
    if name.lower().endswith(".gif"):
        return "image/gif"
    elif name.lower().endswith(".jpg"):
        return "image/jpeg"
    elif name.lower().endswith(".jpeg"):
        return "image/jpeg"
    elif name.lower().endswith(".png"):
        return "image/png"
    elif name.lower().endswith(".pdf"):
        return "application/pdf"
    elif name.lower().endswith(".txt"):
        return "application/txt"
    elif name.lower().endswith(".zip"):
        return "application/zip"
    else:
        return "application/octet-stream"

main()
