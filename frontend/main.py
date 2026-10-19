import tkinter as tk
import requests


def abrir_laboratorios():
    tela = tk.Toplevel(janela)
    tela.title("Laboratórios")
    tela.geometry("700x500")

    titulo = tk.Label(
        tela,
        text="Laboratórios",
        font=("Arial", 18)
    )
    titulo.pack(pady=20)

    lista = tk.Listbox(
        tela,
        width=80,
        height=15
    )
    lista.pack(pady=20)

    resposta = requests.get(
        "http://127.0.0.1:8000/laboratorios/"
    )

    laboratorios = resposta.json()

    for laboratorio in laboratorios:
        lista.insert(
            tk.END,
            f"{laboratorio['idLaboratorio']} - "
            f"{laboratorio['nome']} - "
            f"{laboratorio['localizacao']} - "
            f"Capacidade: {laboratorio['capacidade']}"
        )


def abrir_disponibilidade():
    tela = tk.Toplevel(janela)
    tela.title("Consultar Disponibilidade")
    tela.geometry("600x500")

    titulo = tk.Label(
        tela,
        text="Consultar Disponibilidade",
        font=("Arial", 18)
    )
    titulo.pack(pady=20)

    tk.Label(
        tela,
        text="Data:"
    ).pack()

    campo_data = tk.Entry(tela)
    campo_data.pack(pady=5)

    tk.Label(
        tela,
        text="Hora início:"
    ).pack()

    campo_inicio = tk.Entry(tela)
    campo_inicio.pack(pady=5)

    tk.Label(
        tela,
        text="Hora fim:"
    ).pack()

    campo_fim = tk.Entry(tela)
    campo_fim.pack(pady=5)

    resultado = tk.Text(
        tela,
        width=60,
        height=10
    )
    resultado.pack(pady=15)

    def consultar():
        dados = {
            "data": campo_data.get(),
            "horaInicio": campo_inicio.get(),
            "horaFim": campo_fim.get()
        }

        resposta = requests.post(
            "http://127.0.0.1:8000/disponibilidade/",
            json=dados
        )

        resultado.delete("1.0", tk.END)

        if resposta.status_code == 200:
            dados_resposta = resposta.json()

            for laboratorio in dados_resposta["laboratoriosDisponiveis"]:
                resultado.insert(
                    tk.END,
                    f"ID: {laboratorio['idLaboratorio']}\n"
                    f"Nome: {laboratorio['nome']}\n"
                    f"Localização: {laboratorio['localizacao']}\n"
                    f"Capacidade: {laboratorio['capacidade']}\n"
                    f"Status: {laboratorio['status']}\n"
                    f"--------------------------\n"
                )
        else:
            resultado.insert(
                tk.END,
                resposta.json()["detail"]
            )

    botao_consultar = tk.Button(
        tela,
        text="Consultar",
        command=consultar
    )
    botao_consultar.pack(pady=5)

def consultar():
    dados = {
        "data": campo_data.get(),
        "horaInicio": campo_inicio.get(),
        "horaFim": campo_fim.get()
    }

    resposta = requests.post(
        "http://127.0.0.1:8000/disponibilidade/",
        json=dados
    )

    resultado.delete("1.0", tk.END)

    if resposta.status_code == 200:
        dados_resposta = resposta.json()

        for laboratorio in dados_resposta["laboratoriosDisponiveis"]:
            resultado.insert(
                tk.END,
                f"ID: {laboratorio['idLaboratorio']}\n"
                f"Nome: {laboratorio['nome']}\n"
                f"Localização: {laboratorio['localizacao']}\n"
                f"Capacidade: {laboratorio['capacidade']}\n"
                f"Status: {laboratorio['status']}\n"
                f"--------------------------\n"
            )
    else:
        resultado.insert(
            tk.END,
            resposta.json()["detail"]
        )

def abrir_reservas():
    tela = tk.Toplevel(janela)
    tela.title("Reservas")
    tela.geometry("600x550")

    titulo = tk.Label(
        tela,
        text="Reservas",
        font=("Arial", 18)
    )
    titulo.pack(pady=20)

    tk.Label(
        tela,
        text="Data:"
    ).pack()

    campo_data = tk.Entry(tela)
    campo_data.pack(pady=5)

    tk.Label(
        tela,
        text="Hora início:"
    ).pack()

    campo_inicio = tk.Entry(tela)
    campo_inicio.pack(pady=5)

    tk.Label(
        tela,
        text="Hora fim:"
    ).pack()

    campo_fim = tk.Entry(tela)
    campo_fim.pack(pady=5)

    tk.Label(
        tela,
        text="ID do usuário:"
    ).pack()

    campo_usuario = tk.Entry(tela)
    campo_usuario.pack(pady=5)

    tk.Label(
        tela,
        text="ID do laboratório:"
    ).pack()

    campo_laboratorio = tk.Entry(tela)
    campo_laboratorio.pack(pady=5)

    resultado = tk.Text(
        tela,
        width=60,
        height=8
    )
    resultado.pack(pady=15)

    def realizar_reserva():
        dados = {
            "data": campo_data.get(),
            "horaInicio": campo_inicio.get(),
            "horaFim": campo_fim.get(),
            "idUsuario": int(campo_usuario.get()),
            "idLaboratorio": int(campo_laboratorio.get())
        }

        resposta = requests.post(
            "http://127.0.0.1:8000/reservas/",
            json=dados
        )

        resultado.delete("1.0", tk.END)

        if resposta.status_code == 201:
            resultado.insert(
                tk.END,
                "Reserva realizada com sucesso!\n\n"
            )
            resultado.insert(
                tk.END,
                str(resposta.json())
            )
        else:
            resultado.insert(
                tk.END,
                str(resposta.json())
            )

    botao_reservar = tk.Button(
        tela,
        text="Realizar Reserva",
        command=realizar_reserva
    )
    botao_reservar.pack(pady=5)
    botao_gerenciar = tk.Button(
        tela,
        text="Gerenciar Reservas",
        command=abrir_gerenciar_reservas
    )
    botao_gerenciar.pack(pady=5)



