from django.shortcuts import render
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .forms import BisseccaoForm
from.forms import NewtonForm
from.forms import FalsaPosicaoForm
from.forms import SecanteForm
import numpy as np  
import matplotlib.pyplot as plt
import io
import base64
import sympy as sp
# Create your views here.
def home(request):
    return render(request, 'home.html')

def calcular_bisseccao(funcao, intervalo_esquerda, intervalo_direita, tolerancia, iteracoes):
    a = float(intervalo_esquerda)
    b = float(intervalo_direita)

    # Lista para armazenar as interações (valores de a, b, c e f(c))
    interacoes = []
    
    # Calcula f(a) e f(b)
    f_a = eval(funcao.replace('x', f'({a})'))
    f_b = eval(funcao.replace('x', f'({b})'))

    # Verifica se os sinais de f(a) e f(b) são opostos
    if f_a * f_b > 0:
        raise ValueError(f"A função deve ter sinais opostos em a e b: f(a) = {f_a}, f(b) = {f_b} ou contém mais uma raiz para o intervalo")

    # Verifica se já existe uma raiz em a ou b
    if f_a == 0:
        return a, [(a, b, a, f_a)]  # Se f(a) é 0, a raiz é a
    if f_b == 0:
        return b, [(a, b, b, f_b)]  # Se f(b) é 0, a raiz é b
    
    # Loop para iterar até o número máximo de iterações
    for i in range(iteracoes):
        c = (a + b) / 2  # Calcula o ponto médio do intervalo
        f_c = eval(funcao.replace('x', f'({c})'))  # Calcula a função f(c)
        interacoes.append((a, b, c, f_c))  # Armazena a interação atual
        
        # Verifica se a raiz foi encontrada ou se a tolerância foi atingida
        if f_c == 0 or (b - a) / 2 < tolerancia:
            return c, interacoes  # Retorna a raiz e as interações
        
        # Atualiza os limites do intervalo baseado no sinal de f(c)
        if f_c * f_a < 0:  # A raiz está entre a e c
            b = c
            f_b = f_c  # Atualiza f(b) para o novo c
        else:  # A raiz está entre c e b
            a = c
            f_a = f_c  # Atualiza f(a) para o novo c
            
    return c, interacoes  # Retorna c como a raiz aproximada e as interações

def bisseccao(request):
    form = BisseccaoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        funcao = form.cleaned_data['funcao']
        limite_esquerdo = form.cleaned_data['limite_esquerdo']
        limite_direito = form.cleaned_data['limite_direito']
        tolerancia = form.cleaned_data['tolerancia']
        iteracoes = form.cleaned_data['iteracoes']

        raiz, interacoes = calcular_bisseccao(funcao, limite_esquerdo, limite_direito, tolerancia, iteracoes)

        # Gerar gráfico
        plt.figure()
        x = np.linspace(limite_esquerdo, limite_direito, 100)
        y = eval(funcao.replace('x', 'x'))  
        plt.plot(x, y, label='Função')
        plt.axhline(0, color='gray', lw=0.5)
        plt.axvline(raiz, color='red', linestyle='--', label='Raiz')
        plt.legend()

        # Salvar a figura em um objeto de bytes
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        imagem_base64 = base64.b64encode(buf.read()).decode('utf-8')

        return render(request, 'bisseccao.html', {
            'form': form,
            'raiz': raiz,
            'interacoes': interacoes,
            'imagem': imagem_base64,
        })

    return render(request, 'bisseccao.html', {'form': form})

def calcular_newton(funcao, derivada, valor_inicial, tolerancia, iteracoes):
    x = float(valor_inicial)
    interacoes = []

    # Cria funções a partir das strings usando eval
    f = eval("lambda x: " + funcao)  # Função original
    f_prime = eval("lambda x: " + derivada)  # Derivada da função

    # Loop para iterar até o número máximo de iterações
    for i in range(iteracoes):
        f_x = f(x)  # Avalia a função no ponto atual x
        f_prime_x = f_prime(x)  # Avalia a derivada no ponto atual x

        # Verifica se a derivada é zero para evitar divisão por zero
        if f_prime_x == 0:
            raise ValueError("A derivada não pode ser zero.")

        # Aplica a fórmula do método de Newton para encontrar o novo valor de x
        x_novo = x - f_x / f_prime_x
        expressao = f"x = {x} - ({f_x}/{f_prime_x})"  # Monta a expressão para a interação
        interacoes.append((x, f_x, f_prime_x, expressao))  # Armazena a interação atual

        # Verifica se a diferença entre o novo x e o anterior está dentro da tolerância
        if abs(x_novo - x) < tolerancia:
            return x_novo, interacoes  # Retorna a raiz encontrada e as interações

        x = x_novo  # Atualiza x para o próximo loop

    return x, interacoes  # Retorna o valor final de x e as interações

