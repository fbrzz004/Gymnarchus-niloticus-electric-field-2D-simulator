import numpy as np
import matplotlib.pyplot as plt
from random import randint
from time import sleep as zZz

xi, xs = -4, 4  
yi, ys = -4, 4 

posxCarga, posyCarga = -1, 0  
posxCarga2, posyCarga2 = 1, 0 

pez_img = plt.imread(r"res\fish.png")

def posAleatoria():
    x = randint(xi, xs)
    y = randint(yi, ys)
    return x, y

def crearMatriz():
    x = np.linspace(xi, xs, 100)
    y = np.linspace(yi, ys, 100)
    X, Y = np.meshgrid(x, y)
    return X, Y

def dividirMatriz(a, b):
    mask = (b == 0)
    division = np.divide(a, b, out=np.zeros_like(a), where=~mask)
    return division

def campoElectrico(q, posx, posy, X, Y, Permitividad):
    dx = X - posx
    dy = Y - posy
    d = np.hypot(dx, dy)**3  
    FactorE = (1 / (4 * np.pi * Permitividad) ) * q
    Ex = FactorE * dividirMatriz(dx, d) 
    Ey = FactorE * dividirMatriz(dy, d) 
    return Ex, Ey

def dipoloPez():
    global x, y, x2, y2, residuo
    X, Y = crearMatriz()
    x, y = carga.center
    x2, y2 = carga2.center
    Permitividad = crearMatrizPermitividad(X, Y, residuo, permitividadAmbiente, permitividadResiduo)
    Ex1, Ey1 = campoElectrico(-1, x, y, X, Y, Permitividad)
    Ex2, Ey2 = campoElectrico(1, x2, y2, X, Y, Permitividad)
    Ex = Ex1 + Ex2 
    Ey = Ey1 + Ey2 
    E = np.hypot(Ex, Ey) 
    i = dividirMatriz(Ex, E) 
    j = dividirMatriz(Ey, E) 
    return X, Y, i, j, E

def crearMatrizPermitividad(X, Y, residuo, permitividadAmbiente, permitividadResiduo):
    posxResiduo, posyResiduo = residuo.center
    dx = X - posxResiduo
    dy = Y - posyResiduo
    d = np.sqrt(np.hypot(dx, dy)**2)
    Permitividad = np.where(d > residuo.radius, permitividadAmbiente, permitividadResiduo)
    return Permitividad

def actualizar():
    ax.cla() 
    ax.add_patch(carga)
    ax.add_patch(carga2)
    ax.add_patch(residuo)
    ax.set_aspect('equal') 
    ax.set_xlim(xi, xs)
    ax.set_ylim(yi, ys)

    X, Y, i, j, E = dipoloPez()

    maskE = (E == 0) 

    #Er = E

    Er = np.sqrt(np.log(E), out=np.zeros_like(E), where=~maskE)  

    co = plt.contourf(X, Y, Er, levels=np.linspace(np.amin(Er), np.amax(Er), 20), zorder=0)

    plt.draw()
    plt.imshow(pez_img, extent=[x - 0.5, x2 + 0.5, y - 1, y2 + 1], zorder=4)

def on_key(event):
    step = -1  
    global xi, xs, yi, ys
    if event.key == 'up':
        carga.center = (x, y + step)
        carga2.center = (x2, y2 + step)
        yi, ys = yi + step, ys + step
        actualizar()
    elif event.key == 'down':
        carga.center = (x, y - step)
        carga2.center = (x2, y2 - step)
        yi, ys = yi - step, ys - step
        actualizar()
    elif event.key == 'left':
        carga.center = (x - step, y)
        carga2.center = (x2 - step, y2)
        xi, xs = xi - step, xs - step
        actualizar()
    elif event.key == 'right':
        carga.center = (x + step, y)
        carga2.center = (x2 + step, y2)
        xi, xs = xi + step, xs + step
        actualizar()
    elif event.key == 'enter':
        nuevoResiduo()
        actualizar()

def nuevoResiduo():
    global residuo
    posxResiduo = randint(xi, xs)
    posyResiduo = ys
    radioResiduo = 0.5
    print("Posición del nuevo residuo: ", posxResiduo, "-", posyResiduo)
    residuo = plt.Circle((posxResiduo, posyResiduo), radioResiduo, facecolor="none", edgecolor="black", zorder=2)

fig, ax = plt.subplots()

permitividadResiduo = 8.85*2.4*10**(-12)
permitividadAmbiente = 8.85*80*10**(-12)

carga = plt.Circle((posxCarga, posyCarga), 0.2, color="none", zorder=3)
ax.add_patch(carga)
carga2 = plt.Circle((posxCarga2, posyCarga2), 0.2, color="none", zorder=3)
ax.add_patch(carga2)
nuevoResiduo()
ax.add_patch(residuo)

x, y = carga.center
x2, y2 = carga2.center

ax.set_xlim(xi, xs)
ax.set_ylim(yi, ys)
ax.set_aspect('equal')

actualizar()

fig.canvas.mpl_connect('key_press_event', on_key)
plt.show()
