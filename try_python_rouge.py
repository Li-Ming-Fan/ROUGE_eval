# -*- coding: utf-8 -*-
"""

https://www.jianshu.com/p/2d7c3a1fcbe3

https://github.com/pltrdy/rouge
https://pypi.org/project/rouge/0.2.1/

"""


from rouge import Rouge

a = ["i am a student from xx school"]  # 预测摘要 （可以是列表也可以是句子）
b = ["i am a student from school on china"] #真实摘要

rouge = Rouge()
rouge_score = rouge.get_scores(a, b)
print(rouge_score[0]["rouge-1"])
print(rouge_score[0]["rouge-2"])
print(rouge_score[0]["rouge-l"])

