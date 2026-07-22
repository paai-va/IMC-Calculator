import customtkinter as ctk

from calculos import calcular_resultado
from utils import calcular_idade_em_meses, validar_data_nascimento, validar_float, validar_texto

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

CORES_POR_CLASSIFICACAO = {
    "Magreza acentuada": "#E74C3C",
    "Magreza": "#3B8ED0",
    "Abaixo do peso": "#3B8ED0",
    "Peso adequado para a idade": "#2FA572",
    "Peso normal": "#2FA572",
    "Sobrepeso": "#D9A441",
    "Obesidade": "#E74C3C",
    "Obesidade Grau I": "#E74C3C",
    "Obesidade Grau II": "#C0392B",
    "Obesidade Grau III": "#922B21",
    "Fora da faixa coberta (consulte um pediatra)": "#D9A441",
}


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora de IMC Pro")
        self.geometry("700x800")

        # A coluna 0 da janela passa a ocupar 100% da largura disponível.
        self.grid_columnconfigure(0, weight=1)

        self.tema_escuro = True
        self.botao_tema = ctk.CTkButton(
            self, text="🌙 Modo escuro", command=self._alternar_tema, width=140
        )
        self.botao_tema.place(relx=1.0, x=-20, y=16, anchor="ne")

        # Caixinha invisível que guarda todo o formulário. Como ela não usa
        # sticky="ew", o Tkinter a centraliza sozinha dentro da coluna 0.
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0, pady=(70, 20))

        self.entrada_nome = self._criar_campo("Nome", 0)
        self.entrada_nascimento = self._criar_campo("Data de nascimento (DD/MM/AAAA)", 2)
        self.entrada_nascimento.bind("<KeyRelease>", self._formatar_data_nascimento)
        self.entrada_peso = self._criar_campo("Peso (kg)", 4)
        self.entrada_altura = self._criar_campo("Altura (cm)", 6)

        label_sexo = ctk.CTkLabel(self.container, text="Sexo", anchor="w")
        label_sexo.grid(row=8, column=0, padx=20, pady=(12, 0), sticky="ew")

        self.opcao_sexo = ctk.CTkSegmentedButton(
            self.container, values=["Masculino", "Feminino"], command=self._atualizar_cor_sexo
        )
        self.opcao_sexo.set("Masculino")
        self.opcao_sexo.grid(row=9, column=0, padx=20, pady=(4, 0), sticky="ew")
        self._atualizar_cor_sexo("Masculino")

        self.botao_calcular = ctk.CTkButton(
            self.container, text="Calcular IMC", command=self.calcular,
            fg_color="#2FA572", hover_color="#268A5F"
        )
        self.botao_calcular.grid(row=10, column=0, padx=20, pady=20, sticky="ew")

        self.rotulo_erro = ctk.CTkLabel(self.container, text="", text_color="#E74C3C")
        self.rotulo_erro.grid(row=11, column=0, padx=20, pady=(0, 4), sticky="w")

        self.frame_resultado = ctk.CTkFrame(self.container)
        self.frame_resultado.grid(row=12, column=0, padx=20, pady=(4, 20), sticky="ew")

    def _criar_campo(self, rotulo, linha):
        label = ctk.CTkLabel(self.container, text=rotulo, anchor="w")
        label.grid(row=linha, column=0, padx=20, pady=(12, 0), sticky="ew")

        entrada = ctk.CTkEntry(self.container, width=360)
        entrada.grid(row=linha + 1, column=0, padx=20, pady=(4, 0), sticky="ew")

        return entrada

    def _formatar_data_nascimento(self, event=None):
        texto = self.entrada_nascimento.get()
        somente_digitos = "".join(caractere for caractere in texto if caractere.isdigit())
        somente_digitos = somente_digitos[:8]

        partes = []
        if len(somente_digitos) > 0:
            partes.append(somente_digitos[0:2])
        if len(somente_digitos) > 2:
            partes.append(somente_digitos[2:4])
        if len(somente_digitos) > 4:
            partes.append(somente_digitos[4:8])

        texto_formatado = "/".join(partes)

        self.entrada_nascimento.delete(0, "end")
        self.entrada_nascimento.insert(0, texto_formatado)

    def _atualizar_cor_sexo(self, valor_selecionado):
        if valor_selecionado == "Masculino":
            self.opcao_sexo.configure(selected_color="#3B8ED0", selected_hover_color="#2F72A8")
        else:
            self.opcao_sexo.configure(selected_color="#E91E8C", selected_hover_color="#C0176F")

    def _alternar_tema(self):
        self.tema_escuro = not self.tema_escuro

        if self.tema_escuro:
            ctk.set_appearance_mode("dark")
            self.botao_tema.configure(text="🌙 Modo escuro")
        else:
            ctk.set_appearance_mode("light")
            self.botao_tema.configure(text="☀️ Modo claro")

    def calcular(self):
        self.rotulo_erro.configure(text="")

        nome = validar_texto(self.entrada_nome.get())
        nascimento = validar_data_nascimento(self.entrada_nascimento.get())
        peso = validar_float(self.entrada_peso.get())
        altura = validar_float(self.entrada_altura.get())
        sexo = self.opcao_sexo.get()

        if nascimento is None:
            self.rotulo_erro.configure(text="Data de nascimento inválida.")
            return

        if peso is None:
            self.rotulo_erro.configure(text="Peso inválido.")
            return

        if altura is None:
            self.rotulo_erro.configure(text="Altura inválida.")
            return

        idade_meses = calcular_idade_em_meses(nascimento)

        resultado = calcular_resultado(
            peso_kg=peso, altura_cm=altura, idade_meses=idade_meses, sexo=sexo
        )

        self._exibir_resultado(nome, resultado)

    def _exibir_resultado(self, nome, resultado):
        for widget in self.frame_resultado.winfo_children():
            widget.destroy()

        cor = CORES_POR_CLASSIFICACAO.get(resultado['classificacao'], "#FFFFFF")

        ctk.CTkLabel(
            self.frame_resultado, text=f"Nome: {nome}", anchor="w"
        ).pack(fill="x", padx=12, pady=(12, 2))

        ctk.CTkLabel(
            self.frame_resultado, text=f"IMC: {resultado['imc']:.2f}",
            font=ctk.CTkFont(size=18, weight="bold"), anchor="w"
        ).pack(fill="x", padx=12, pady=2)

        ctk.CTkLabel(
            self.frame_resultado, text=f"Classificação: {resultado['classificacao']}",
            text_color=cor, font=ctk.CTkFont(weight="bold"), anchor="w"
        ).pack(fill="x", padx=12, pady=2)

        if "z_score" in resultado:
            ctk.CTkLabel(
                self.frame_resultado,
                text=f"Escore-Z (IMC-para-idade): {resultado['z_score']:.2f}",
                text_color="gray60", anchor="w"
            ).pack(fill="x", padx=12, pady=2)

        if "peso_min_saudavel" in resultado:
            ctk.CTkLabel(
                self.frame_resultado,
                text=(
                    f"Faixa de peso saudável: {resultado['peso_min_saudavel']:.1f} kg "
                    f"a {resultado['peso_max_saudavel']:.1f} kg"
                ),
                text_color="gray60", anchor="w", wraplength=380, justify="left"
            ).pack(fill="x", padx=12, pady=2)

        ctk.CTkLabel(
            self.frame_resultado, text=f"Fonte: {resultado['fonte']}",
            text_color="gray60", anchor="w", wraplength=380, justify="left"
        ).pack(fill="x", padx=12, pady=(2, 12))


def iniciar_app():
    app = App()
    app.mainloop()