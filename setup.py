from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('VERSION') as f:
    version = f.read()

setup(name='elb-instance-manager',
      version=version,
      description='A simple HTTP service to manage instances in a ELB',
      long_description=readme,
      author='Diogo Nicoleti',
      author_email='diogo.nicoleti@gmail.com',
      url='https://github.com/diogonicoleti/elb-instance-manager',
      license=license)
