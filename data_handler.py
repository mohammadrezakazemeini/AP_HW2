import os

def load_data(file_path="data.txt"):
    if not os.path.isfile(file_path):
        print("File doesn't exist")
        return
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.readlines()
    data = [line.strip()for line in data]
    data.sort()
    return data

def save_data(data , file_path="data.txt"):
    with open(file_path, "w", encoding="utf-8") as file:
        for record in data:
            file.write(f"{record}\n")
    print("Data saved")

