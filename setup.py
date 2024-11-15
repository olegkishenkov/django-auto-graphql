import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-auto-graphql", # Replace with your own username
    version="0.0.6",
    author="olegkishenkov",
    author_email="oleg.kishenkov@gmail.com",
    description="an automatic GraphQL API for all the models in a Django project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olegkishenkov/django-auto-graphql",
    packages=setuptools.find_packages(where='auto_graphql'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.1',
)
