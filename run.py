"""
Input: disease_catalog.csv and disease.csv

Output: 

AntDesign multilevel selector

[{
  "value": "A00-B99",
  "label": "某些传染病和寄生虫病",
  "children": [{
    "value": "A00-A09",
    "label": "肠道传染病",
    "children": [{
      "value": "A00",
      "label": "霍乱",
    }],
    ...
  }],
  ...
}]
"""

import csv
import json

cat1_children = {}  # {cat1_code: children_list}
cat2_children = {}  # {cat2_code: children_list}
res = []            # final array for jsonify
diseases = []       # disease rows container


def in_code_range(code, code_range):
    start, end = code_range.split('-')
    return start <= code <= end

with open('disease.csv') as file:
    reader = csv.DictReader(file, delimiter='\t')
    diseases = [row for row in reader]

with open('disease_catalog.csv') as file:
    reader = csv.DictReader(file, delimiter='\t')
    for row in reader:
        code = row['code_lower_bound'] + '-' + row['code_upper_bound']
        if row['level'] == "1":
            _children = []
            cat1_children[code] = _children
            res.append({
                'value': code,
                'label': row['catalog'],
                'children': _children,
            })
            continue
        cat2_children[code] = []
        _children.append({
            'value': code,
            'label': row['catalog'],
            'children': cat2_children[code],
        })

for d in diseases:
    is_inserted = False
    for k, v in cat2_children.items():
        if in_code_range(d['code'], k):
            v.append({
                'value': d['code'],
                'label': d['disease'],
            })
            is_inserted = True
            break
    if is_inserted:
        continue
    for k, v in cat1_children.items():
        if in_code_range(d['code'], k):
            v.append({
                'value': d['code'],
                'label': d['disease'],
            })

with open('diseases.json', 'w', encoding='utf-8') as file:
    json.dump(res, file, ensure_ascii=False, separators=(',', ':'))
