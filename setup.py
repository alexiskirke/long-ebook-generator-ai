from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="long_ebook_generator_ai",
    version="1.0.2",
    author="Alexis Kirke",
    author_email="alexiskirke2@gmail.com",
    description="An A.I. tool for generating long Kindle ebooks based on a prompt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "openai",
        "tiktoken",
        "ebooklib",
        "Pillow",
        "requests",
        "latex2mathml",
    ],
)
