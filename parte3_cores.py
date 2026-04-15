"""
Parte 3 - Cores no OpenGL
==========================
Este exemplo demonstra:
  - Sistema de cores RGB e RGBA no OpenGL
  - glColor3f(r, g, b)       : define cor sem transparência
  - glColor4f(r, g, b, a)    : define cor com canal alfa (transparência)
  - Aplicação de cores distintas em diferentes primitivas
  - Cores por vértice (interpolação de cor — Gouraud shading)

Sistema de cores RGBA:
  - Cada componente varia de 0.0 (ausente) a 1.0 (máximo)
  - R = vermelho (Red)
  - G = verde   (Green)
  - B = azul    (Blue)
  - A = alfa    (transparência: 0.0 = transparente, 1.0 = opaco)

A cor definida por glColor*() permanece ativa até ser trocada.
Quando vértices diferentes de uma mesma primitiva têm cores diferentes,
o OpenGL interpola as cores entre eles (efeito gradiente).
"""

import glfw
from OpenGL.GL import *
import sys


def criar_janela(largura, altura, titulo):
    if not glfw.init():
        sys.exit(1)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    janela = glfw.create_window(largura, altura, titulo, None, None)
    if not janela:
        glfw.terminate()
        sys.exit(1)
    glfw.make_context_current(janela)
    return janela


# ── Primitivas coloridas ──────────────────────────────────────────────────────

def desenhar_pontos_coloridos():
    """
    Desenha três pontos com cores distintas usando glColor3f().
    Cada chamada a glColor3f() antes de glVertex2f() define a cor daquele vértice.
    """
    glPointSize(20.0)

    glBegin(GL_POINTS)

    glColor3f(1.0, 0.0, 0.0)   # vermelho puro
    glVertex2f(-0.7, 0.75)

    glColor3f(0.0, 1.0, 0.0)   # verde puro
    glVertex2f(0.0, 0.75)

    glColor3f(0.0, 0.0, 1.0)   # azul puro
    glVertex2f(0.7, 0.75)

    glEnd()


def desenhar_linhas_coloridas():
    """
    Desenha três segmentos de reta, cada um com uma cor diferente.
    """
    glLineWidth(4.0)

    # Linha vermelha
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-0.8, 0.35)
    glVertex2f(-0.1, 0.35)
    glEnd()

    # Linha verde
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(-0.1, 0.35)
    glVertex2f(0.4, 0.35)
    glEnd()

    # Linha azul
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0.4, 0.35)
    glVertex2f(0.8, 0.35)
    glEnd()


def desenhar_triangulo_cor_solida():
    """
    Triângulo com cor única (laranja). Demonstra glColor3f() antes do glBegin().
    A mesma cor é aplicada a todos os vértices.
    """
    glColor3f(1.0, 0.5, 0.0)   # laranja

    glBegin(GL_TRIANGLES)
    glVertex2f(-0.75, -0.10)
    glVertex2f(-0.25, -0.10)
    glVertex2f(-0.50, 0.30)
    glEnd()


def desenhar_triangulo_multicolor():
    """
    Triângulo com uma cor diferente por vértice.
    O OpenGL interpola as cores entre os vértices (Gouraud shading),
    criando um gradiente suave dentro da primitiva.
    """
    glBegin(GL_TRIANGLES)

    glColor3f(1.0, 0.0, 0.0)   # vermelho — vértice inferior esquerdo
    glVertex2f(0.10, -0.10)

    glColor3f(0.0, 1.0, 0.0)   # verde    — vértice inferior direito
    glVertex2f(0.60, -0.10)

    glColor3f(0.0, 0.0, 1.0)   # azul     — vértice superior
    glVertex2f(0.35, 0.30)

    glEnd()


def desenhar_triangulo_rgba():
    """
    Demonstra glColor4f() com canal alfa.
    Habilita o blending para que a transparência seja efetiva.

    O blending permite misturar a cor do fragmento com o que já está no buffer,
    criando o efeito de transparência.
    """
    # Habilita o teste de blending (mistura de cores)
    glEnable(GL_BLEND)
    # Define a equação de blending: cor_final = src_alpha * src + (1-src_alpha) * dst
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glBegin(GL_TRIANGLES)

    # glColor4f(r, g, b, alpha) — alpha=0.5 = 50% transparente
    glColor4f(0.8, 0.0, 0.8, 0.55)   # magenta semitransparente
    glVertex2f(-0.55, -0.75)

    glColor4f(0.8, 0.0, 0.8, 0.55)
    glVertex2f(0.55, -0.75)

    glColor4f(1.0, 1.0, 1.0, 0.9)    # branco quase opaco no topo
    glVertex2f(0.0, -0.20)

    glEnd()

    glDisable(GL_BLEND)


def renderizar():
    desenhar_pontos_coloridos()
    desenhar_linhas_coloridas()
    desenhar_triangulo_cor_solida()
    desenhar_triangulo_multicolor()
    desenhar_triangulo_rgba()


# ── Loop principal ────────────────────────────────────────────────────────────

def main():
    janela = criar_janela(800, 600, "Parte 3 - Cores no OpenGL (RGBA)")

    print("Controles: ESC para sair.")
    print("Demonstração:")
    print("  • 3 pontos com glColor3f() — vermelho, verde, azul")
    print("  • 3 segmentos com cores distintas")
    print("  • Triângulo laranja (cor sólida)")
    print("  • Triângulo multicolor (interpolação de cor por vértice)")
    print("  • Triângulo com glColor4f() — canal alfa / transparência")

    while not glfw.window_should_close(janela):
        glfw.poll_events()

        if glfw.get_key(janela, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(janela, True)

        glClearColor(0.10, 0.10, 0.15, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        renderizar()

        glfw.swap_buffers(janela)

    glfw.terminate()


if __name__ == "__main__":
    main()
