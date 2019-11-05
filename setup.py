import setuptools

with open('README.rst', 'r') as readme:
    LONG_DESCRIPTION = readme.read()

setuptools.setup(
    name='dlinfo',
    use_scm_version=True,
    author='Fabian Peter Hammerle',
    author_email='fabianpeter.hammerle@catalysts.cc',
    maintainer='Catalysts Space',
    maintainer_email='space@catalysts.cc',
    description="Python wrapper for libc\'s dlinfo and dyld_find on Mac",
    long_description=LONG_DESCRIPTION,
    url='https://code.grasp-open.com/grasp-tools/python-dlinfo',
    packages=setuptools.find_packages(),
    setup_requires=[
        'setuptools_scm',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        # https://github.com/PyCQA/pylint/issues/2694
        'pylint>=2.3.0',
    ],
    classifiers=[
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
    ],
)
