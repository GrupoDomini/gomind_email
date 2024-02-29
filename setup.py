from setuptools import setup

setup(
    name="gomind_email",
    python_requires=">=3.6",
    version="0.0.1",
    description="GoMind email sender service",
    url="https://github.com/GrupoDomini/gomind_email.git",
    author="JeffersonCarvalhoGD",
    author_email="jefferson.carvalho@grupodomini.com",
    license="unlicense",
    packages=["gomind_email"],
    zip_safe=False,
    install_requires=["get-mac==0.9.2"],
)
