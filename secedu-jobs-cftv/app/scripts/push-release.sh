cd ..

echo "eliminação de ficheiros relacionados com a versão existente"
rm -rf dist/*
rm -rf build/*

echo "criar um pacote para a versão atual - compatível com pypi"
python setup.py sdist bdist_wheel

echo "enviando a versão para o pypi"
python -m twine upload dist/*
