import numpy as np

import matplotlib.pyplot as plt

num_nodos_y = 331  # numero de columnas con mas una columnas de ceros implicita
num_nodos_x = 63 # numero de filas con mas una filas de ceros implicita

num_nodos_x1 = num_nodos_x + 1 # numero de filas de el universo mas una filas de ceros

num_nodos_y1 = num_nodos_y + 1 # numero de columnas de el mundo con una columnas de cerps
 
mundo0 = np.zeros(( num_nodos_x1 , num_nodos_y1 ))# mundo inicial 

mundo1 = np.zeros(( num_nodos_x1 , num_nodos_y1 ))# copia del mundo

Ey = np.zeros(( num_nodos_x1 , num_nodos_y1 ))# campo electrico en y

Ex = np.zeros(( num_nodos_x1 , num_nodos_y1 ))# campo electrico en y

Exy = np.zeros(( num_nodos_x1 , num_nodos_y1 ))# campo electrico en y

c = np.zeros((1,260)) #matriz de capacitancia

imin = 500 # maximo de iteraciones
iteraciones  = 1000 #numero de iteraciones minimas 
err = 100 # error inicial de esta forma err != de 0

for n in range(iteraciones):# iteraciones
    err = 100 # error inicial de esta forma err != de 0
    for i in range(num_nodos_x1): # recorrer i y j en el ranga de la matriz mundo
        for j in range(num_nodos_y1): 
            mundo0[0 : num_nodos_x1 - 1][0] = 0 # que la filais "0" y "num_nodos_x1 - 1" sean ceros 
            mundo0[num_nodos_x1 - 1 : num_nodos_x1][0] = 0 
            mundo0[i][0] = 0# que la columnas "0" y "num_nodos_y1 - 1" sean ceros
            mundo0[i][num_nodos_y1-1] = 0
            mundo0[29][35 : 296] = 200# placas paralelas en mundo0
            mundo0[35][35 : 296] = 0
            if i>=1 and j >=1:# el prime nodo se (1,1) y de esta forma no tome ni la fila 0 ni la columna 0
                if i < num_nodos_x1-1 and j < num_nodos_y1-1:
                    error1a = np.sum(mundo0, axis=1)#suma de todas las filas de la matriz mundo0                
                    error1b = np.sum(error1a, axis=0)#suma de todas la columna de la matriz error1a               
                    mundo1[i][j]=(mundo0[i+1][j]+ mundo0[i][j+1] +mundo0[i-1][j]+ mundo0[i][j-1])/4 #para hacer la operacion de voltage y que el ultimo nodo sea (num_nodos_x1-1,num_nodos_x1-1) sin tomar la ultima fila ni la ultima columna
                    mundo1[29][35 : 296] = 200
                    mundo1[35][35 : 296] = 0
                    error2a = np.sum(mundo1, axis=1)#suma de todas las filas de la matriz mundo1
                    error2b = np.sum(error2a, axis=0)#suma de todas la columna de la matriz error2a
    err = ((error1b-error2b)/error2b)*100#encontramos el error de toda la matriz
    if err < 0 : # el error siempre sea positivo
        err = -err
    if n > 500:# despues de las iteraciones minimas se salga si el error es menor a 0.01%
        if err <= 0.01:
            break
    mundo1=mundo0

    
    
Ey, Ex = np.gradient(mundo1) #encontramos el gradiente de la matriz de potencial para de esta forma encontrar el campo electrico tanto en x como en y
Ey, Ex = -Ey, -Ex #  el campo electrico nos da negativo asi que lo volvemos positivo
                 
Exy = ((Ex)**2+(Ey)**2)**1/2# encontramos en 
    
for i in range(260):
    for j in range(35, 296): 
        c[0][i]= (Exy[30][j]*8.85e-12*2.04)/200#se calcula la matriz de capacitancia en cada uno de los puntos que estab debajo de una placa
                                              #se multiplica el campo electrico por el epsilon0 por 2.1 metros y de divide en voltage en ese punto
                                              #se multiplica por 2 metros debido a que la parametrizacion es de 1 mm si multiplicamos 2 po 0.001 da 0.00204mm^2 y si sumamos eso 260 veces da 0.05309m^2 que es el harea de una placa circular de radio 0.13m
C = (np.sum(c, axis=1))/260# se encuentra la capazitancia total sumando la capacitancia en cada uno de los punto y dividiendo en el numero de puntos, de esta forma se encuantra la capacitancia promedio 
print(C)       
        
        
        
fig1 = plt.figure(1)#graficamos la matriz de potencial 
f1 = plt.contourf(mundo1, 10, cmap ='jet')
plt.colorbar(f1) #Barra de color al lado de la gráfica
plt.xlabel("Largo [mm]") #nombre eje x
plt.ylabel("Alto [mm]") #nombre eje y
plt.savefig("potencial.png", dpi=300)  # Guardo la figura en formato png a 300 DPI


fig2 =  plt.figure(2)# graficamops la matriz del campo electrico 
f2 = plt.contourf(Exy, 40, cmap ='jet')
cb = plt.colorbar(f2)  #Barra de color al lado de la gráfica
plt.xlabel("Largo [mm]") #nombre eje x
plt.ylabel("Alto [mm]") #nombre eje y
plt.savefig("campo_electrico.png", dpi=300)  # Guardo la figura en formato png a 300 DPI













