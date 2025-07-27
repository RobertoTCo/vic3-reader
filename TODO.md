### TODO

1. En la subcarpeta metrics, crear las funciones que permitan extraer cada métrica necesaria.

2. Crear una clase que haga uso de las funciones en metrics para obtener las métricas respecto a TAGs en los que estemos interesados.

3. Crear métodos para obtener las métricas de alto nivel (que no cambian por país)

4. Crear una clase o sistema de funciones que usen lo definido en 2. y 3. para leer un archivo y obtener todo validado como pandas dataframe.

5. Crear una función que explore los saves que queramos, y reestructure múltiple pandas para varios años de la forma que queramos (filas: años, columnas: tags, hojas: variables)

6. Crear métodos que permita añadir nuevas columnas a partir de las métricas inciales.

##### Métricas:

1. Prestigio (es un valor en country manager, por país)
2. GDP (es un valor en country manager, por país)
3. SoL (no sé dónde esta) 
4. POP (suma de los 3 estratos en pop_statistics, country manager, por país)
5. Peasants (en population_workforce_by_profession (creo, uk tiene 3.9M) , pop_statistics, country manager, por país; hay que sacar el ID)
6. employed (no sé, debería de ser en pop_statistics)
7. Literacy
8. Construcción
9. national revenue (ingresos, no investment pool) (el de por semana?)
10. gastos (el de por semana?)
11. Debt (principal, está hecho)
12. Army
13. Navy