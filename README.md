# Explorando o Universo Gráfico com OpenGL: Uma Introdução Prática

Repositório da Atividade Avaliativa P1 — Computação Gráfica (UGB)

## Estrutura

| Arquivo | Conteúdo |
|---|---|
| `parte1_janela.py` | Introdução ao OpenGL e criação de janela com GLFW |
| `parte2_formas.py` | Primitivas geométricas: GL_POINTS, GL_LINES, GL_TRIANGLES |
| `parte3_cores.py` | Sistema de cores RGBA, glColor3f(), glColor4f(), interpolação |
| `parte4_transformacoes.py` | Transformações: glTranslatef(), glRotatef(), glScalef() |

## Dependências

```bash
pip install PyOpenGL PyOpenGL_accelerate glfw
```

## Como executar

```bash
python parte1_janela.py
python parte2_formas.py
python parte3_cores.py
python parte4_transformacoes.py
```

### Controles — Parte 4

| Tecla | Efeito |
|---|---|
| `1` | Exibe apenas translação |
| `2` | Exibe apenas rotação (animada) |
| `3` | Exibe apenas escala |
| `4` | Exibe todas as transformações combinadas (padrão) |
| `ESC` | Fecha a janela |
