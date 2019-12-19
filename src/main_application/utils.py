from os import walk


def extract_serializable_files_from(path):
    files = []
    for dir_path, dirnames, filenames in walk(path):
        files.extend(filenames)
        break

    acceptable_files = []
    for filename in files:
        if filename.endswith(('.csv', '.tree')):
            acceptable_files.append(filename)

    return acceptable_files
