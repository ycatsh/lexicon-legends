import string
import random
                                                
def generate_key():
    gen_key = ''
    choices = string.ascii_lowercase + string.digits
    for _ in range(8):
        gen_key += random.choice(choices)
                                                
    return gen_key                                                
                                                