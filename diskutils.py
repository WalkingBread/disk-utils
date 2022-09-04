import os

def get_fs_object_size(path):
    return os.path.getsize(path)

class FSObjectInfo:
    def __init__(self, parent_path, path, name):
        self.name = name
        self.path = path
        self.parent_path = parent_path
        self.size = get_fs_object_size(path)

class FileInfo(FSObjectInfo):
    def __init__(self, parent_path, path, name, extension=None):
        super().__init__(parent_path, path, name)
        self.extension = extension

class FolderInfo(FSObjectInfo):
    def __init__(self, parent_path, path, name):
        super().__init__(parent_path, path, name)

def split_file_name(name):
    split_name = name.rsplit('.', 1)
    filename = split_name[0]
    ext = None
    if len(split_name) > 1:
        ext = split_name[1]
    return (filename, ext)

def name_check(searched_phrase, found_phrase, explicit):
    if explicit:
        return searched_phrase.lower() == found_phrase.lower()
    return searched_phrase.lower() in found_phrase.lower()

def search_by_name_rule(info, searched_name, search_config):
    results = []
    if type(info) is FolderInfo:
        if search_config['recurrent']:
            results += search(info.path, searched_name, search_by_name_rule, search_config)
        if search_config['include_folders']:
            if name_check(searched_name, info.name, search_config['explicit']):
                results.append(info)
    elif type(info) is FileInfo:
        if search_config['include_files']:
            if name_check(searched_name, info.name, search_config['explicit']):
                results.append(info)            
    return results

def search_by_extension_rule(info, searched_extension, search_config):
    results = []
    if type(info) is FolderInfo:
        if search_config['recurrent']:
            results += search(info.path, searched_extension, search_by_extension_rule, search_config)
    elif type(info) is FileInfo:
        if info.extension is not None:
            if name_check(searched_extension, info.extension, search_config['explicit']):
                results.append(info)      
    return results

def search(directory, searched_phrase, search_rule, search_config):
    results = []
    directory = os.path.abspath(directory)
    for fs_object in os.scandir(directory):
        fs_info_object = None
        if fs_object.is_dir():
            fs_info_object = FolderInfo(directory, fs_object.path, fs_object.name)
        else:
            filename, ext = split_file_name(fs_object.name)
            fs_info_object = FileInfo(directory, fs_object.path, filename, ext)
        results += search_rule(fs_info_object, searched_phrase, search_config)
    return results

def search_by_name(directory, name, search_config={}):
    if 'recurrent' not in search_config:
        search_config['recurrent'] = True
    if 'explicit' not in search_config:
        search_config['explicit'] = False
    if 'include_files' not in search_config:
        search_config['include_files'] = True
    if 'include_folders' not in search_config:
        search_config['include_folders'] = True
    return search(directory, name, search_by_name_rule, search_config)

def search_by_extension(directory, extension, search_config={}):
    if 'recurrent' not in search_config:
        search_config['recurrent'] = True
    if 'explicit' not in search_config:
        search_config['explicit'] = False
    return search(directory, extension, search_by_extension_rule, search_config)

def delete_files_by_extension(directory, extension, search_config={}):
    files = search_by_extension(directory, extension, search_config)
    for file in files:
        os.remove(file.path)

