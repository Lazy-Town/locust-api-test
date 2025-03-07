from locust import HttpUser, task, between
import time


class ApiUser(HttpUser):
    wait_time = between(1, 3)  # Tempo de espera entre requisições

    def on_start(self):
        """Define os headers com a chave de autenticação."""
        self.headers = {
            "Ocp-Apim-Subscription-Key": "xxxx",
            "Content-Type": "application/json"
        }

    @task
    def test_api(self):
        cpf = "03148250109"
        base_api = "xxxx" # URL de base para as consultas por link
        base_cpf = base_api+"xxxx" # Consulta por cpf
        base_stats = base_api+"xxxx" # Consulta do status do endpoint
        base_result = base_api+"xxxx" # Consutla do resultado do endpoint

        # Etapa 1: Enviar CPF e receber um ID (POST)
        response = self.client.post(base_cpf, headers=self.headers, json={"cpf": cpf})
        if response.status_code != 202:
            print(f"Erro ao enviar CPF: {response.text}")
            print(f"Esse é o status {response.status_code}")
            return

        response_data = response.json()
        request_id = response_data.get("id")
        if not request_id:
            print("Nenhum ID retornado.")
            return

        # Etapa 2: Consultar status do ID (POST)
        status_data = ""
        for _ in range(10):
            time.sleep(5)
            status_response = self.client.post(base_stats, headers=self.headers, json={"id": request_id})
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"ESSE É O STATUS DATA {status_data}")

                # Registra métricas personalizadas
                if status_data == "PENDING":
                    self.environment.events.request.fire(
                        request_type="STATUS",
                        name="PENDING",
                        response_time=0,
                        response_length=0,
                        exception=None
                    )

                if status_data == "FAILED":
                    self.environment.events.request.fire(
                        request_type="STATUS",
                        name="FAILED",
                        response_time=0,
                        response_length=0,
                        exception=None
                    )

                if status_data in ["SUCCESS", "FAILED", "PENDING"]:
                    break

            if status_data != "SUCCESS":
                print(f"Processo falhou ou ainda está pendente: {status_data}")
                return

        if status_data != "SUCCESS":
            print(f"Status não completado: {status_data}")
            return

        # Etapa 3: Consultar resultado final (POST)
        result_response = self.client.post(base_result, headers=self.headers, json={"id": request_id})
        print("-------------------------")
        print(result_response.status_code)
        print(result_response)
        print("-------------------------")
        if result_response.status_code == 200:
            print(f"Resultado final: {result_response.json()}")
        else:
            print(f"Erro ao buscar resultado final: {result_response.text}")

        # Sempre para o Locust após a execução de 1 usuário, os outros continuam sendo executados
        self.stop()
