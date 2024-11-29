import random
import time

def create_file():
    with open("numbers.txt", "w") as file:
        for _ in range(100):
            line = ' '.join(str(random.randint(1, 100)) for _ in range(20))
            file.write(line + "\n")

def read_and_filter_file():
    with open("numbers.txt", "r") as file:
        lines = file.readlines()
    int_arrays = list(map(lambda line: list(map(int, line.split())), lines))
    filtered_arrays = [list(filter(lambda x: x > 40, arr)) for arr in int_arrays]
    with open("numbers.txt", "w") as file:
        for arr in filtered_arrays:
            file.write(' '.join(map(str, arr)) + "\n")

def read_file_as_generator():
    with open("numbers.txt", "r") as file:
        for line in file:
            yield list(map(int, line.split()))

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time of {func.__name__}: {end_time - start_time:.6f} seconds")
        return result
    return wrapper

@measure_time
def process_file():
    create_file()            
    read_and_filter_file()

process_file()

print("Reading filtered data as a generator:")
for data in read_file_as_generator():
    print(data)
