from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='py_debug',
    version='0.1.0',
    author='DDSurok',
    author_email='ddsurok@gmail.com',
    description='This is the simplest module for logging functions.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.io/DDSurok/py-debug',
    packages=find_packages(include=['py_debug', 'tests']),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='logging log debug',
    project_urls={
        'GitHub': 'https://github.io/DDSurok/py-debug'
    },
    python_requires='>=3.8'
)
