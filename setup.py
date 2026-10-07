from setuptools import find_packages,setup

def get_packages(filePath:str)->list[str]:
    '''this function returns the packages present inside the filePath'''
    try:
        package_list : list[str] = []
        with open(filePath, 'r') as file:
            packages = file.readlines()
            for package in packages:
                if package and package.strip() != "-e .":
                    package_list.append(package)
        return package_list
    except FileNotFoundError :
        print(f"File not found with {filePath}")

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author='banoth anil nayak',
    author_email='banothanilnayak50@gmail.com',
    packages= find_packages(),
    install_requires=get_packages('requirements.txt')
)