import json
import os
import re
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from classes.ObjectsTemplate import ObjectsTemplate



def split_objects(content: str):
    """Dzieli tekst na fragmenty odpowiadające pojedynczym obiektom JSON"""
    objs = []
    brace_count = 0
    start = 0
    for i, ch in enumerate(content):
        if ch == '{':
            if brace_count == 0:
                start = i
            brace_count += 1
        elif ch == '}':
            brace_count -= 1
            if brace_count == 0:
                objs.append(content[start:i+1])
    return objs

def parse_object_with_comments(obj_text: str):
    """Parsuje jeden obiekt JSON, zachowując komentarze jako *_comment"""
    comments = {}
    processed_lines = []
    for line in obj_text.splitlines():
        match = re.search(r"//(.*)", line)
        if match:
            comment = match.group(1).strip()
            line = re.sub(r"//.*", "", line)
            key_match = re.search(r'"(\w+)"\s*:', line)
            if key_match:
                key = key_match.group(1)
                comments[f"{key}_comment"] = comment
        processed_lines.append(line)

    clean_text = "\n".join(processed_lines)
    obj = json.loads(clean_text)

    # dodajemy komentarze tylko do tego obiektu
    obj.update(comments)
    return obj

def load_json_with_comments(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # usuwamy przecinki na końcu obiektów (luźny JSON)
    content = re.sub(r",\s*}", "}", content)
    content = re.sub(r",\s*]", "]", content)

    # dzielimy na obiekty
    objs = split_objects(content)

    data = []
    for obj_text in objs:
        data.append(parse_object_with_comments(obj_text))

    return data

def json_to_objectTemplate(data):
    objectTempltes = []
    for row in data:
        obj = ObjectsTemplate(
            row['def'],
            row['passability'],
            row['actionability'],
            row['allowed_landscapes'],
            row['landscape_group'],
            row['object_class'],
            row['object_subclass'],
            row['object_group'],
            row['is_ground'],
            row['unknown']
        )

        objectTempltes.append(obj)
    return objectTempltes

def read_object_templates_from_json(filename):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"templates\\{filename}.json")
    data = load_json_with_comments(path)
    return json_to_objectTemplate(data)

if __name__ == "__main__":
    path = "templates\\towns.json"
    filename = "towns"
    r = read_object_templates_from_json(filename)

    print("✅ Wygenerowano")