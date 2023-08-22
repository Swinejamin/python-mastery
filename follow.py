import os
import time


def follow(filename):
    """
    Generator that produces a sequence of lines being written at the end of a file.
    """
    try:
        with open(filename, "r") as f:
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if line == "":
                    time.sleep(0.1)  # Sleep briefly to avoid busy wait
                    continue
                yield line
    except GeneratorExit:
        print("Following Done")


# Example use
if __name__ == "__main__":
    # Experiment: Garbage collection of a running generator
    f = follow("Data/stocklog.csv")

    print("next(f)")
    next(f)
    print()

    print("del f")
    print()
    del f
    # Experiment: Closing a generator
    f = follow("Data/stocklog.csv")
    for line in f:
        print(line, end="")
        if "IBM" in line:
            f.close()
