from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from TrainningDbEmdding import TrainningDbEmdding
import os
import requests

#Funcoes Comuns
DIR_PATH = "B:/workspace/escola"

def download_image(url, file_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(file_path, "wb") as file:
        file.write(response.content)

def create_directory(path):
    os.makedirs(path, exist_ok=True)



# Inicializando o Firebase
cred = credentials.Certificate("securitys/secedu-mobile-firebase-adminsdk-mbvfp-44cf27817c.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Inicializando o Flask
app = Flask(__name__)

# Rota para retornar todos os documentos de uma coleção do Firestore
@app.route('/contratos', methods=['GET'])
def get_contratos():
    try:
        # Obtém a coleção de contratos
        collection_ref = db.collection("contratos")
        docs = collection_ref.stream()

        # Itera sobre os documentos e armazena os dados em uma lista
        results = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            results.append(data)

        # Retorna a lista de documentos no formato JSON
        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/escolas', methods=['GET'])
def get_escolas():
    try:
        collection_ref = db.collection("escolas")
        docs = collection_ref.stream()

        results = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id

            # Verifica se o campo "protocol" existe no documento
            if 'protocol' in data:
                # Obtém o caminho completo do documento de referência
                protocol_ref = data['protocol']
                protocol_path = protocol_ref.path

                data['protocol'] = protocol_path  # Substitui o objeto DocumentReference pelo caminho completo

            results.append(data)

        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/turmas', methods=['GET'])
def get_turmas():
    try:
        collection_ref = db.collection("turmas")
        docs = collection_ref.stream()

        results = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id

            # Verifica se o campo "protocol" existe no documento
            if 'protocol' in data:
                # Obtém o caminho completo do documento de referência
                protocol_ref = data['protocol']
                protocol_path = protocol_ref.path

                data['protocol'] = protocol_path  # Substitui o objeto DocumentReference pelo caminho completo

            results.append(data)

        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Collection ALUNOS
@app.route('/alunos', methods=['GET'])
def get_alunos():
    try:
        collection_ref = db.collection("alunos")
        docs = collection_ref.stream()

        results = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id

            # Verifica se o campo "protocol" existe no documento
            if 'turma_id' in data:
                # Obtém o caminho completo do documento de referência
                protocol_ref = data['turma_id']
                protocol_path = protocol_ref.path

                data['turma_id'] = protocol_path  # Substitui o objeto DocumentReference pelo caminho completo

            results.append(data)

        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/alunos-por-turma', methods=['GET'])
def get_alunos_turma():
    try:
        turma_id = request.args.get('turma_id')
        turma_id_completo = f"turmas/{turma_id}"
        if turma_id is None:
            return jsonify({'error': 'Parâmetro turma_id não encontrado'}), 400
        # Obtém a referência do documento da turma com ID turma_id
        turma_doc_ref = db.document(turma_id_completo)

        # Obtém a referência da coleção "alunos"
        collection_ref = db.collection("alunos")

        # Faz a consulta filtrando pelo campo "turma_id" igual à referência da turma
        query = collection_ref.where("turma_id", "==", turma_doc_ref).stream()
        
        if not query:
            return {'error': 'Nenhum aluno encontrado para a turma informada'}
        
        results = []
        for doc in query:
            data = doc.to_dict()

            # Verifica se o campo "turma" existe no documento
            if 'turma_id' in data:
                # Obtém o caminho completo do documento de referência
                protocol_ref = data['turma_id']
                protocol_path = protocol_ref.path
                #print("data['turma_id']: ", protocol_path)

                data['turma_id'] = protocol_path  # Substitui o objeto DocumentReference pelo caminho completo

            results.append(data)

        #FOR para criar pasta e baixar img
        for aluno in results:
            ra = aluno["ra"]
            # print(aluno)
            if "captura_frontal" in aluno:
                captura_frontal_url = aluno["captura_frontal"]
                directory_path = os.path.join(DIR_PATH, str(ra))
                create_directory(directory_path)
                file_path = os.path.join(directory_path, "captura_frontal.jpg")
                download_image(captura_frontal_url, file_path)
            
            if "captura_left" in aluno:
                captura_left_url = aluno["captura_left"]
                directory_path = os.path.join(DIR_PATH, str(ra))
                create_directory(directory_path)
                file_path = os.path.join(directory_path, "captura_left.jpg")
                download_image(captura_left_url, file_path)
            
            if "captura_right" in aluno:
                captura_right_url = aluno["captura_right"]
                directory_path = os.path.join(DIR_PATH, str(ra))
                create_directory(directory_path)
                file_path = os.path.join(directory_path, "captura_right.jpg")
                download_image(captura_right_url, file_path)

        return results

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Execução da aplicação Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
