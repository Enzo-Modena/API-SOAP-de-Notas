from spyne import ComplexModel, Integer, Unicode, Float

class AlunoModel(ComplexModel):
    ra = Integer
    nome = Unicode
    nota1 = Float
    nota2 = Float
    media = Float
    situacao = Unicode
