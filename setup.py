from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="onlyoffice-api-client",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Python client for ONLYOFFICE API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/onlyoffice-api-client",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.1",
        "python-dotenv>=0.15.0",
    ],
)
