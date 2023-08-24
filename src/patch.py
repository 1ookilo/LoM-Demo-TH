import os
import json
import UnityPy

root = os.path.dirname(os.path.realpath(__file__))
path_asset = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
path_localize = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Localize', 'utf8')
path_release = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Release')
def check_blacklist():
    src = os.path.join(root, "path_id.json")
    with open(src, "r") as f:
        data = json.load(f)
        blacklist = data["blacklist"]
    return blacklist

def readjson():
    src = os.path.join(path_localize, "Localize.json")
    with open(src, 'r', encoding='utf-8') as f:  # Open with explicit encoding
        data = json.load(f)
    return data

def check_and_assign(data_asset, localize):
    text = data_asset.text
    updated_text_lines = []

    for line in text.splitlines():
        if 'say("' in line:
            for item in localize:
                original_value = item.get("original", "").strip()
                translation_value = item.get("translation", "")
                stage_value = item.get("stage", "")

                if original_value in line and stage_value == 1:
                    line = line.replace(original_value, translation_value)
                    break
        updated_text_lines.append(line)

    updated_text = '\n'.join(updated_text_lines)
    data_asset.text = updated_text
    return data_asset

def main():
    localize = readjson()
    src = os.path.join(path_asset, "resources.assets")
    assets = UnityPy.load(src)
    for o in assets.objects:
        if o.type.name in ['TextAsset']:
            data_asset = o.read()
            blacklist = check_blacklist()

            if not data_asset.path_id in blacklist:
                check_and_assign(data_asset, localize)
                data_tran = check_and_assign(data_asset, localize)
                data_asset = data_tran
                text = data_tran.text

            data_asset.save()
            with open(os.path.join(path_release, "Mortal_Data/resources.assets"), "wb") as f:
                f.write(assets.file.save())


if __name__ == '__main__':
    main()


