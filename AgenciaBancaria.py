from random import randrange
from Conexao import Conexao

connBD = Conexao(host = 'localhost', user = 'postgres', password = 'root', database = 'Python_Banco')

class AgenciaBancaria:
    def cadastrarCliente(self, infos):
        connBD.insert(table = 'clientes', inserts = infos)
        return connBD.commit()

    def updateCliente(self, cpf_cliente, campo, novoValor):
        connBD.update(table = 'clientes', set = { campo: novoValor }, where = { 'cpf': cpf_cliente})
        return connBD.commit()

    def criarContaCliente(self, infos):
        select = connBD.selectAll(table = 'contas', calumns = 'numero')     
        numeros = [ i[0] for i in select ]

        while True:
            numero = str(randrange(10000)).zfill(4)
            if numero not in numeros: break 

        infos['numero'] = numero
        connBD.insert(table = 'contas', inserts = infos)
        return connBD.commit() and numero

    
    def getClientes(self, cpf = False):
        return connBD.selectAll(
            table = 'clientes', 
            columns = ('nome', 'idade', 'sexo', 'telefone', 'email', 'cpf'),
            where = cpf and { 'cpf': cpf }
        )
    
    def getContas(self, numero = False):
        return connBD.selectAll(
            table = 'contas', 
            columns = ('numero', 'senha', 'cpf_cliente', 'saldo', 'bloqueada'),
            where = numero and { 'numero': numero }
        )

    def bloquearConta(self, numero): return ContaBancaria(numero).bloquear()
    def desbloquearConta(self, numero): return ContaBancaria(numero).desbloquear()

    def creditarConta(self, numero, infos): 
        if ContaBancaria(numero).creditar(infos['valor']):
            self.inserirExtrato(**infos, numero_conta = numero) 
            return True
        return False

    def debitarConta(self, numero, infos): 
        if ContaBancaria(numero).debitar(infos['valor']):
            self.inserirExtrato(**infos, numero_conta = numero) 
            return True
        return False

    def transferir(self, numeroConta, numeroOutraConta, valor):
        infos = {
            'descricao': 'Tranferência',
            'origem': numeroOutraConta,
            'valor': valor
        }
        if ContaBancaria(numeroConta).transferir(valor, ContaBancaria(numeroOutraConta)):
            self.inserirExtrato(**infos, numero_conta = numeroConta)
            self.inserirExtrato(**infos, numero_conta = numeroOutraConta)
            return True
        return False

    def inserirExtrato(self, **infos):
        connBD.insert(table = 'extratos', inserts = infos)
        return connBD.commit()

    def extrato(self, numeroConta): 
        extrato = {}
        extrato['extrato'] = connBD.selectAll (
            table = 'extratos', 
            columns = ('valor', 'data_hora', 'descricao', 'origem'), 
            where = { 'numero_conta': numeroConta } 
        )
        extrato['saldo_atual'] = ContaBancaria(numeroConta).saldo
        return extrato

class ContaBancaria:
    def __init__(self, numero):
        self.__numero = numero
        self.table = 'contas'

    @property
    def numero(self): return self.__numero

    @property
    def saldo(self): return connBD.selectOne (
        table = self.table, columns = 'saldo', where = { 'numero': self.numero }
    )

    @saldo.setter
    def saldo(self, valor): 
        connBD.update(table = self.table, set = { 'saldo': valor }, where = { 'numero': self.numero })

    @property
    def bloqueada(self): return connBD.selectOne (
        table = self.table, columns = 'bloqueada', where = { 'numero': self.numero }
    )

    @bloqueada.setter
    def bloqueada(self, boolean): 
        connBD.update(table = self.table, set = { 'bloqueada': boolean }, where = { 'numero': self.numero })

    def debitar(self, valor): 
        if self.saldo < valor: return False
        self.saldo -= valor
        return connBD.commit()

    def creditar(self, valor): 
        self.saldo += valor
        return connBD.commit()

    def transferir(self, valor, conta): 
        if self.saldo < valor: return False
        self.saldo -= valor
        conta.saldo += valor
        return connBD.commit()

    def bloquear(self): 
        self.bloqueada = True
        return connBD.commit()
    
    def desbloquear(self): 
        self.bloqueada = False
        return connBD.commit()