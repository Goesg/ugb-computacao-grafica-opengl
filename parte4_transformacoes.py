"""
Parte 4 - Transformações Geométricas
=====================================
Este exemplo demonstra:
  - glMatrixMode(GL_MODELVIEW) : seleciona a matriz de modelo-visão
  - glLoadIdentity()            : reseta a matriz para identidade (sem transformação)
  - glTranslatef(tx, ty, tz)   : move o objeto no espaço (translação)
  - glRotatef(angulo, x, y, z) : gira o objeto em torno de um eixo (rotação)
  - glScalef(sx, sy, sz)       : dimensiona o objeto (escala)
  - glPushMatrix() / glPopMatrix(): salva e restaura o estado da matriz

Pipeline de transformação (Model-View):
  A GPU multiplica cada vértice pela matriz atual antes de renderizá-lo.
  A ordem das transformações importa: elas são aplicadas na ordem inversa
  ao código — a última função chamada é a primeira a ser executada no vértice.

Teclas interativas:
  1 — apenas translação
  2 — apenas rotação (animada)
  3 — apenas escala
  4 — as três simultaneamente (padrão ao abrir)
  ESC — sair
"""

import glfw
from OpenGL.GL import *
import sys
import math
import time


# ── Estado global da aplicação ────────────────────────────────────────────────

modo_atual = 4          # modo de exibição selecionado pelo usuário
angulo = 0.0            # ângulo de rotação acumulado (graus)
ultimo_tempo = 0.0      # momento da última atualização (para animação)


# ── Utilidades ────────────────────────────────────────────────────────────────

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


def callback_teclado(janela, tecla, scancode, acao, mods):
    """Callback chamado pelo GLFW a cada evento de teclado."""
    global modo_atual
    if acao == glfw.PRESS:
        if tecla == glfw.KEY_1:
            modo_atual = 1
            print("Modo: Translação")
        elif tecla == glfw.KEY_2:
            modo_atual = 2
            print("Modo: Rotação")
        elif tecla == glfw.KEY_3:
            modo_atual = 3
            print("Modo: Escala")
        elif tecla == glfw.KEY_4:
            modo_atual = 4
            print("Modo: Todas as transformações")
        elif tecla == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(janela, True)


# ── Desenho do triângulo base ─────────────────────────────────────────────────

def desenhar_triangulo_base(r, g, b):
    """
    Desenha um triângulo simples centrado na origem com a cor especificada.
    As transformações são aplicadas pela matriz atual ANTES deste desenho.
    """
    glColor3f(r, g, b)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0,  0.3)    # vértice superior
    glVertex2f(-0.25, -0.2)  # vértice inferior esquerdo
    glVertex2f(0.25, -0.2)   # vértice inferior direito
    glEnd()


def desenhar_triangulo_referencia():
    """Triângulo cinza de referência sem transformações aplicadas."""
    glColor3f(0.4, 0.4, 0.4)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0,  0.3)
    glVertex2f(-0.25, -0.2)
    glVertex2f(0.25, -0.2)
    glEnd()


# ── Modos de transformação ────────────────────────────────────────────────────

def modo_translacao():
    """
    TRANSLAÇÃO: desloca o objeto para uma nova posição.

    glTranslatef(tx, ty, tz) multiplica a matriz atual por uma
    matriz de translação. O objeto é movido (tx, ty, tz) unidades
    em cada eixo a partir de sua posição atual.
    """
    # Referência (sem transformação) — cinza
    glPushMatrix()          # salva o estado atual da matriz
    glLoadIdentity()        # reseta para identidade
    desenhar_triangulo_referencia()
    glPopMatrix()           # restaura o estado salvo

    # Triângulo transladado para a direita — verde
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(0.55, 0.0, 0.0)    # move +0.55 no eixo X
    desenhar_triangulo_base(0.2, 0.9, 0.3)
    glPopMatrix()

    # Triângulo transladado para cima — ciano
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(0.0, 0.55, 0.0)    # move +0.55 no eixo Y
    desenhar_triangulo_base(0.2, 0.9, 0.9)
    glPopMatrix()

    # Triângulo transladado diagonalmente — laranja
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(-0.55, -0.50, 0.0) # move nas direções negativas
    desenhar_triangulo_base(1.0, 0.55, 0.1)
    glPopMatrix()


