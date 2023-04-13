import io


class IncorrectInput(Exception):
    pass


def filt_generator(file_name, words):
    if isinstance(file_name, str):
        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:
                line_words = line.lower().split()
                for word in words:
                    if word.lower() in line_words:
                        yield line.strip()
                        break
    elif isinstance(file_name, io.StringIO):
        file_name.seek(0)
        line = file_name.readline()
        while line:
            line_words = line.lower().split()
            for word in words:
                if word.lower() in line_words:
                    yield line.strip()
                    break
            line = file_name.readline()
    else:
        raise IncorrectInput("Enter the correct file name or file object")
