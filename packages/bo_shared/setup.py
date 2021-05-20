from setuptools import setup, find_packages

setup(
    name='bo_shared',
    version='0.1.0',
    description='Shared bo materials',
    url='https://github.com/shalireza/BO',
    author='Alireza Shateri',
    author_email='alirezashateri7@gmail.com',
    license='MIT',
    packages=find_packages(where='.'),
    package_dir={'': '.'},
    install_requires=[
        'pydantic>=1.8.2'
    ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)
