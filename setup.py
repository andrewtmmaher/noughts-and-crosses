import setuptools
with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='noughts_and_crosses',
    version='0.1',
    scripts=['scripts/noughts_and_crosses'],
    author='Andrew Maher',
    author_email='andrewtmmaher@gmail.com',
    description='',
    install_requires=[
        'numpy',
        'scikit-learn',
        'scipy'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/andrewtmmaher/noughts-and-crosses',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)