def realizar_reserva():
    dados = {
        "data": campo_data.get(),
        "horaInicio": campo_inicio.get(),
        "horaFim": campo_fim.get(),
        "idUsuario": int(campo_usuario.get()),
        "idLaboratorio": int(campo_laboratorio.get())
    }

    resposta = requests.post(
        "http://127.0.0.1:8000/reservas/",
        json=dados
    )

    resultado.delete("1.0", tk.END)

    if resposta.status_code == 201:
        resultado.insert(
            tk.END,
            "Reserva realizada com sucesso!\n\n"
        )
        resultado.insert(
            tk.END,
            str(resposta.json())
        )
    else:
        resultado.insert(
            tk.END,
            str(resposta.json())
        )

def abrir_gerenciar_reservas():
    tela = tk.Toplevel(janela)
    tela.title("Gerenciar Reservas")
    tela.geometry("700x550")

    titulo = tk.Label(
        tela,
        text="Gerenciar Reservas",
        font=("Arial", 18)
    )
    titulo.pack(pady=20)

    tk.Label(
        tela,
        text="ID da reserva:"
    ).pack()

    campo_id = tk.Entry(tela)
    campo_id.pack(pady=5)

    botao_consultar = tk.Button(
        tela,
        text="Consultar"
    )
    botao_consultar.pack(pady=5)

    botao_cancelar = tk.Button(
        tela,
        text="Cancelar"
    )
    botao_cancelar.pack(pady=5)

    resultado = tk.Text(
        tela,
        width=75,
        height=15
    )
    resultado.pack(pady=15)

    def listar_reservas():
        resposta = requests.get(
            "http://127.0.0.1:8000/gerenciar-reservas/"
        )

        resultado.delete("1.0", tk.END)

        if resposta.status_code == 200:
            reservas = resposta.json()

            for reserva in reservas:
                resultado.insert(
                    tk.END,
                    f"ID: {reserva['idReserva']}\n"
                    f"Data: {reserva['data']}\n"
                    f"Hora início: {reserva['horaInicio']}\n"
                    f"Hora fim: {reserva['horaFim']}\n"
                    f"Laboratório: {reserva['idLaboratorio']}\n"
                    f"Usuário: {reserva['idUsuario']}\n"
                    f"Status: {reserva['status']}\n"
                    f"--------------------------\n"
                )
        else:
            resultado.insert(
                tk.END,
                str(resposta.json())
            )

    botao_listar = tk.Button(
        tela,
        text="Listar Reservas",
        command=listar_reservas
    )
    botao_listar.pack(pady=10)

    def listar_reservas():
        resposta = requests.get(
            "http://127.0.0.1:8000/gerenciar-reservas/"
        )

        resultado.delete("1.0", tk.END)

        if resposta.status_code == 200:
            reservas = resposta.json()

            for reserva in reservas:
                resultado.insert(
                    tk.END,
                    f"ID: {reserva['idReserva']}\n"
                    f"Data: {reserva['data']}\n"
                    f"Hora início: {reserva['horaInicio']}\n"
                    f"Hora fim: {reserva['horaFim']}\n"
                    f"Laboratório: {reserva['idLaboratorio']}\n"
                    f"Usuário: {reserva['idUsuario']}\n"
                    f"Status: {reserva['status']}\n"
                    f"--------------------------\n"
                )
        else:
            resultado.insert(
                tk.END,
                str(resposta.json())
            )

janela = tk.Tk()

janela.title("Sistema de Gerenciamento de Laboratórios")
janela.geometry("900x600")
janela.configure(bg="BLUE")


faixa_topo = tk.Frame(
    janela,
    bg="#d0d0d0",
    height=90
)

faixa_topo.pack(fill="x")


titulo = tk.Label(
    faixa_topo,
    text="Sistema de Gerenciamento de Laboratórios",
    font=("Arial", 20),
    bg="#d0d0d0"
)

titulo.pack(pady=25)


botao_laboratorios = tk.Button(
    janela,
    text="Laboratórios",
    command=abrir_laboratorios,
    bg="#ffffff"
)

botao_laboratorios.pack(pady=10)


botao_disponibilidade = tk.Button(
    janela,
    text="Disponibilidade",
    command=abrir_disponibilidade,
    bg="#ffffff"
)

botao_disponibilidade.pack(pady=10)


botao_reservas = tk.Button(
    janela,
    text="Reservas",
    command=abrir_reservas,
    bg="#ffffff"
)

botao_reservas.pack(pady=10)


janela.mainloop()