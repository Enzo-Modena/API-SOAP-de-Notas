from zeep import Client

#conecta ao wsdl do servidor soap
client = Client(wsdl='http://127.0.0.1:8000/?wsdl')

#chama a operação consultar_aluno com RA = 1
resposta = client.service.consultar_aluno(ra=1)

print("=== Resultado da Consulta ===")
print(f"Nome: {resposta.nome}")
print(f"Nota 1: {resposta.nota1}")
print(f"Nota 2: {resposta.nota2}")
print(f"Média: {resposta.media}") 
print(f"Situação: {resposta.situacao}")