def newton(request):
    form = NewtonForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        funcao = form.cleaned_data['funcao']
        derivada = form.cleaned_data['derivada']
        valor_inicial = form.cleaned_data['valor_inicial']
        tolerancia = form.cleaned_data['tolerancia']
        iteracoes = form.cleaned_data['iteracoes']

        raiz, interacoes = calcular_newton(funcao, derivada, valor_inicial, tolerancia, iteracoes)

        # Gerar gráfico
        plt.figure()
        x = np.linspace(valor_inicial - 10, valor_inicial + 10, 100)  # Ajuste a faixa conforme necessário
        y = eval(funcao.replace('x', 'x'))
        plt.plot(x, y, label='Função')
        plt.axhline(0, color='gray', lw=0.5)
        plt.axvline(raiz, color='red', linestyle='--', label='Raiz')
        plt.legend()

        # Salvar a figura em um objeto de bytes
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        imagem_base64 = base64.b64encode(buf.read()).decode('utf-8')

        return render(request, 'newton.html', {
            'form': form,
            'raiz': raiz,
            'interacoes': interacoes,
            'imagem': imagem_base64,
        })

    return render(request, 'newton.html', {'form': form})

def metodo_falsa_posicao(funcao, a, b, tolerancia, max_iteracoes):
    # Inicializa uma lista para armazenar as iterações
    iteracoes = []
    # Loop para executar o algoritmo até o número máximo de iterações
    for i in range(max_iteracoes):
        # Avalia a função nos pontos a e b
        f_a = eval(funcao.replace('x', str(a)))
        f_b = eval(funcao.replace('x', str(b)))

        # Calcula o ponto c usando a fórmula da falsa posição
        c = (a * f_b - b * f_a) / (f_b - f_a)
        # Avalia a função no ponto c
        f_c = eval(funcao.replace('x', str(c)))

        # Adiciona os valores da iteração à lista
        iteracoes.append((i, a, b, c, f_c))

        # Se o valor absoluto de f(c) for menor que a tolerância, a raiz foi encontrada
        if abs(f_c) < tolerancia:
            return c, iteracoes  # Retorna a raiz e as iterações

        # Se f(a) e f(c) tiverem sinais opostos, a raiz está entre a e c
        if f_a * f_c < 0:
            b = c  # Atualiza b para c
        else:
            a = c  # Atualiza a para c
    return None, iteracoes  # Retorna None se a raiz não foi encontrada e as iterações

def falsaposicao(request):
    resultado = None  # Inicializa a variável de resultado
    grafico = None  # Inicializa a variável do gráfico
    iteracoes = []  # Inicializa a lista de iterações

    # Verifica se a requisição é um POST
    if request.method == 'POST':
        form = FalsaPosicaoForm(request.POST)  # Cria o formulário com os dados do POST
        if form.is_valid():  # Verifica se o formulário é válido
            funcao = form.cleaned_data['funcao']  # Obtém a função do formulário
            intervalo_inferior = form.cleaned_data['intervalo_inferior']  # Obtém o intervalo inferior
            intervalo_superior = form.cleaned_data['intervalo_superior']  # Obtém o intervalo superior
            tolerancia = form.cleaned_data['tolerancia']  # Obtém a tolerância
            max_iteracoes = form.cleaned_data['max_iteracoes']  # Obtém o número máximo de iterações

            try:
                # Chama o método da falsa posição
                resultado, iteracoes = metodo_falsa_posicao(funcao, intervalo_inferior, intervalo_superior, tolerancia, max_iteracoes)

                # Gera o gráfico da função
                x = np.linspace(intervalo_inferior, intervalo_superior, 100)  # Gera 100 pontos no intervalo
                y = [eval(funcao.replace('x', str(val))) for val in x]  # Avalia a função em cada ponto
                plt.figure()  # Cria uma nova figura
                plt.plot(x, y)  # Plota a função
                plt.axhline(0, color='black', lw=0.5, ls='--')  # Adiciona uma linha horizontal em y=0
                plt.title('Gráfico da Função')  # Define o título do gráfico
                plt.xlabel('x')  # Rotula o eixo x
                plt.ylabel('f(x)')  # Rotula o eixo y
                buf = io.BytesIO()  # Cria um buffer em memória
                plt.savefig(buf, format='png')  # Salva o gráfico no buffer em formato PNG
                plt.close()  # Fecha a figura para liberar memória
                buf.seek(0)  # Move o cursor para o início do buffer
                grafico = base64.b64encode(buf.read()).decode('utf-8')  # Codifica o gráfico em base64

            except Exception as e:
                resultado = f"Erro na avaliação da função: {str(e)}"  # Captura erros na avaliação da função

    else:
        form = FalsaPosicaoForm()  # Cria um novo formulário se não for um POST

    # Renderiza o template com os resultados
    return render(request, 'falsaposicao.html', {'form': form, 'resultado': resultado, 'grafico': grafico, 'iteracoes': iteracoes})

