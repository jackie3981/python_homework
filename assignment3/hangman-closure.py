# Task 4

def make_hangman(secret_word):
    guesses = []

    def hangman_closure(ltr):
        guesses.append(ltr)

        display = ''.join([char if char in guesses else '_' for char in secret_word])
        print("Word:", display)

        return all(char in guesses for char in secret_word)

    return hangman_closure


if __name__ == "__main__":
    secret = input("Type the secret word: ").lower()
    print("\n¡The Hangman game has begun.!\n")

    guess_func = make_hangman(secret)

    while True:
        letter = input("Guess a letter: ").lower()
        if len(letter) != 1 or not letter.isalpha():
            print("Please, only one letter at a time")
            continue

        completed = guess_func(letter)
        if completed:
            print("Congratulations! You guessed the whole word!")
            break
