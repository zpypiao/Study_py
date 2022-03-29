import os

#this function use absolutely addr
def find_str(parent_dir,dir_or_file,str):
    file_abspath = os.path.join(parent_dir,dir_or_file)
    if os.path.isdir(file_abspath):
        for f in os.list(file_abspath):
            find(file_abspath,f,str)
    else:
        if file_abspath.endwith('.py'):
            if read_find(file_abspath,str):
                file_list.append(file_abspath)
def read_find(dir,str):
    flag = False
    f = open(dir,'r')
    while True:
        line = f.readline()
        if line == '':
            break
        elif str in line:
            flag = True
     f.close()
     return flag

file_list = []
path = '/root/'
file = 'python'
find(path,file,'Hello')
print(file_list)
