from fastapi import FastAPI
from AgenciaBancaria import AgenciaBancaria

app = FastAPI()
agencia = AgenciaBancaria()

@app.get("/clientes")
def get_clientes(): return agencia.getClientes()

@app.get("/clientes/{cpf}")
def get_cliete_by_cpf(cpf): return agencia.getClientes(cpf)

@app.post("/clientes")
def post_cliente(cliente: dict):
    resultado = agencia.cadastrarCliente(cliente)
    
    if resultado: return successResponse('Cliente cadastro com sucesso.')
    else: return errorResponse('Erro durante o cadastro do cliente.')

@app.put("/clientes/{cpf}/alterar")
def setter(cpf, atributos: dict):
    for chave, valor in atributos.items():
        resposta = agencia.updateCliente(cpf, chave, valor)
        if not resposta: return errorResponse('Erro durante a atribução dos valores.')
    return successResponse('Atribuições realizadas com sucesso.')

@app.get("/contas")
def get_contas(): return agencia.getContas()

@app.get("/contas/{numero}")
def get_conta_by_numero(numero): return agencia.getContas(numero)

@app.post('/contas')
def post_conta(conta: dict):
    resultado = agencia.criarContaCliente(conta)
    
    if resultado: return successResponse('Conta cadastrada com sucesso.')
    else: return errorResponse('Erro durante o cadastro da conta.')

@app.get("/contas/{numero}/extrato")
def get_extrato(numero): return agencia.extrato(numero)

@app.put('/contas/{numero}/bloquear')
def bloquear_conta(numero):
    resultado = agencia.bloquearConta(numero)
    
    if resultado: return successResponse('Bloqueio da conta realizado com sucesso.')
    else: return errorResponse('Erro durante o bloqueio da conta.')

@app.put('/contas/{numero}/desbloquear')
def bloquear_conta(numero): 
    resultado = agencia.desbloquearConta(numero)
    
    if resultado: return successResponse('Desbloqueio da conta realizado com sucesso.')
    else: return errorResponse('Erro durante o desbloqueio da conta.')

@app.put("/contas/{numero}/debitar")
def debitar(numero, infos: dict):
    resultado = agencia.debitarConta(numero, infos)
    
    if resultado: return successResponse('Débitação da conta realizada com sucesso.')
    else: return errorResponse('Erro durante o débitação da conta.')

@app.put("/contas/{numero}/creditar")
def creditar(numero, infos: dict):
    resultado = agencia.creditarConta(numero, infos)
    
    if resultado: return successResponse('Creditação da conta realizada com sucesso.')
    else: return errorResponse('Erro durante o creditação da conta.')

@app.put("/contas/{numero}/transferir")
def transferir(numero, tranferencia: dict): 
    resultado = agencia.transferir(numero, tranferencia['numero_conta'], tranferencia['valor'])

    if resultado: return successResponse('Tranferência realizada com sucesso.')
    else: return errorResponse('Erro durante a tranferência da conta.')

def successResponse(message): return { "status": 200, "message": message }
def errorResponse(message): return { "status": 404, "message": message }