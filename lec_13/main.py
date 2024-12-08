import random
import string
import time
from collections import defaultdict
import threading
from multiprocessing import Pool, Manager

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_large_text_file(file_name, total_sentences=10000):
    with open(file_name, 'w', encoding='utf-8') as file:
        for _ in range(total_sentences):
            num_words = random.randint(5, 15)
            sentence = ' '.join(generate_random_string(random.randint(3, 7)) for _ in range(num_words))
            file.write(sentence + '.\n')

def count_words_sequential(file_name):
    word_count = defaultdict(int)
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            words = line.split()
            for word in words:
                word_count[word.lower()] += 1
    return word_count

def process_chunk_with_threads(chunk, shared_counts):
    local_count = defaultdict(int)
    for line in chunk:
        words = line.split()
        for word in words:
            local_count[word.lower()] += 1
    
    with threading.Lock():
        for word, count in local_count.items():
            shared_counts[word] += count

def count_words_using_threads(file_name, num_threads=4):
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    chunk_size = len(lines) // num_threads
    threads = []
    shared_counts = defaultdict(int)

    for i in range(num_threads):
        chunk = lines[i*chunk_size : (i+1)*chunk_size]
        thread = threading.Thread(target=process_chunk_with_threads, args=(chunk, shared_counts))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    return shared_counts

def process_chunk_with_mp(chunk):
    local_count = defaultdict(int)
    for line in chunk:
        words = line.split()
        for word in words:
            local_count[word.lower()] += 1
    return local_count

def count_words_using_multiprocessing(file_name, num_processes=4):
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    chunk_size = len(lines) // num_processes
    chunks = [lines[i*chunk_size : (i+1)*chunk_size] for i in range(num_processes)]

    with Manager() as manager:
        shared_counts = manager.dict()
        with Pool(processes=num_processes) as pool:
            results = pool.map(process_chunk_with_mp, chunks)

        for result in results:
            for word, count in result.items():
                if word in shared_counts:
                    shared_counts[word] += count
                else:
                    shared_counts[word] = count

        return dict(shared_counts)

def compare_execution_time(file_name):
    start = time.time()
    sequential_counts = count_words_sequential(file_name)
    sequential_duration = time.time() - start
    print(f"Sequential method took {sequential_duration:.4f} seconds")

    start = time.time()
    thread_counts = count_words_using_threads(file_name, num_threads=4)
    thread_duration = time.time() - start
    print(f"Multithreading method took {thread_duration:.4f} seconds")

    start = time.time()
    process_counts = count_words_using_multiprocessing(file_name, num_processes=4)
    process_duration = time.time() - start
    print(f"Multiprocessing method took {process_duration:.4f} seconds")

    assert sequential_counts == thread_counts == process_counts, "Mismatch in results!"

    threading_speedup = sequential_duration / thread_duration
    multiprocessing_speedup = sequential_duration / process_duration

    print(f"Speedup (Multithreading): {threading_speedup:.2f}")
    print(f"Speedup (Multiprocessing): {multiprocessing_speedup:.2f}")

generate_large_text_file('generated_text.txt', total_sentences=10000)

if __name__ == "__main__":
    file_name = 'generated_text.txt'
    compare_execution_time(file_name)
