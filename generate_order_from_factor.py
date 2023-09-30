customers_name: str = ''

with open('/home/gatorova/Downloads/a.txt', 'r') as source:
    full_file: list = source.readlines()

lines_with_no_newlines: list = []
for line in full_file:
    lines_with_no_newlines.append(line.replace("\n", ""))

lines_with_no_empty_str: list = [x for x in lines_with_no_newlines if x]
title_line: int = 0
order_lines: list = []
first_output: dict = {}
# print(list(lines_with_no_empty_str))
# print(list(lines_with_no_empty_str))
for idx, line in enumerate(lines_with_no_empty_str):
    # print(line)
    line = line.replace('\t', '---').replace('\u200f', '')

    if 'شرح' in line and title_line == 0:
        title_line = idx
    elif ':مشتري' in line:
        char_str = ''.join((z for z in line if not z.isdigit()))
        customers_name = char_str.replace(':مشتري', '').replace('آقاي ', '')

    if title_line < idx and title_line != 0:
        split_line = line.split('---')
        factor_number = split_line[-2]
        # print(split_line)
        if factor_number.isnumeric():
            split_line = line.split('---')
            fee = split_line[3]
            quantity = split_line[5]
            that_line = list(lines_with_no_empty_str)[idx]
            if factor_number in first_output.keys():
                first_output[factor_number].append([fee, quantity])
            else:
                first_output[factor_number] = [[fee, quantity]]
print(customers_name)
# i = 1
# for key, value in first_output.items():
#     print(i, key, value)
#     i += 1

# print(first_output)