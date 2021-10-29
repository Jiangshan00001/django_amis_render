# coding: utf-8

import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
	
setuptools.setup(
    name="django_amis_render",
    version="0.0.1",
    author="jiangshan00000",
    author_email="710806594@qq.com",
    description="a django app to render amis json file to web.",
	long_description=long_description,
	long_description_content_type = "text/markdown",
    url="https://github.com/Jiangshan00001/django_amis_render",
    packages=setuptools.find_packages(),
    include_package_data=True,

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	install_requires=[
    'django',
	],
)