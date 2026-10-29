from setuptools import setup, find_packages

setup(
    name="buxdu-smart-admin",
    version="1.0.0",
    description="Smart Multilingual & New Uzbek Latin (2026) Assistant for Django Admin",
    author="BuxDU Tech Helper",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django>=3.2",
    ],
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
