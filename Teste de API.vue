from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Carregar o CSV com os dados das operadoras
operadoras_df = pd.read_csv("operadoras_ativas.csv")

@app.route('/buscar', methods=['GET'])
def buscar_operadoras():
    termo = request.args.get('termo')
    resultado = operadoras_df[operadoras_df['nome'].str.contains(termo, case=False)]
    return jsonify(resultado.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(debug=True)
