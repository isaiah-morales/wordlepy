import random
from colorama import Fore, Back, Style, init

#parses the word list, creating a sublist with words matching the desired length
def getWordList(word_length):
    f = open("usa.txt")
    words = [line.rstrip() for line in f]
    new_list = [x for x in words if len(x) == word_length]
    f.close()
    return new_list

#checks if the provided word is in the word list
def findWord(word, word_list):
    if word in word_list:
        return True
    return False

#displays all of the words already used by the player in a keyboard formation
def printUsed(word, used_letters):
    keyboard_r1 = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"]
    keyboard_r2 = ["a", "s", "d", "f", "g", "h", "j", "k", "l"]
    keyboard_r3 = ["z", "x", "c", "v", "b", "n", "m"]

    full_key = [keyboard_r1, keyboard_r2, keyboard_r3]

    for row_num, row in enumerate(full_key):
        for i, letter in enumerate(row):
            if letter in word and letter in used_letters:
                row[i] = Fore.GREEN + letter
            elif letter in used_letters:
                row[i] = Fore.RED + letter
                
        if row_num == 1:
            print(" ", end="")
        elif row_num == 2:
            print("   ", end="")

        for letter in row:
            print(letter, end=" ")
        print("")
    print("")

#formats each letter of the word to the correct color
#for x in word_array, x[0] is letter, x[1] is letter value, x[2] is dupe boolean
#for x[1] || 0 = not in word, 1 = in word, 2 = fully correct
def formatWord(word_array):
    word = ""
    
    for x in word_array:
        if x[1] == 0:                                #if not in word
            word += (Fore.WHITE + Style.BRIGHT + Back.RESET + x[0])
        elif x[1] == 1 and x[2]:                     #if in word, but wrong place, dup letter
            word += (Fore.MAGENTA + Style.BRIGHT + Back.YELLOW + x[0])
        elif x[1] == 1 and not x[2]:                 #if in word, but wrong place
            word += (Fore.BLACK + Style.NORMAL + Back.YELLOW + x[0])
        elif x[1] == 2 and x[2]:                     #in word, right place, dup letter
            word += (Fore.MAGENTA + Style.BRIGHT + Back.GREEN + x[0])
        elif x[1] == 2 and not x[2]:                 #in word, right place
            word += (Fore.BLACK + Style.NORMAL + Back.GREEN + x[0])
    return word

#main game logic function
def runGame(chosen_word, word_list, word_length):

    word = list(chosen_word)

    last_guesses = []
    used_letters = []

    check = False
    guess_num = 1

    #this loop will take guesses until the guess matches the randomly chosen word
    while check == False:
        if guess_num != 1:
            print("=========================\n")

        for x in last_guesses:
            print(x)

        print("\ncurrent guess (" + str(guess_num) + "):  ", end = "")

        guess = input("").lower()

        print("")

        #quits the game
        if guess == "#":
            break

        #checks previously used letters
        if guess == "*":
            printUsed(word, used_letters)
            continue

        #checks if the word is the correct length
        if (len(guess) != word_length):
            print("Sorry, please try again with a length (" + str(word_length) + ") word!")
            continue

        #checks if the word is a real word in the word_list
        if guess not in word_list:
            print("Sorry, please try again with a real word!")
            continue

        guess = list(guess)
        gw_zip = zip(guess, word)

        #checks if there are any duplicate letters in the final word
        dup_letters = set(i for i in word if word.count(i)>1)
        
        f_guess = []

        #for each item in f_guess, x[0] is letter, x[1] is letter value, x[2] is dupe boolean 
        for x in gw_zip:
            is_dup = False
            l_val = 0

            if x[0] in dup_letters:
                is_dup = True
            if x[0] in word:
                l_val = 1
            if x[0] == x[1]:
                l_val = 2
            
            f_guess.append((x[0], l_val, is_dup))  
            if x[0] not in used_letters:
                used_letters.append(x[0])

        last_guesses.append(formatWord(f_guess))

        #do part of the do while, runs game until the player runs out of guesses or words match
        if guess_num == 6:
            break

        for x in f_guess:
            if x[1] == 2:
                check = True
            else:
                check = False
                break
        
        guess_num += 1
    
    print("=========================\n")
    for item in last_guesses:
        print(item)
    if check == True:
        print("\nCongratulations! You completed it in " + str(guess_num-1) + " tries!")

def main():
    init(autoreset=True)

    word_length = 5

    word_list = getWordList(word_length) #filters words of x length from word list
    list_len = len(word_list)
    retry = True

    message = ""
    with open("intro.txt") as f:
        message = f.read()

    while (retry == True):
        print(message)
        chosen_word = word_list[random.randint(0,list_len)] #selects a random word

        runGame(chosen_word, word_list, word_length)

        print("\n" + "Game over! The word was: " + chosen_word + "\n")

        x = input("Press Enter to exit or guess 'retry' to play again.\n\n").lower()
        if x != "retry":
            retry = False

if __name__ == "__main__":
    main()