def convert_rot13(text):
    new_text = []
    for character in text:
        if character.isalpha():
            new_text.append(get_rot13_value(character))
        else:
            new_text.append(character)
    return ''.join(new_text)


def get_rot13_value(character):
    """
    Convert the character to the ROT13 character.

    This happens by first converting the character to it's ASCII value. Then, it's important to
    know whether it's on the a-z or A-Z range, so that case sensitivity is preserved. Then, since
    this function yields symmetrical results (ie. if the numbers are in a loop, then adding or
    subtracting 13 would yield the same number), the rot13 value can be calculated by adding or
    removing depending on what keeps the value below the upper bound.
    """
    current_position = ord(character)
    upper_bound = 90 if current_position <= 90 else 122  # 90 = 'A', 122 = 'a'
    current_position += 13 if current_position + 13 <= upper_bound else -13
    return chr(current_position)
