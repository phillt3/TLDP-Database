# GameFilter.py
# A high level class to run the program from and also abstract away all the primary implementations

import ApiHandler

def main():
    ApiHandler.fetch_games(batch_size=100, transaction_num=100)
    print("Finished Executing")

if __name__ == "__main__":
    main()