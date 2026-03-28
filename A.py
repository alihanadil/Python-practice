import os

# Joining paths
path = os.path.join('folder', 'subfolder', 'file.txt')   # uses OS-specific separator

# Splitting
dirname = os.path.dirname(path)          # 'folder/subfolder'
basename = os.path.basename(path)        # 'file.txt'
split = os.path.split(path)              # ('folder/subfolder', 'file.txt')

# Getting absolute path
abs_path = os.path.abspath('file.txt')   # e.g., '/home/user/project/file.txt'

# Checking existence
exists = os.path.exists('file.txt')
is_file = os.path.isfile('file.txt')
is_dir = os.path.isdir('folder')

print(path)
print(dirname)
print(basename)
print(split)
print(abs_path)
print(exists)
print(is_file)
print(is_dir)

# # Size
# size = os.path.getsize('file.txt')       # bytes

# # Rename, remove
# os.rename('old.txt', 'new.txt')
# os.remove('file.txt')