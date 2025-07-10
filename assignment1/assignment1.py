# Task 1
def hello():
    return "Hello!"

# Task 2
def greet(name):
    return f"Hello, {name}!"

# Task 3
def calc(value1, value2, op="multiply"):
    match op:
        case "add":
            try:
                return value1 + value2
            except TypeError:
                return "You can't add those values!"
        case "subtract":
            try:
                return value1 - value2
            except TypeError:
                return "You can't subtract those values!"
        case "multiply":
            try:
                return value1 * value2
            except TypeError:
                return "You can't multiply those values!"
        case "divide":
            try:
                return value1 / value2
            except ZeroDivisionError:
                return "You can't divide by 0!"
            except TypeError:
                return "You can't divide those values!"
        case "modulo":
            try:
                return value1 % value2
            except TypeError:
                return "You can't find the modulo for those values!"
        case "int_divide":
            try:
                return value1 // value2
            except TypeError:
                return "You can't divide those values!"
        case "power":
            try:
                return value1 ** value2
            except TypeError:
                return "You can't do this operation with those values!"
        case _:
            try:
                return value1 * value2
            except TypeError:
                return "You can't multiply those values!"

# Task 4
def data_type_conversion(value, value_type):
    try:
        if value_type == "int":
            return int(value)
        elif value_type == "float":
            return float(value)
        elif value_type == "str":
            return str(value)
        else:
            return f"You can't convert {value} into a {value_type}."
    except (ValueError, TypeError):
        return f"You can't convert {value} into a {value_type}."

# Task 5
def grade(*args):
    try:
        average_note = sum(args)/len(args)
        if average_note >= 90:
            return "A"
        elif average_note >= 80:
            return "B"
        elif average_note >= 70:
            return "C"
        elif average_note >= 60:
            return "D"
        else:
            return "F"
    except TypeError:
        return "Invalid data was provided."

# Task 6
def repeat(value, times):
    str_value = ""
    for _ in range(times):
        str_value += value
    return str_value

# Task 7
def student_scores(mode, **kwargs):
    # print(kwargs.values())
    if mode == "best":
        best_student = None
        best_score = -1
        for name, score in kwargs.items():
            if score > best_score:
                best_score = score
                best_student = name
        return best_student
    elif mode == "mean":
        return sum(kwargs.values()) / len(kwargs)
    else:
        return "Invalid data!"

# Task 8
def titleize(sentence):
    little_words = ["a", "on", "an", "the", "of", "and", "is", "in"]
    words = sentence.split()
    titled_sentence = []
    for i,word in enumerate(words):
        # print(i)
        if i == 0 or i == len(words) - 1:
            titled_sentence.append(word.capitalize())
        elif word.lower() in little_words:
            titled_sentence.append(word.lower())
        else:
            titled_sentence.append(word.capitalize())

    return ' '.join(titled_sentence)

# Task 9
def hangman(secret, guess):
    print(f"{secret}, {guess}")
    hangman_word = ""
    for letter in secret:
        # print(letter)
        if letter in guess:
            hangman_word += letter
        else:
            hangman_word += "_"
    return hangman_word

# Task 10
def pig_latin(sentence):
    vowels = "aeiou"
    special_case = "qu"
    ending_word = "ay"

    words = sentence.split()
    converted_words = []
    for word in words:
        if word[0] in vowels:
            converted_words.append(word + ending_word)
        elif word[:2] == special_case:
            converted_words.append(word[2:]+word[:2]+ending_word)
        else:
            idx = 0
            while (idx < len(word)) and (word[idx] not in vowels):
                idx += 1
            if (word[idx - 1] == 'q') and (word[idx] == "u"):
                converted_words.append(word[idx+1:] + word[:idx+1] + ending_word)
            else:
                converted_words.append(word[idx:] + word[:idx] + ending_word)

    return ' '.join(converted_words)
