def read_file(file_name):
    f = open(file_name,'r')
    while True:
        line = f.readline()
        if line == '':
            break
        else:
            student_info = line.split('\t')
            student = {'name' = student_info[0],'age' = student_info[1],'qq' = student_info[2]}
            studentinfo.append(student)
            
def write_file(file_name):
    f = open(file_name,'w')
    for item in studentinfo:
        student = '%s\t%s\t%s'%(item['name'] ,item['age'],item['qq'])
        f.write(student)
    f.close()
    
def print_menu():
    print('='*30)
    print('Student Management System'.center(30))
    print('Enter1:add student')
    print('Enter2:search student')
    print('Enter3:modify student')
    print('Enter4:delete student')
    print('Enter5:check all students')
    print('Enter6:exit')

def add_student():
    name = input('Please enter the name of student:')
    age = int(input('Please enter the age of student:'))
    qq = input('Please enter the qq number of student:')
    stu = {}
    stu['name'] = name
    stu['age'] = age
    stu['qq'] = qq
    studentinfo.append(stu)
    print('Successfully add the student information.')

def search_student():
    name = input('Please enter the name of the student you want to search:')
    for item in studentinfo:
        if item['name'] == name.strip():
            print('%s exist, age: %d, qq: %s'%(item['name'],item['age'],item['qq']))
    else:
        print('%s is not exist, please add the information'%name)

def delete_student():
    name = input('Please enter the name of the student you want to remove:')
    for item in studentinfo:
        if item['name'] == name.strip():
            studentinfo.remove(item)
            print('Sucessfully remove %s from the database'% (name))
    else:
        print('%s is not exist, please try again.'%name)

def modify_student():
    name = input('Please enter the name of the student you want to edit:')
    for item in studentinfo:
        if item['name'] == name.strip():
            item['age'] = int(input('Please enter the age of student:'))
            item['qq'] = input('Please enter the qq number of student:')
    else:
        print('%s is not exist, please try again.'%name)

def print_all():
    print('nope\tname\tage\tqq\t')
    for i,item in enumerate(studentinfo,1):
        print('%s\t'%i, end='')
        print('%s\t%s\t%s\t'%(item['name'],item['age'],item['qq']))

def main():
    while True:
        read_file(file_name)
        studentinfo = []
        print_menu()
        choice = int(input())
        if choice == 1:
            add_student()
        elif choice == 2:
            search_student()
        elif choice == 3:
            modify_student()
        elif choice == 4:
            delete_student()
        elif choice == 5:
            print_all()
        else:
            break
            
file_name = ''
mian()
write_file(filename)