def modo_rotacao(ang):
    """
    ROTAÇÃO: gira o objeto em torno de um eixo.

    glRotatef(angulo, x, y, z):
      - angulo : graus de rotação (sentido anti-horário positivo)
      - (x,y,z): vetor que define o eixo de rotação
      Para rotação 2D usamos o eixo Z: (0, 0, 1)

    ATENÇÃO: a rotação é em torno da ORIGEM. Para girar em torno do
    próprio centro do objeto, translada-se para a origem, rotaciona e
    translada de volta.
    """
    # Referência — cinza
    glPushMatrix()
    glLoadIdentity()
    desenhar_triangulo_referencia()
    glPopMatrix()

    # Rotação em torno do eixo Z (perpendicular à tela) — vermelho
    glPushMatrix()
    glLoadIdentity()
    glRotatef(ang, 0.0, 0.0, 1.0)  # gira 'ang' graus no eixo Z
    desenhar_triangulo_base(0.9, 0.2, 0.2)
    glPopMatrix()


def modo_escala():
    """
    ESCALA: dimensiona o objeto em torno da origem.

    glScalef(sx, sy, sz):
      - sx, sy, sz: fatores de escala em cada eixo
      - sx=sy=sz=1.0 → sem alteração (identidade)
      - sx=sy=sz=2.0 → dobra o tamanho
      - sx=0.5       → metade na horizontal
      - sx=-1.0      → espelha horizontalmente
    """
    # Referência — cinza
    glPushMatrix()
    glLoadIdentity()
    desenhar_triangulo_referencia()
    glPopMatrix()

    # Escala uniforme (maior) — azul
    glPushMatrix()
    glLoadIdentity()
    glScalef(2.0, 2.0, 1.0)         # dobra em X e Y
    desenhar_triangulo_base(0.3, 0.5, 1.0)
    glPopMatrix()

    # Escala não-uniforme (achatado horizontalmente) — magenta
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(0.0, -0.55, 0.0)   # desloca para não sobrepor
    glScalef(2.5, 0.5, 1.0)         # alarga em X, achata em Y
    desenhar_triangulo_base(0.9, 0.2, 0.8)
    glPopMatrix()


def modo_todas(ang):
    """
    TODAS AS TRANSFORMAÇÕES combinadas.

    Demonstra a ordem de aplicação:
      O OpenGL aplica as transformações de baixo para cima no código.
      Ou seja, a última glTranslatef/glRotatef/glScalef chamada é
      a primeira a ser efetivamente aplicada ao vértice.

    Aqui: primeiro escala, depois rotaciona, depois translada.
    """
    # Referência — cinza
    glPushMatrix()
    glLoadIdentity()
    desenhar_triangulo_referencia()
    glPopMatrix()

    # Apenas translação — verde
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(0.6, 0.0, 0.0)
    desenhar_triangulo_base(0.2, 0.9, 0.3)
    glPopMatrix()

    # Apenas rotação animada — vermelho
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(-0.6, 0.0, 0.0)
    glRotatef(ang, 0.0, 0.0, 1.0)
    desenhar_triangulo_base(0.9, 0.2, 0.2)
    glPopMatrix()

    # Apenas escala — azul
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(0.0, -0.55, 0.0)
    glScalef(1.5, 1.5, 1.0)
    desenhar_triangulo_base(0.3, 0.5, 1.0)
    glPopMatrix()

    # Translação + Rotação + Escala — amarelo
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(0.0, 0.55, 0.0)    # 3º aplicado: move para cima
    glRotatef(ang * 0.5, 0.0, 0.0, 1.0)  # 2º: rotaciona
    glScalef(0.8, 0.8, 1.0)         # 1º aplicado: reduz
    desenhar_triangulo_base(1.0, 1.0, 0.0)
    glPopMatrix()


# ── Loop principal ────────────────────────────────────────────────────────────

def main():
    global angulo, ultimo_tempo, modo_atual

    janela = criar_janela(800, 600, "Parte 4 - Transformações Geométricas")
    glfw.set_key_callback(janela, callback_teclado)

    ultimo_tempo = glfw.get_time()

    print("Controles:")
    print("  1 — Translação")
    print("  2 — Rotação (animada)")
    print("  3 — Escala")
    print("  4 — Todas (padrão)")
    print("  ESC — sair")

    # Seleciona e configura a matriz de modelo-visão
    glMatrixMode(GL_MODELVIEW)

    while not glfw.window_should_close(janela):
        glfw.poll_events()

        # ── Atualiza animação ──────────────────────────────────────────────
        tempo_atual = glfw.get_time()
        delta = tempo_atual - ultimo_tempo
        ultimo_tempo = tempo_atual

        # Velocidade: 60 graus por segundo
        angulo = (angulo + 60.0 * delta) % 360.0

        # ── Renderização ───────────────────────────────────────────────────
        glClearColor(0.10, 0.10, 0.15, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        if modo_atual == 1:
            modo_translacao()
        elif modo_atual == 2:
            modo_rotacao(angulo)
        elif modo_atual == 3:
            modo_escala()
        else:
            modo_todas(angulo)

        glfw.swap_buffers(janela)

    glfw.terminate()


if __name__ == "__main__":
    main()
