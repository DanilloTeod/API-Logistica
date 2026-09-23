# API

- Listar motoristas: GET /motoristas/
[
    {
        "nome": "",
        "cpf": "",
        "cnh": "",
        "telefone": "",
        "ativo": "",
    }
]

- Detalhar motorista: GET /motoristas/<id>/
[
    {
        "nome": "",
        "cpf": "",
        "cnh": "",
        "telefone": "",
        "ativo": "",
    }
]

- Detalhar caminhão: GET /caminhoes/<id>/
[
    {
        "placa": "",
        "modelo": "",
        "motorista atual": "" 
    }
]

- Detalhar encomenda: GET /pacotes/<id>/
[
    {
        "cliente": "",
        "codigo de rastreio": "",
        "destino": "",
        "status": "",
    }
]

- Adicionar motorista: POST /motoristas/

- Adicionar caminhão: POST /caminhoes/

- Adicionar encomenda: POST /pacotes/

- Excluir motorista: DELETE /motoristas/<id>/

- Excluir caminhão: DELETE /caminhoes/<id>/

- Excluir encomenda: DELETE /pacotes/<id>/

- Editar um motorista: PUT/PATCH /motoristas/<id>/

- Editar um caminhão: PUT/PATCH /caminhoes/<id>/

- Editar uma encomenda: PUT/PATCH /pacotes/<id>/