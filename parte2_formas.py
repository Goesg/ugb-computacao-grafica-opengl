"""
Parte 2 - Desenhando as Primeiras Formas Geométricas
=====================================================
Este exemplo demonstra:
  - O conceito de vértices e primitivas geométricas
  - GL_POINTS  : renderiza vértices como pontos isolados
  - GL_LINES   : conecta pares de vértices em segmentos de reta
  - GL_TRIANGLES: agrupa vértices em triângulos preenchidos
  - glBegin() / glEnd() : delimitam o bloco de especificação de primitivas
  - glVertex2f(x, y)    : define a posição de um vértice em 2D

Sistema de coordenadas OpenGL (NDC - Normalized Device Coordinates):
  - Centro da tela : (0, 0)
  - Extremidade direita : x = +1.0
  - Extremidade esquerda: x = -1.0
  - Extremidade superior: y = +1.0
  - Extremidade inferior : y = -1.0
"""

import glfw
from OpenGL.GL import *
import sys


# ── Configuração do GLFW ─────────────────────────────────────────────────────

def criar_janela(largura, altura, titulo):
    if not glfw.init():
        print("Erro: GLFW não pôde ser inicializado.")
        sys.exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)

    janela = glfw.create_window(largura, altura, titulo, None, None)
    if not janela:
        glfw.terminate()
        print("Erro: janela não pôde ser criada.")
        sys.exit(1)

    glfw.make_context_current(janela)
    return janela


# ── Funções de desenho ────────────────────────────────────────────────────────

def desenhar_ponto():
    """
    Desenha um único ponto na parte superior da tela.

    glPointSize define o diâmetro do ponto em pixels.
    GL_POINTS instrui a GPU a renderizar cada vértice como um ponto.
    """
    glPointSize(15.0)          # tamanho do ponto em pixels
    glColor3f(1.0, 1.0, 0.0)  # amarelo (R=1, G=1, B=0)

    glBegin(GL_POINTS)         # início do bloco de primitivas do tipo PONTO
    glVertex2f(0.0, 0.75)      # vértice na posição (x=0, y=0.75)
    glEnd()                    # fim do bloco


def desenhar_linha():
    """
    Desenha um segmento de reta horizontal no meio da tela.

    GL_LINES: cada par de vértices forma um segmento independente.
    glLineWidth define a espessura da linha em pixels.
    """
    glLineWidth(3.0)           # espessura da linha em pixels
    glColor3f(0.0, 1.0, 1.0)  # ciano (R=0, G=1, B=1)

    glBegin(GL_LINES)          # início do bloco de primitivas do tipo LINHA
    glVertex2f(-0.6, 0.0)      # vértice inicial do segmento
    glVertex2f(0.6, 0.0)       # vértice final do segmento
    glEnd()


def desenhar_triangulo():
    """
    Desenha um triângulo preenchido na parte inferior da tela.

    GL_TRIANGLES: cada grupo de 3 vértices forma um triângulo preenchido.
    Os vértices devem ser fornecidos em sentido anti-horário (padrão OpenGL).
    """
    glColor3f(0.2, 0.8, 0.2)  # verde

    glBegin(GL_TRIANGLES)      # início do bloco de primitivas do tipo TRIÂNGULO
    glVertex2f(-0.5, -0.75)    # vértice inferior esquerdo
    glVertex2f(0.5, -0.75)     # vértice inferior direito
    glVertex2f(0.0, -0.20)     # vértice superior (ápice)
    glEnd()


def renderizar():
    """Chama todas as funções de desenho em sequência."""
    desenhar_ponto()
    desenhar_linha()
    desenhar_triangulo()


# ── Loop principal ────────────────────────────────────────────────────────────

def main():
    janela = criar_janela(800, 600, "Parte 2 - Ponto, Linha e Triângulo")

    print("Controles: ESC para sair.")
    print("Primitivas desenhadas:")
    print("  • GL_POINTS   → ponto amarelo no topo")
    print("  • GL_LINES    → linha ciana no centro")
    print("  • GL_TRIANGLES→ triângulo verde na base")

    while not glfw.window_should_close(janela):
        glfw.poll_events()

        if glfw.get_key(janela, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(janela, True)

        # Cor de fundo escura para contrastar com as primitivas
        glClearColor(0.10, 0.10, 0.15, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        renderizar()

        glfw.swap_buffers(janela)

    glfw.terminate()


if __name__ == "__main__":
    main()
