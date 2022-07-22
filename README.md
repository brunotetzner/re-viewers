<p style="font-weight:bold;text-align:center;font-size:30px">Re:Viewers API</p>
Procurando uma API para seu site de 

# <p style="font-weight:bold;text-align:center">Registro</p>
<br>

## Rota
### `POST /users/register/`
<br>

## Requisição válido
```json
{
	"email": "gustavo@mail.com",
	"password": "1234",
	"first_name": "gustavo",
	"last_name": "oliveira "
}
```

### <p style="color:green;font-weight:bold;text-align:center">Response - 201 CREATED</p>
```json
{
  "id": "386d77b8-0825-4;text-align:centera45-a4f0-a17d14ef75e7",
  "email": "gustavo@mail.com",
  "first_name": "gustavo",
  "last_name": "oliveira",
  "create_at": "2022-07-21T13:23:10.348577Z",
  "update_at": "2022-07-21T13:23:10.348619Z"
}
```
<br>
<hr>
<br>

## Requisição inválida
+ Não passando algum dos campos obrigatórios.
```json
{
	"email": "gustavo1@mail.com",	
	"last_name": "oliveira "
}
```

### <p style="color:red;font-weight:bold;text-align:center">Response - 400 BAD REQUEST</p>

```json
{
  "first_name": [
    "This field is required."
  ],
  "password": [
    "This field is required."
  ]
}
```
<br>

+ Informando um e-mail já previamente cadastrado.

```json
{
	"email": "gustavo@mail.com",
	"password": "1234",
	"first_name": "gustavo",
	"last_name": "oliveira "
}
```

### <p style="color:orange;font-weight:bold;text-align:center">Response - 409 CONFLICT</p>

```json
{
  "error": "Email already exists"
}
```
<br>

# <p style="font-weight:bold;text-align:center"> Login</p>

## Rota
### `POST /users/login/`
<br>

## Requisição válido
+ Qualquer outra chave será ignorada.

```json
{
	"email": "gustavo@mail.com",
	"password": "1234"
}
```
### <p style="color:#00ff00;font-weight:bold;text-align:center">Response - 200 OK</p>
```json
{
  "token": "a3824506034c70589b93d1a00a884b7180cc1224"
}
```
<br>
<hr>
<br>

## Requisição inválida
+ Credenciais incorretas
  
```json
{
	"email": "gustavo@mail.com",
	"password": "asdasd"
}
```

### <p style="color:orange;font-weight:bold;text-align:center">Response - 401 UNAUTHORIZED</p>
```json
{
  "error": "Invalid credentials"
}
```
<br>

+ Não passando algum dos campos obrigatórios.

```json
{
	"email": "gustavo@mail.com"
}
```

### <p style="color:red;font-weight:bold;text-align:center">Response - 400 BAD REQUEST</p>

```json
{ 
  "password": [
    "This field is required."
  ]
}
```
<br>

# <p style="font-weight:bold;text-align:center">Perfil do usuário</p>
<p>Para todas as rotas seguras é necessário informar o <code>token</code> de acesso recebido através do login.</p>
<p>Pode ser feito de dois modos, através do <code>Bearer Token</code> ou <code>Authorization Header</code>.</p>

|Bearer Token| Dados
|------------|----
|TOKEN|a3824506034c70589b93d1a00a884b7180cc1224|
|PREFIX|Token

<br>

|Header| Dados|
|-----|----
|Authorization|Token a3824506034c70589b93d1a00a884b7180cc1224|



<br>

## Rota segura
### `POST /users/profile/`
<br>

## Requisição válida
+ Não é necessário passar nada no body, a consulta é feita através do token do próprio usuário.
```json
{}
```

### <p style="color:#00ff00;font-weight:bold;text-align:center">Response - 200 OK</p>
```json
{
  "id": "386d77b8-0825-4a45-a4f0-a17d14ef75e7",
  "email": "gustavo@mail.com",
  "first_name": "gustavo",
  "last_name": "oliveira",
  "create_at": "2022-07-21T13:23:10.348577Z",
  "update_at": "2022-07-21T13:23:10.348619Z"
}
```
<br>
<hr>
<br>

## Requisição inválida
+ Não sendo informado o token de autorização.
  
```json
{}
```
### <p style="color:orange;font-weight:bold;text-align:center">Response - 401 UNAUTHORIZED</p>
```json
{
  "detail": "Authentication credentials were not provided."
}
```

<br>

# <p style="font-weight:bold;text-align:center">Listar todos os usuários</p>
Para listar todos os usuário é necessário possuir um `token` de administrador.

## Rota segura (administrador)
### `POST /users/`
<br>

## Requisição válida

+ Não é necessário passar nada no body.
```json
{}
```
### <p style="color:#00ff00;font-weight:bold;text-align:center">Response - 200 OK</p>
```json
[
  {
    "id": "386d77b8-0825-4a45-a4f0-a17d14ef75e7",
    "email": "gustavo@mail.com",
    "first_name": "gustavo",
    "last_name": "oliveira",
    "create_at": "2022-07-21T13:23:10.348577Z",
    "update_at": "2022-07-21T13:23:10.348619Z"
  },
  {
    "id": "386d77b8-0825-4a45-a4f0-a17d14ef75e7",
    "email": "gustavo@mail.com",
    "first_name": "gustavo",
    "last_name": "oliveira",
    "create_at": "2022-07-21T13:23:10.348577Z",
    "update_at": "2022-07-21T13:23:10.348619Z"
  }
]
```
<br>
<hr>
<br>

## Requisição inválida
+ Informando um token de usuário não administrador.
  
```json
{}
```
### <p style="color:orange;font-weight:bold;text-align:center">Response - 403 FORBIDDEN</p>
```json
{
  "detail": "You do not have permission to perform this action."
}
```

<br>

+ Não sendo informado o token de autorização.
  
```json
{}
```
### <p style="color:orange;font-weight:bold;text-align:center">Response - 401 UNAUTHORIZED</p>
```json
{
  "detail": "Authentication credentials were not provided."
}
```
<br>

# <p style="font-weight:bold;text-align:center">Listar usuário por id</p>
Para listar um usuário expecífico por id é necessário possuir um `token` de administrador.

## Rota segura (administrador)
### `POST /users/<id>`
<br>

## Requisição válida

+ Não é necessário passar nada no body.
```json
{}
```

+ É necessário passar o id nos parâmetros da requisição:
  `/users/<id>`
  <br><br>
  Exemplo: `/users/386d77b8-0825-4a45-a4f0-a17d14ef75e7`
  

### <p style="color:#00ff00;font-weight:bold;text-align:center">Response - 200 OK</p>
```json
  {
    "id": "386d77b8-0825-4a45-a4f0-a17d14ef75e7",
    "email": "gustavo@mail.com",
    "first_name": "gustavo",
    "last_name": "oliveira",
    "create_at": "2022-07-21T13:23:10.348577Z",
    "update_at": "2022-07-21T13:23:10.348619Z"
  }  
```
<br>
<hr>
<br>

## Requisição inválida
+ Informando um token de usuário não administrador.
  
```json
{}
```
### <p style="color:orange;font-weight:bold;text-align:center">Response - 403 FORBIDDEN</p>
```json
{
  "detail": "You do not have permission to perform this action."
}
```

<br>

+ Não sendo informado o token de autorização.
  
```json
{}
```
### <p style="color:orange;font-weight:bold;text-align:center">Response - 401 UNAUTHORIZED</p>
```json
{
  "detail": "Authentication credentials were not provided."
}
```