import setuptools

with open('README.rst', 'r') as readme:
    LONG_DESCRIPTION = readme.read()

setuptools.setup(
    name='dlinfo',
    use_scm_version=True,
    maintainer='Cloudflight Space',
    maintainer_email='aerospace@cloudflight.io',
    description="Python wrapper for libc\'s dlinfo and dyld_find on Mac",
    long_description=LONG_DESCRIPTION,
    license="MIT",
    url='https://github.com/cloudflightio/python-dlinfo',
    packages=setuptools.find_packages(),
    python_requires=">=3.7",  # >=3.6 for f-strings, <3.7 untested
    setup_requires=["setuptools_scm"],
    tests_require=["pytest"],
    classifiers=[
        # https://pypi.org/classifiers/
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        # see .github/workflows/python.yml
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
    ],
)
