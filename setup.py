import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="db_wrapper",
    version="0.1.4",
    author="Andrew Chang-DeWitt",
    author_email="andrew@andrew-chang-dewitt.dev",
    description="Simple wrapper on aiopg to handle postgres connections & basic Models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cheese-drawer/lib-python-db-wrapper/",
    packages=setuptools.find_packages(),
    package_data={
        'db_wrapper': ['py.typed']},
    install_requires=[
        'aiopg>=1.1.0,<2.0.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
