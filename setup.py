import setuptools

setuptools.setup(
    name="pyocpi",
    version="0.0.1",
    author="Florian Maurer",
    author_email="maurer@fh-aachen.de",
    description="python package for the open charge point interface",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'flask',
        'flask-restx',
    ],
)
