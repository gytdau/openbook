import time
import sys
from helpers import process_epubs

filename = sys.argv[1]

if __name__ == "__main__":
    durations = []
    while True:
        start = time.time()
        process_epubs([filename])
        duration = time.time() - start
        durations.append(duration)
        average = sum(durations) / len(durations)
        print(f"Time per set (avg): {average}")
