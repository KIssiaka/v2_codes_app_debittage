from setuptools import setup, find_packages

setup(
    name='ubuntu-optimizer',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A project to develop innovative features and shortcuts for optimizing the Ubuntu system.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # List your project dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.6',
)