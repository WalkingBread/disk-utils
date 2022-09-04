import diskutils

x = {
    'recurrent': True,
    'explicit': False,
    'include_folders': True
}

for inf in diskutils.search_by_name('C:\\Users\\matis\\AppData', 'gi', x):
    print(inf.name + ', ' + inf.path)

#diskutils.delete_files_by_extension('C:\\Users\\matis\\Desktop', 'txt', x)