import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# Use a service account.

# Connect Firebase DB
cred = credentials.Certificate("../securitys/secedu-mobile-firebase-adminsdk-mbvfp-44cf27817c.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

### FUNCTIONS# Rota para retornar todos os documentos de uma coleção do Firestore
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
        return results

    except Exception as e:
        return {'error': str(e)}

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

        return results

    except Exception as e:
        return {'error': str(e)}

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

        return results

    except Exception as e:
        return {'error': str(e)}

#Collection ALUNOS
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

        return results

    except Exception as e:
        return {'error': str(e)}

def get_alunos_turma(turma_id):
    try:
        if turma_id is None:
            return {'error': 'Parâmetro turma_id não encontrado'}
        # Obtém a referência do documento da turma com ID turma_id
        turma_doc_ref = db.document(turma_id)

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
                print("data['turma_id']: ", data['turma_id'])
                # Obtém o caminho completo do documento de referência
                protocol_ref = data['turma_id']
                protocol_path = protocol_ref.path

                data['turma_id'] = protocol_path  # Substitui o objeto DocumentReference pelo caminho completo

            results.append(data)

        return results

    except Exception as e:
        return {'error': str(e)}


if db:
    #escolas = get_escolas()
    #turmas = get_turmas()
    #alunos = get_alunos()

    doc_alunos = get_alunos_turma("turmas/D0001")
    print("Alunos: ", doc_alunos)

    #for turma in turmas:
    #    turma_id = turma['id']
    #    turma_id_completo = f"turmas/{turma_id}"  # Adicionando o prefixo "turmas/" para coincidir com o formato do campo 'turma_id' dos alunos
    #    print("Turma ID:", turma_id)
    #    print("Alunos:", alunos)
    #    alunos_filtrados = list(filter(lambda aluno: aluno['turma_id'] == turma_id_completo, alunos))  # Usando o turma_id_completo para fazer a comparação
    #    print("Alunos filtrados:", alunos_filtrados)

else:
    print("Erro ao conectar ao Firebase")


# Execução da aplicação Flask
#if __name__ == '__main__':
#    app.run(debug=True)
