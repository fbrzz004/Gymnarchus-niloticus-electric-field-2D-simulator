import numpy as np
import matplotlib.pyplot as plt
from random import randint
from time import sleep as zZz

# Limites iniciales de los ejes
xi, xs = -4, 4  # Límites en el eje x (izquierda, derecha)
yi, ys = -4, 4  # Límites en el eje y (abajo, arriba)

# Posiciones iniciales de las cargas y residuo
posxCarga, posyCarga = -1, 0  # Posición de la primera carga
posxCarga2, posyCarga2 = 1, 0  # Posición de la segunda carga

# Imagen del pez
pez_img = plt.imread(r"res\fish.png")

def posAleatoria():
    # Genera una posición aleatoria dentro de los límites especificados
    x = randint(xi, xs)
    y = randint(yi, ys)
    return x, y

def crearMatriz():
    # Crea una matriz de coordenadas X e Y para representar el plano
    x = np.linspace(xi, xs, 25)
    y = np.linspace(yi, ys, 25)
    X, Y = np.meshgrid(x, y)
    return X, Y

def dividirMatriz(a, b):
    # Divide dos matrices elemento por elemento, evitando errores de división por cero
    mask = (b == 0)
    division = np.divide(a, b, out=np.zeros_like(a), where=~mask)
    return division

def campoElectrico(q, posx, posy, X, Y):
    # Calcula el campo eléctrico en cada punto del plano debido a una carga puntual
    k = 9 * 10**9  # Constante electrostática
    dx = X - posx
    dy = Y - posy
    d = np.hypot(dx, dy)**3  # Distancia entre la carga y cada punto del plano
    Ex = k * q * dividirMatriz(dx, d)  # Componente x del campo eléctrico
    Ey = k * q * dividirMatriz(dy, d)  # Componente y del campo eléctrico
    return Ex, Ey

def otraCarga(X, Y):
    # Calcula el campo eléctrico debido a otro objeto de carga (residuo) en el plano
    x, y = posxResiduo, posyResiduo
    Ex, Ey = campoElectrico(1, x, y, X, Y)
    return Ex, Ey

def dipoloPez():
    # Calcula el campo eléctrico total debido a las cargas y el residuo
    global x, y, x2, y2
    X, Y = crearMatriz()
    x, y = carga.center
    x2, y2 = carga2.center
    Ex1, Ey1 = campoElectrico(-1, x, y, X, Y)
    Ex2, Ey2 = campoElectrico(1, x2, y2, X, Y)
    Ex3, Ey3 = otraCarga(X, Y)
    Ex = Ex1 + Ex2 + Ex3  # Componente x del campo eléctrico total
    Ey = Ey1 + Ey2 + Ey3  # Componente y del campo eléctrico total
    E = np.hypot(Ex, Ey)  # Magnitud del campo eléctrico en cada punto
    i = dividirMatriz(Ex, E)  # Componente x normalizada del campo eléctrico
    j = dividirMatriz(Ey, E)  # Componente y normalizada del campo eléctrico
    return X, Y, i, j, E

def actualizar():
    # Actualiza la visualización del campo eléctrico y las cargas en el plano
    ax.cla()  # Limpia el eje antes de trazar nuevos elementos
    ax.add_patch(carga)
    ax.add_patch(carga2)
    ax.add_patch(carga3)
    ax.set_aspect('equal')  # Mantiene la relación de aspecto en el gráfico
    ax.set_xlim(xi, xs)  # Establece los límites del eje x
    ax.set_ylim(yi, ys)  # Establece los límites del eje y

    X, Y, i, j, E = dipoloPez()

    maskE = (E == 0)  # Máscara para evitar errores al calcular el logaritmo

    Er = np.sqrt(np.log(E), out=np.zeros_like(E), where=~maskE)  # Aplica la función sqrt(log(x)) a los valores de E

    # Genera un gráfico de contorno del campo eléctrico
    co = plt.contourf(X, Y, Er, levels=np.linspace(np.amin(Er), np.amax(Er), 20), zorder=0)

    plt.draw()
    plt.imshow(pez_img, extent=[x - 0.5, x2 + 0.5, y - 1, y2 + 1], zorder=4)

def on_key(event):
    # Maneja los eventos de presionar una tecla
    step = -1  # Tamaño del paso al mover las cargas y cambiar los límites del plano
    global xi, xs, yi, ys
    if event.key == 'up':
        # Mueve las cargas hacia arriba y ajusta los límites del plano
        carga.center = (x, y + step)
        carga2.center = (x2, y2 + step)
        yi, ys = yi + step, ys + step
        actualizar()
    elif event.key == 'down':
        # Mueve las cargas hacia abajo y ajusta los límites del plano
        carga.center = (x, y - step)
        carga2.center = (x2, y2 - step)
        yi, ys = yi - step, ys - step
        actualizar()
    elif event.key == 'left':
        # Mueve las cargas hacia la izquierda y ajusta los límites del plano
        carga.center = (x - step, y)
        carga2.center = (x2 - step, y2)
        xi, xs = xi - step, xs - step
        actualizar()
    elif event.key == 'right':
        # Mueve las cargas hacia la derecha y ajusta los límites del plano
        carga.center = (x + step, y)
        carga2.center = (x2 + step, y2)
        xi, xs = xi + step, xs + step
        actualizar()
    elif event.key == 'enter':
        # Crea un nuevo residuo y actualiza la visualización
        nuevoResiduo()
        actualizar()

def nuevoResiduo():
    # Genera una nueva posición para el residuo y crea un objeto de carga para representarlo
    global posyResiduo, posxResiduo, carga3
    posxResiduo = randint(xi, xs)
    posyResiduo = ys
    print("Posición del nuevo residuo: ", posxResiduo, "-", posyResiduo)
    carga3 = plt.Circle((posxResiduo, posyResiduo), 0.2, color="none", zorder=2)

nuevoResiduo()

fig, ax = plt.subplots()

carga = plt.Circle((posxCarga, posyCarga), 0.2, color="none", zorder=3)
ax.add_patch(carga)
carga2 = plt.Circle((posxCarga2, posyCarga2), 0.2, color="none", zorder=3)
ax.add_patch(carga2)
carga3 = plt.Circle((posxResiduo, posyResiduo), 0.2, color="none", zorder=2)
ax.add_patch(carga3)

x, y = carga.center
x2, y2 = carga2.center

ax.set_xlim(xi, xs)
ax.set_ylim(yi, ys)
ax.set_aspect('equal')

actualizar()

# Conectar la función on_key al evento de presionar una tecla
fig.canvas.mpl_connect('key_press_event', on_key)
plt.show()
