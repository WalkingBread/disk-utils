import diskutils

for inf in diskutils.search_by_extension('D:\\Files', 'txt'):
    print(inf.name + " " + inf.path)