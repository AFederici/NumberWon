from setuptools import setup, find_packages

def do_setup():
    setup(name='numberwon',
          version="1.0",
          author="AJ Federici, Michael Huang, Megan Kaye, Christine Zhao",
          description='Facial Recognition and clustering as well as Song Fingerprinting',
          platforms=['Windows', 'Linux', 'Mac OS-X', 'Unix'],
          packages=find_packages())
if __name__ == "__main__":
    do_setup()