from flask import Flask, render_template, request, send_file
import json
import os

app = Flask(__name__)

def texto_para_json(texto):
    if "True" in texto:
        texto = texto.replace("True", "true")
    if "False" in texto:
        texto = texto.replace("False", "false")

    return json.loads(json.dumps(texto, indent=2, ensure_ascii=False))

def salvar_json_em_arquivo(json_string, nome_arquivo):
    json_string = json_string.replace("'", '"')
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write(json_string)

def excluir_arquivo(nome_arquivo):
    try:
        os.remove(nome_arquivo)
    except Exception as e:
        print(f"Erro ao excluir o arquivo: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        texto = request.form['texto']
        json_string = texto_para_json(texto)
        nome_arquivo = request.form['nome_arquivo']

        if not nome_arquivo.endswith('.json'):
            nome_arquivo += '.json'

        salvar_json_em_arquivo(json_string, nome_arquivo)
        return render_template('download.html', nome_arquivo=nome_arquivo)

    return render_template('index.html')

@app.route('/download/<nome_arquivo>')
def download(nome_arquivo):
    caminho_arquivo = os.path.join(os.getcwd(), nome_arquivo)
    try:
        resposta = send_file(caminho_arquivo, as_attachment=True)
        excluir_arquivo(caminho_arquivo)  
        return resposta
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
