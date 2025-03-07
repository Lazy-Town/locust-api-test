# 📌 Locust API Test

Este repositório contém um **script de teste de carga** utilizando a biblioteca [Locust](https://locust.io/) para testar uma API protegida por `Ocp-Apim-Subscription-Key`.

O script segue **três etapas principais**:
1. **Envia um CPF via POST** e recebe um `id`.
2. **Consulta o status** desse `id` via POST.
3. **Obtém o resultado final** usando esse `id` via POST.

O objetivo é medir o desempenho da API sob carga e identificar possíveis gargalos.

---

## ⚠️ Requisitos

Este projeto requer **Python 3.8 ou superior**.

Verifique sua versão com:

```sh
python --version
```

Se necessário, instale uma versão compatível [aqui](https://www.python.org/downloads/).

Além disso, o **Locust** precisa estar instalado.

---

## 📜 Como Usar

### 🔹 Configurar o Script

Antes de rodar o teste, edite o arquivo `locustfile.py` e substitua:

- `"xxxx"` pela **URL correta** da API.
- `"Ocp-Apim-Subscription-Key"` pela **chave de autenticação**.

### 🔹 Executar o Locust

1. Inicie o Locust com o seguinte comando:

   ```sh
   locust -f locustfile.py
   ```

2. Abra um navegador e acesse:

   ```
   http://localhost:8089
   ```

3. Configure os testes na interface:
   - **Número de usuários simulados** (exemplo: 10, 100, 1000).
   - **Taxa de spawn (usuários por segundo)**.
   - **URL da API**.

4. Clique em **Start Swarming** para iniciar os testes.

---

## 🖥️ Fluxo do Script

O código segue a seguinte lógica:

1. **Autenticação**  
   - Adiciona o cabeçalho `Ocp-Apim-Subscription-Key`.

2. **Envio do CPF (POST)**  
   - O CPF é enviado para a API.  
   - Se a resposta for **202**, um `id` é retornado.

3. **Consulta de Status (POST)**  
   - O script consulta o status do `id` periodicamente (a cada 5s).  
   - Se o status for **PENDING**, continua esperando.  
   - Se o status for **FAILED**, o teste falha.  
   - Se o status for **SUCCESS**, passa para a próxima etapa.

4. **Obtenção do Resultado Final (POST)**  
   - A API retorna os dados finais.  
   - Se o status for **200**, o resultado é impresso.  
   - Se houver erro, ele é exibido.

5. **Finalização**  
   - O script **para automaticamente** após a execução de um usuário.

---

## 📊 Exemplo de Saída

Durante a execução, o console pode exibir algo como:

```
Erro ao enviar CPF: {"message": "Invalid CPF"}
Esse é o status 400
-------------------------
200
<Response [200]>
-------------------------
Resultado final: {'score': 850, 'status': 'APROVADO'}
```

Na interface web do Locust, gráficos de desempenho da API serão exibidos.

---

## 🛠️ Personalizações

Se precisar **ajustar os tempos de espera** entre as requisições, edite:

```python
wait_time = between(1, 3)
```

Isso define um intervalo **entre 1 e 3 segundos** para cada usuário.

Caso queira **aumentar as tentativas** na consulta de status, altere:

```python
for _ in range(10):  # Tenta 10 vezes
    time.sleep(5)  # Espera 5 segundos entre cada tentativa
```

---

## 📌 Referências

- [Documentação Oficial do Locust](https://docs.locust.io/)
- [Instalação do Python](https://www.python.org/downloads/)
- [Testes de Carga com Locust](https://medium.com/)

---

## 📝 Autor

📌 **Gabriel Martins**  
🔗 [GitHub](https://github.com/Lazy-Town)  
📧 gabriel.silvamartins@yahoo.com.br  

---

