from os import get_terminal_size

line_width = get_terminal_size().columns
half_line = int(line_width/2)

def print_centralized(text = '', fill_in = '-'):
    fill_in = str(fill_in)
    if len(fill_in) > 1: fill_in = '-'
    
    msg_to_print = str(text)
    
    sentence_length = len(msg_to_print)
    half_sentence = int(sentence_length)

    left_margin = half_sentence
    right_margin = (sentence_length - half_sentence)

    if (left_margin < right_margin):
        a = right_margin
        right_margin = left_margin
        left_margin = a

    print('\n' + fill_in * (half_line - left_margin) + msg_to_print + fill_in * (half_line - right_margin) + '\n')

if __name__ == '__main__':
    variable = '/home/usr/test.wat'
    print_centralized(f' Test {variable} ', fill_in = ' ')