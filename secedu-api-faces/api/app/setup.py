import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().split("\n")

setuptools.setup(
    name="SecEdu-Face-Recognition",
    version="0.0.1",
    author="Edson Lourenço B. Filho",
    author_email="edcastanha@gmail.com",
    description="Uma estrutura de reconhecimento facial e análise de atributos faciais (idade, género, emoção, raça) para Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edcastanha/secedu",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
  
    python_requires=">=3.5.5",
    install_requires=requirements,
)
