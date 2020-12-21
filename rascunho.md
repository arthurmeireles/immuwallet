### FUNCIONALIDADES
- [ ] cadastro de vacinas e estoques
- [ ] cadastro de profissionais e vínculos
- [ ] gerenciar agenda e fila de atendimento
- [ ] gerenciar estoque e aplicação de vacina
- [ ] autocadastro de paciente


### ATORES

#### Coordenador do SUS
- importar estados, municípios e estabelecimentos
- cadastrar vacinas, profissionais e seus vínculos

#### Profissional de saúde
- gerenciar agenda do estabelecimento
- chamar pacientes da fila de espera

#### Paciente
- marcar vacinação
- autonotificar vacina


### REQUISITOS
- ver relatório de vacinas aplicadas
- controlar agenda do estabelecimento (horários de funcionamento)
- diferenciar vacina de autovacina

### PROJETO DO BANCO

#### Usuário
- nome, cpf

#### Perfil
- paciente|profissional|coordenador
- estabelecimento

#### Estado
- codigo, nome

#### Município
- estado, codigo, nome

#### Estabelecimento
- tudo do CSV
- horario de funcionamento

#### Vacina
- código, nome, tempo de aplicação

#### Vacina Estocada
- data, estabelecimento, quantidade, quantidadeAtual

#### Vacina Aplicada
- data, estabelecimento, agendamento?, vacina, aplicador, aplicando

#### Horário de funcionamento
- dia da semana, hora de abertura e de fechamento
- dia específico

#### Horário de atendimento
- data, estabelecimento, status, comentário, ocupado por, atendido por

### TELAS

#### Landing page

introdução, links, login

#### Login

autocadastro, autenticação, oauth

#### Index do gestor

- pré-cadastrar um usuário, associar vínculo
- listar e cadastrar estabelecimento
- visualizar relatório
- listar e cadastrar estoque

#### Index do profissional

- visualizar relatório
- listar e cadastrar estoque
- modificar horário de funcionamento
- Gerenciar fila de espera

#### Index do paciente

- visualizar e buscar estabelecimentos
- agendar vacinação
- ver lista de espera