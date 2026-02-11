import re

def get_length_and_material(text):
    extracted_data = {}
    # 提取长度信息
    length_pattern = r'([A-Za-z\s]*Length)[：:]\s*(\d+)\s*CM'
    length_matches = re.findall(length_pattern, text, re.IGNORECASE)
    for key, value in length_matches:
        # 去除多余空格
        key = key.strip()
        value = value.strip()
        extracted_data[key] = value

    # 提取材料信息
    material_pattern = r'([A-Za-z\s]*material)[：:]\s*([^：:\n]+?)(?=\s{2,}|$)'
    material_matches = re.findall(material_pattern, text, re.IGNORECASE)
    for key, value in material_matches:
        # 去除多余空格
        key = key.strip()
        value = value.strip()
        extracted_data[key] = value

    values = list(extracted_data.values())[:5]

    # pattern = r'([^：:\n]+?)[：:]\s*(?:(\d+)\s*CM|([^：:\n]+?))(?=\s{2,}|$)'
    # matches = re.findall(pattern, text)

    # # 清理结果
    # extracted_data = {}
    # print(matches)
    # for key, value in matches:
    #     # 去除多余空格
    #     key = key.strip()
    #     value = value.strip()
    #     extracted_data[key] = value

    # print(extracted_data)

    if len(extracted_data.values()) != 5:
        print('Invalid input text')
        raise ValueError('Invalid input text')
    
    values = list(extracted_data.values())[:5]
    
    return values

def get_product_description(text):
    first_english_match = re.search(r'[A-Za-z]', text)
    if first_english_match:
        split_index = first_english_match.start()
        part1 = text[:split_index]
        part2 = text[split_index:]
    
    return part1, part2