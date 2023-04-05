def filt_generator(file_name, words):
    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            line_words = line.lower().split()
            for word in words:
                if word.lower() in line_words:
                    yield line.strip()
                    break
