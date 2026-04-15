"""
Parte 1 - Introdução ao OpenGL e Configuração do Ambiente
==========================================================
Este exemplo demonstra:
  - O que é o OpenGL e como funciona como API gráfica
  - Configuração básica do ambiente com GLFW
  - Criação de uma janela simples com fundo colorido

Dependências:
    pip install PyOpenGL PyOpenGL_accelerate glfw

OpenGL (Open Graphics Library) é uma API multiplataforma para renderização
de gráficos 2D e 3D. Ela define um conjunto de funções que a GPU executa,
abstraindo o hardware e permitindo código portável entre sistemas operacionais.

GLFW é uma biblioteca auxiliar que cuida de:
  - Criação e gerenciamento de janelas
  - Contexto OpenGL
  - Captura de eventos de teclado e mouse
"""

import glfw
from OpenGL.GL import *
import sys


def inicializar_glfw():
    """Inicializa a biblioteca GLFW. Encerra o programa se falhar."""
    if not glfw.init():
        print("Erro: GLFW não pôde ser inicializado.")
        sys.exit(1)


def criar_janela(largura, altura, titulo):
    """
    Cria uma janela GLFW e ativa o contexto OpenGL.

    Parâmetros:
        largura  -- largura da janela em pixels
        altura   -- altura da janela em pixels
        titulo   -- título exibido na barra da janela

    Retorna:
        O objeto janela criado pelo GLFW.
    """
    # Solicita OpenGL 2.1 (suporta pipeline de função fixa: glBegin/glEnd, etc.)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)

    janela = glfw.create_window(largura, altura, titulo, None, None)
    if not janela:
        glfw.terminate()
        print("Erro: janela GLFW não pôde ser criada.")
        sys.exit(1)

    # Torna o contexto OpenGL desta janela o contexto atual da thread
    glfw.make_context_current(janela)
    return janela


def configurar_viewport(janela):
    """Ajusta o viewport OpenGL sempre que a janela for redimensionada."""
    largura, altura = glfw.get_framebuffer_size(janela)
    glViewport(0, 0, largura, altura)


def loop_principal(janela):
    """
    Loop de renderização principal (render loop).

    A cada iteração:
      1. Limpa o buffer de cor com a cor de fundo definida.
      2. Envia o buffer renderizado para a tela (swap de buffers duplos).
      3. Processa eventos pendentes (teclado, mouse, redimensionamento).
    """
    print("Janela OpenGL criada com sucesso!")
    print("Versão OpenGL:", glGetString(GL_VERSION).decode())
    print("Pressione ESC ou feche a janela para sair.")

    while not glfw.window_should_close(janela):
        # ── Processa eventos de entrada ───────────────────────────────────
        glfw.poll_events()

        # Fecha ao pressionar ESC
        if glfw.get_key(janela, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(janela, True)

        # ── Renderização ──────────────────────────────────────────────────
        # Define a cor de fundo (R, G, B, A) — valores de 0.0 a 1.0
        glClearColor(0.12, 0.12, 0.20, 1.0)   # azul escuro
        # Limpa o buffer de cor com a cor acima
        glClear(GL_COLOR_BUFFER_BIT)

        # Aqui entrariam as chamadas de desenho (próximas partes)

        # Troca o buffer traseiro (onde desenhamos) com o buffer frontal (tela)
        glfw.swap_buffers(janela)


def main():
    inicializar_glfw()
    janela = criar_janela(800, 600, "Parte 1 - Janela OpenGL com GLFW")
    configurar_viewport(janela)
    loop_principal(janela)
    glfw.terminate()
    print("Encerrado.")


if __name__ == "__main__":
    main()
