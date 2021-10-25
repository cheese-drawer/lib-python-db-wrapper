import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

short_description = \
    "Simple wrapper on aiopg to handle postgres connections & basic Models."

setuptools.setup(
    name="db_wrapper",
    version="2.1.0",
    author="Andrew Chang-DeWitt",
    author_email="andrew@andrew-chang-dewitt.dev",
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cheese-drawer/lib-python-db-wrapper/",
    packages=setuptools.find_packages(),
    package_data={
        'db_wrapper': ['py.typed']},
    install_requires=[
        'aiopg>=1.1.0,<2.0.0',
        'pydantic>=1.8.1,<2.0.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
