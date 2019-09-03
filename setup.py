import setuptools

setuptools.setup(
    name='dlinfo',
    use_scm_version=True,
    packages=setuptools.find_packages(),
    setup_requires=[
        'setuptools_scm',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pylint',
        # https://github.com/PyCQA/pylint/issues/2694
        'pylint>=2.3.0',
    ],
)
