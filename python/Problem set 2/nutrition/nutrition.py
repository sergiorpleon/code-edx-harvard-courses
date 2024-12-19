
def main():
    items = ["Apple", "Avocado", "Banana", "Cantaloupe", "Grapefruit", "Grapes", "Honeydew Melon", "Kiwifruit", "Lemon", "Lime", "Nectarine", "Orange",  "Peach", "Pear", "Pineapple", "Plums", "Strawberries", "Sweet Cherries", "Tangerine", "Watermelon"]
    calories =[130, 50, 110, 50, 60, 90, 50 , 90, 15, 20, 60, 80, 60, 100, 50, 70, 50, 100, 50, 80]

    item = input("Item: ").strip()

    index = 0
    for i in items:
        if i.lower() == item.lower():
            print(f"Calories: {calories[index]}")
        index = index + 1



if __name__ == "__main__":
    main()
