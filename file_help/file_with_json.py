import json


def open_file(path, mode='r', encoding='utf8'):
    with open(path, mode, encoding=encoding) as file:
        result = json.loads(file.read())
    return result


def save_file(path, data, mode='w', encoding='utf8'):
    with open(path, mode, encoding=encoding) as pf:
        json.dump(data, pf, ensure_ascii=False)


if __name__ == '__main__':
    js = open_file('../../QA/data/KUAKE-QIC_dev.json')
    for item in js:
        print(item['query'], item['label'])
