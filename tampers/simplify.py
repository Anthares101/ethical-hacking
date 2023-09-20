# Oracle specific for now, works pretty well alongside space2comment

#!/usr/bin/env python3

from lib.core.enums import PRIORITY
import re


__priority__ = PRIORITY.NORMAL

def dependencies():
    pass

def tamper(payload, **kwargs):
    ret_val = ''

    # Nerf comments a bit
    ret_val = re.sub('--.*', '--A', payload)

    # Nerf CHR functions
    found_chr_functions = re.findall('CHR\(\d*?\)', ret_val)
    for found_chr_function in found_chr_functions:
        chr_num = re.search('\d+', found_chr_function).group()
        ret_val = ret_val.replace(found_chr_function, f"'{chr(int(chr_num))}'")

    return ret_val
