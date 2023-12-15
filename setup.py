from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='d-debug',
  version='0.0.1',
  author='DDSurok',
  author_email='ddsurok@gmail.com',
  description='This is the simplest module for logging functions.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.io/DDSurok',
  packages=find_packages(),
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='logging log debug',
  project_urls={
    'GitHub': 'https://github.io/DDSurok'
  },
  python_requires='>=3.6'
)