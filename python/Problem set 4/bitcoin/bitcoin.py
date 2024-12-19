import sys
import requests


table = {
"USD": 38761.0833
}

def main():
    try:
        user_input = float(sys.argv[1])
        if user_input <= 0:
            sys.exit("Command-line argument is negative number")

        #convertion = table["USD"]*user_input
        response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
        obj_data = response.json()
        convertion = obj_data["bpi"]["USD"]["rate_float"]
        result = float(convertion)*user_input
        print(f"${result:,.4f}")

    except IndexError:
        sys.exit("Missing command-line argument")
    except ValueError:
        sys.exit("Command-line argument is not a number")
    except requests.RequestException:
        sys.exit("Request error")
    except KeyError:
        sys.exit("Key Error")


if __name__ == "__main__":
    main()
