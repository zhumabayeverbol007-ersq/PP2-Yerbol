def reverse_words(sentence):
    words = sentence.split()
    return ' '.join(words[::-1])

sentence = "We are ready"
print(f"Reversed: '{reverse_words(sentence)}'")