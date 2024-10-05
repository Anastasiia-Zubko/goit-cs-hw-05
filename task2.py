import requests
from collections import defaultdict
import matplotlib.pyplot as plt
import concurrent.futures

def map_function(text):
    words = text.split()
    return [(word.lower(), 1) for word in words] 

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(shuffled_values):
    reduced = {}
    for key, values in shuffled_values:
        reduced[key] = sum(values)
    return reduced

def map_reduce(text):
    # Крок 1: Мапінг
    mapped_values = map_function(text)

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Крок 3: Редукція
    reduced_values = reduce_function(shuffled_values)

    return reduced_values

# Завантаження тексту з URL
def fetch_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return ""

# Візуалізація результатів
def visualize_top_words(word_frequencies, top_n=10):
    sorted_words = sorted(word_frequencies.items(), key=lambda item: item[1], reverse=True)
    top_words = sorted_words[:top_n]
    
    words = [word for word, freq in top_words]
    frequencies = [freq for word, freq in top_words]
    
    plt.barh(words, frequencies, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.show()

# Основна функція для завантаження тексту і аналізу
def main():
    url = input("Enter the URL of the text: ")

    # Завантаження тексту
    text = fetch_text(url)
    if not text:
        print("Failed to fetch the text.")
        return

    # Використання багатопотоковості для MapReduce
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(map_reduce, text)
        result = future.result()

    # Виведення результату
    print("Word Frequencies:", result)

    # Візуалізація топ-10 слів
    visualize_top_words(result, top_n=10)

if __name__ == '__main__':
    main()
