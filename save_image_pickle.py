from trdg.data_generator import FakeTextDataGenerator
import random
import pickle
import time
import os

KOR_DICT_DIR = os.path.join('data', 'dicts', 'korean')
KOR_DICT_FILENAME = 'filtered_ex1.txt'
KOR_STRING_DIR = os.path.join('data', 'chars', 'korean')
KOR_STRING_FILENAME = 'ko.txt'
FONT_DIR = os.path.join('data', 'fonts', 'otf')
IMAGE_DIR = os.path.join('data', 'images_640_270')


def get_fonts():
    return [os.path.join(FONT_DIR, filename) for filename in os.listdir(FONT_DIR)]


def get_words():
    with open(os.path.join(KOR_DICT_DIR,KOR_DICT_FILENAME), 'r', encoding='utf8') as file:
        return [string.strip() for string in file.readlines()]
    

def get_chars():
    with open(os.path.join(KOR_STRING_DIR,KOR_STRING_FILENAME), 'r', encoding='utf8') as file:
        return [ch for ch in file.read().strip()]


FONTS = get_fonts()
WORDS = get_words()
CHARS = get_chars()
IMAGE_PATHS = [os.path.join(IMAGE_DIR, image_filename) for image_filename in os.listdir(IMAGE_DIR)]


def add_noise_to_number(number, w=0.1):
    w_int = int(number * w)
    return number + random.randint(-w_int, w_int)


def get_random_colors(num=5):
    return ['#' + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)]) for __ in range(num)]


def get_random_string(strings, min_return_len=6, ws_step_type='random'):
    string = random.choice(strings)
    cnt = 1
    reset = False
    if ws_step_type == 'random':
        reset = True
    while len(string) < min_return_len:
        if ws_step_type == 'random':
            if reset:
                cnt = random.randint(1, 10)
                reset = False
        if cnt == 0:
            string += ' ' + random.choice(strings)
            cnt = 1
            reset = True
        else:
            string += random.choice(strings)
        cnt -= 1
    return string[:40]


def get_random_lengths(start, end, num=10, distinct=False):
    result = set() if distinct else []
    while len(result) != num:
        if distinct:
            result.add(random.randint(start, end))
        else:
            result.append(random.randint(start, end))
    return list(result)


def get_strings_to_generate(lengths):
    result = []
    for ln in lengths[:len(lengths) // 2]:
        result.append(get_random_string(WORDS, min_return_len=ln, ws_step_type='1'))
    for ln in lengths[len(lengths) // 2:]:
        result.append(get_random_string(CHARS, min_return_len=ln))
    return result


def save_pickle(num=1000):
    st = time.time()
    string_lengths = get_random_lengths(2, 40, num)
    strings = get_strings_to_generate(string_lengths) 
    fonts = [random.choice(FONTS) for _ in range(num)]
    sizes = [add_noise_to_number(random.choice(range(32, 202, 17))) for _ in range(num)]
    colors = get_random_colors(num)

    stack = []
    for tup in zip( 
           [i for i in range(num)],
           strings,
           fonts,
           [None] * num,
           sizes,
           [None] * num,
           [0] * num,
           [False] * num,
           [3] * num,
           [True] * num,
           [random.choice([0,1,3,4]) for _ in range(num)],
           [0] * num,
           [0] * num,
           [False] * num,
           [0] * num,
           [-1] * num,
           [1] * num,
           colors,
           [0] * num,
           [1.0] * num,
           [random.randint(0, 3) for _ in range(num)],
           [(5, 5, 5, 5)] * num,
           [False] * num,
           [False] * num,
           [False] * num,
           [IMAGE_DIR] * num,
       ):
        stack.append(FakeTextDataGenerator.generate_from_tuple(tup))
    stack_in_bytes = pickle.dumps(stack)
    print(time.time() - st)
    return stack_in_bytes


def save_pickle2(num=1000):
    st = time.time()
    fonts = get_fonts()
    cnt = num
    strings = ['박박'] * cnt
    fonts = [fonts[0]] * cnt
    sizes = [60] * cnt
    colors = ['#000000'] * cnt

    stack = []
    for tup in zip( 
           strings,
           fonts,
           sizes,
           [0] * num,
           [False] * num,
           [3] * num,
           [True] * num,
           [3 for _ in range(num)],
           [0] * num,
           [0] * num,
           [False] * num,
           [-1] * num,
           [1] * num,
           colors,
           [0] * num,
           [1.0] * num,
           [random.randint(0, 3) for _ in range(num)],
           [(5, 5, 5, 5)] * num,
           [False] * num,
           [False] * num,
           [IMAGE_PATHS[0]] * num,
           #[random.choice(IMAGE_PATHS) for _ in range(num)],
           #[os.path.join(IMAGE_DIR, 'img_1279_mv_1_002.jpg')] * num,
           #[random.choice(IMAGE_PATHS) for _ in range(num)],
       ):
        #try:
            stack.append(FakeTextDataGenerator.generate_from_tuple(tup))
        #except Exception as e:
        #    print(str(e))
        #    print(tup)
    #print(stack)
    stack_in_bytes = pickle.dumps(stack)
    print(time.time() - st)
    return stack_in_bytes

if __name__ == '__main__':
    #save_pickle(100)
    save_pickle2(1000)
