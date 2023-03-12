def filt_generator(file_name, words):
    try:  # если на вход дано имя файла
        with open(file_name, "r", encoding="utf-8") as file:
            lines = file.read()
    except TypeError:  # если на вход дан файловый объект
        lines = file_name.getvalue()
    lines = lines.split("\n")
    for line in lines:
        for word in words:
            if word.lower() in line.lower():
                yield line
                break
