import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().split("\n")

setuptools.setup(
    name="secedu",
    version="0.0.11",
    author="Edson L Bezerra Filho",
    author_email="edcastanha@gmail.com",
    description="Uma estrutura leve de reconhecimento facial e análise de atributos faciais (idade, género, emoção, raça) para Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edcastanha/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ["secedu = deepface.DeepFace:cli"],
    },
    python_requires=">=3.5.5",
    install_requires=requirements,
)