def secante(request): 
    resultado = None  # Inicializa a variável de resultado
    grafico = None  # Inicializa a variável do gráfico
    iteracoes = []  # Inicializa a lista de iterações

    # Verifica se a requisição é um POST
    if request.method == 'POST':
        form = SecanteForm(request.POST)  # Cria o formulário com os dados do POST
        if form.is_valid():  # Verifica se o formulário é válido
            funcao = form.cleaned_data['funcao']  # Obtém a função do formulário
            x0 = form.cleaned_data['x0']  # Obtém o primeiro ponto inicial
            x1 = form.cleaned_data['x1']  # Obtém o segundo ponto inicial
            tolerancia = form.cleaned_data['tolerancia']  # Obtém a tolerância
            max_iteracoes = form.cleaned_data['max_iteracoes']  # Obtém o número máximo de iterações

            try:
                # Chama o método da secante
                resultado, iteracoes = metodo_secante(funcao, x0, x1, tolerancia, max_iteracoes)

                # Gera o gráfico da função
                if resultado is not None:  # Verifica se a raiz foi encontrada
                    x_vals = np.linspace(x0 - 1, x1 + 1, 100)  # Gera 100 pontos ao redor dos pontos iniciais
                    y_vals = []

                    for val in x_vals:
                        try:
                            # Avalia a função em cada ponto
                            y_vals.append(eval(funcao, {"_builtins_": None}, {"x": val}))
                        except Exception:
                            y_vals.append(float('nan'))  # Adiciona NaN se houver erro na avaliação

                    plt.figure()  # Cria uma nova figura
                    plt.plot(x_vals, y_vals, label='f(x)')  # Plota a função
                    plt.axhline(0, color='black', lw=0.5, ls='--')  # Adiciona uma linha horizontal em y=0
                    plt.title('Gráfico da Função')  # Define o título do gráfico
                    plt.xlabel('x')  # Rotula o eixo x
                    plt.ylabel('f(x)')  # Rotula o eixo y
                    plt.legend()  # Adiciona uma legenda
                    buf = io.BytesIO()  # Cria um buffer em memória
                    plt.savefig(buf, format='png')  # Salva o gráfico no buffer em formato PNG
                    plt.close()  # Fecha a figura para liberar memória
                    buf.seek(0)  # Move o cursor para o início do buffer
                    grafico = base64.b64encode(buf.read()).decode('utf-8')  # Codifica o gráfico em base64

            except Exception as e:
                resultado = f"Erro na avaliação da função: {str(e)}"  # Captura erros na avaliação da função

    else:
        form = SecanteForm()  # Cria um novo formulário se não for um POST

    # Renderiza o template com os resultados
    return render(request, 'secante.html', {'form': form, 'resultado': resultado, 'grafico': grafico, 'iteracoes': iteracoes})

def metodo_secante(funcao, x0, x1, tolerancia, max_iteracoes):
    # Inicializa uma lista para armazenar as iterações
    iteracoes = []
    
    # Loop para executar o algoritmo até o número máximo de iterações
    for i in range(max_iteracoes):
        # Avalia a função nos pontos x0 e x1
        f_x0 = eval(funcao, {"_builtins_": None}, {"x": x0})
        f_x1 = eval(funcao, {"_builtins_": None}, {"x": x1})

        # Verifica se a diferença entre os valores é zero para evitar divisão por zero
        if f_x1 - f_x0 == 0:
            return None, iteracoes  # Retorna None se não for possível calcular

        # Calcula o novo ponto x2 usando a fórmula da secante
        x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
        f_x2 = eval(funcao, {"_builtins_": None}, {"x": x2})  # Avalia a função em x2

        # Adiciona os valores da iteração à lista
        iteracoes.append((i, x0, x1, x2, f_x2))

        # Se a diferença entre x2 e x1 for menor que a tolerância ou f(x2) for próximo de zero, a raiz foi encontrada
        if abs(x2 - x1) < tolerancia or abs(f_x2) < tolerancia:
            return x2, iteracoes  # Retorna a raiz e as iterações
        
        # Atualiza os pontos para a próxima iteração
        x0, x1 = x1, x2

    return None, iteracoes  # Retorna None se a raiz não foi encontrada e as iterações
