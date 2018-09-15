try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='kinoa',
      version='0.0.2',
      description='Library for experiments logging.',
      long_description=open('README.md').read(),
      url='https://github.com/oleg-panichev/kinoa',
      license='Apache License Version 2.0',
      author='Oleg Panichev',
      author_email='olegxpanichev@gmail.com',
      packages=['kinoa'],
      install_requires=[
          'numpy', 
          'matplotlib', 
          'pandas',
          'scipy>=0.14.0', 
          'scikit-learn>=0.18'],
      )
