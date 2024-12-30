import subprocess
def custom_makemigrations():
    try:
        print('Im make migrations')
        command = ['python', 'manage.py', 'makemigrations']
        subprocess.run(command)

        return True
    except Exception as error:
        print('error',error)
        return error
def custom_migrate():
    try:
        print('im migrate')
        command = ['python', 'manage.py', 'migrate']
        subprocess.run(command)
        print('success')
        return True
    except Exception as error:
        print('error',error)
        return error