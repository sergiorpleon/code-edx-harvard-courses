import re
import sys

def main():
    print(parse(input("HTML: ")))


def parse(s):
    #http://youtube.com/embed/xvFZjo5PgG0
    #https://youtube.com/embed/xvFZjo5PgG0
    #https://www.youtube.com/embed/xvFZjo5PgG0
    if not (s.startswith("<iframe") and s.endswith("iframe>")):
        return None

    matches = re.search(r"(http(s)?://(www.)?youtube.com/embed/\w*)", s)
    if matches:
        url = matches.group(1)

        code = re.search(r"(\w*)$", url)
        if code:
            return f"https://youtu.be/{code.group(1)}"
        else:
            return None
    else:
        return None

if __name__ == "__main__":
    main()
