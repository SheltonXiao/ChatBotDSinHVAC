# -*- coding:utf-8 -*-
'''
@File    :   tokenChecker.py
@Time    :   2023/05/11 22:09:10
@Author  :   SheltonXiao
@Version :   1.0
@Contact :   pi620903@163.com
@Desc    :   None
@License :

    (c) Copyright 2022 SheltonXiao

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or(at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY;without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
    GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with this program.If not, see < https: //www.gnu.org/licenses/>.
'''

# here put the import lib
from transformers import GPT2Tokenizer
import numpy as np

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")  # GPT-2的tokenizer和GPT-3是一样的
MAX_LIMIT = 4097
SUBSET_LIMIT = 4000

def check_prompts(prompts):
    token_counts = len(tokenizer.encode(prompts))
    if token_counts > MAX_LIMIT:
        return np.ceil(token_counts/SUBSET_LIMIT)
    else:
        return None


if __name__ == '__main__':
    pass
