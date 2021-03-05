create table clientes (
    nome varchar(100) not null,
    idade int not null,
    sexo varchar(10) not null,
    telefone varchar(15),
    email varchar not null,
    cpf varchar(14) not null,
    constraint cpf_pk primary key (cpf)
);

create table contas (
    numero char(4) not null,
    senha varchar(6) not null,
    cpf_cliente varchar(14) not null,
    saldo float not null default 0.00,
    bloqueada boolean not null default false,
    constraint numero_conta_pk primary key (numero),
    constraint cpf_cliente_fk foreign key (cpf_cliente) references clientes (cpf) on delete cascade
);

create table extratos (
    numero_conta char(4) not null,
    valor float not null,
    data_hora TIMESTAMP not null default CURRENT_TIMESTAMP,
    descricao text,
    origem varchar,
    constraint numero_conta_fk foreign key (numero_conta) references contas (numero) on delete cascade
);