import os

class FSObjectInfo:
    def __init__(self, parent_path, path, name):
        self.name = name
        self.path = path
        self.parent_path = parent_path

class FileInfo(FSObjectInfo):
    def __init__(self, parent_path, path, name, extension=None):
        super().__init__(parent_path, path, name)
        self.extension = extension

class FolderInfo(FSObjectInfo):
    def __init__(self, parent_path, path, name):
        super().__init__(parent_path, path, name)

def search_by_name_rule(info, searched_name):
    results = []
    if type(info) is FolderInfo:
        results += search(info.path, searched_name, search_by_name_rule)
    if searched_name.lower() in info.name.lower():
        results.append(info)
    return results

def search_by_extension_rule(info, searched_extension):
    results = []
    if type(info) is FolderInfo:
        results += search(info.path, searched_extension, search_by_extension_rule)
    elif type(info) is FileInfo:
        if info.extension is not None:
            if searched_extension.lower() in info.extension.lower():
                results.append(info)
    return results

def search(directory, searched_phrase, search_rule):
    results = []
    directory = os.path.abspath(directory)
    for fs_object in os.scandir(directory):
        fs_info_object = None
        if fs_object.is_dir():
            fs_info_object = FolderInfo(directory, fs_object.path, fs_object.name)
        else:
            split_name = fs_object.name.rsplit('.', 1)
            filename = split_name[0]
            ext = None
            if len(split_name) > 1:
                ext = split_name[1]
            fs_info_object = FileInfo(directory, fs_object.path, filename, ext)
        results += search_rule(fs_info_object, searched_phrase)
    return results

def search_by_name(directory, name):
    return search(directory, name, search_by_name_rule)

def search_by_extension(directory, extension):
    return search(directory, extension, search_by_extension_rule)

