

from pyrouge import Rouge155

rg = Rouge155()
rg.system_dir = './data_result/reference'
rg.model_dir = './data_result/model'
rg.system_filename_pattern = 'example.(\d+).txt'
rg.model_filename_pattern = 'example.[A-Z].#ID#.txt'

output = rg.convert_and_evaluate()
print(output)

output_dict = rg.output_to_dict(output)





