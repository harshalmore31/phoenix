import webbrowser

def order_food(food : str,city :str) -> str:
    print(f"Lets order {food}:")
    select = int(input("Select opt. number from Below \n 1. Zomato \n 2. Swiggy \n Opt. No : "))
    if select == 1:
        print(f"Ordering {food} from zomato")
        print(f"Click on the link below \n https://www.zomato.com/{city}/delivery/dish-{food} ")
        webbrowser.open("https://www.zomato.com/{city}/delivery/dish-{food}")
    
    else:
        print(f"Ordering {food} from swiggy")   