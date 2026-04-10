import math
import collections
import os


def calculate_entropy(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, "rb") as f:
        data = f.read()

    if not data:
        return 0.0

    length = len(data)
    counter = collections.Counter(data)

    entropy = 0.0
    for count in counter.values():
        p_x = count / length
        entropy += -p_x * math.log2(p_x)

    return entropy


if __name__ == "__main__":
    dummy_file = "dummy_test_file.txt"
    with open(dummy_file, "w", encoding="utf-8") as f:
        f.write(
            "This is a dummy file to test the Shannon Entropy calculation. Let's see how random this is!"
        )

    entropy_score = calculate_entropy(dummy_file)
    print(f"Entropy of {dummy_file}: {entropy_score:.4f}")

    if os.path.exists(dummy_file):
        os.remove(dummy_file)
