Bitácora de Inteligencia Artificial — TFI Programación I - 2026

Carrera: Tecnicatura Universitaria en Telecomunicaciones (UTN FRBA)
Proyecto: Banco de Mediciones Automatizado en Python
Modelo de IA utilizado: Gemini – Hydrogen

Prompt Inicial

Hola Gemi como estas, soy estudiante de telecomunicaciones, necesito que te coloques en el rol de un experto en programación y código, sobre todo en lo que es Python y sus librerias estándar como socket y math, también podes usar otras, para que me ayudes en el trabajo final
Consigna: me pidieron desarrollar un código para un banco de mediciones automatizado, o sea una computadora que le habla a un instrumento de laboratorio, le pide mediciones, verifica que esas mediciones tengan sentido y escribe el informe.
La facultad me brindo instrumento_virtual.py : un programa que hace de cuenta que es el osciloscopio ADS3202 y el multímetro XDM1041 del laboratorio, y que contesta los mismos comandos que contestan los equipos de verdad.
Te adjunto los archivos que me dio la catedra
Tu objetivo es mediante las ideas y conceptos que te pase crear una función lo más eficiente posible, para que el proyecto te su resultado más óptimo. Yo realice los 2 primeros ejercicios que te los paso en el siguiente mensaje, por si queres cambiarlos. Corrí esos scripts y me dieron "pruebas ok "
te dejo un índice de como irán los archivos en orden
01_identificacion.py
02_magnitudes.py
03_comandos.py
04_configurar.py
05_cliente.py
06_barrido.py
07_verificacion.py
08_log.py
09_estadistica.py
10_informe.py
y esta observación de pruebas

Las pruebas van adentro del archivo
Al final de cada ejercicio, abajo de todo, va un bloque de pruebas. No hace falta ninguna
biblioteca: con assert alcanza. El patrón es siempre este:

...
# ---- pruebas ----
assert parsear_idn("OWON,ADS3202,254,V1.0") is not None
assert parsear_idn("OWON,ADS3202,254") is None
assert parsear_idn("") is None
print("pruebas OK")
Mínimo tres assert por ejercicio, y por lo menos uno tiene que ser un caso raro:
la lista vacía, el valor que falta, el canal que no existe, el número que no es un número.

te pido que te tomas tu tiempo para entender las consignas y si podés ver los archivos que te pase, para empezar a iniciar el proyecto




Prompt: Necesito hacer una función donde se reciba el texto (*IDN?), esta función tiene que devolver un diccionario con las siguientes claves: "fabricante, modelo, serie y versión". Agregar una condicional, si la respuesta no sirve, que devuelva "None". Los campos TIENEN que estar separados por comas, y que solamente se muestren 4 campos, en caso de que haya instrumentos que devuelvan 5 o más campos. Casos a tener en cuenta, campos < 4, cadena vacía, campos con espacios de más alrededor y la respuesta ERROR: comando desconocido.

Ejercicios 1 y 2
Le pase a la IA unos scripts que había hecho, donde la base está bastante sólida, pero me devolvió dos funciones mejoradas con ciertos retoques donde me aclaro “• Qué pasa si un mensaje de error trae comas: En tu código actual, "ERROR: comando desconocido" devuelve None de casualidad porque no tiene comas (entonces len(datos) es 1 y es < 4). Pero si un instrumento llegara a devolver "ERROR: parámetro inválido, revise el canal, intente de nuevo, código 400" (que tiene 4 partes separadas por comas), tu función lo tomaría como válido y guardaría "ERROR: parámetro inválido" como fabricante.

Donde se mejoraron las líneas  en los campos y se le agrego “.strip()” para quitar espacios sobrante para achicar los márgenes de errores y se agregó un if len, para detectar que una respuesta no sirve si hay menos de cuatro campos.
Lo comprobé haciendo la prueba con mi código anterior, donde si yo ponía espacios, mi función lo tomaría como valido.
En el caso de la función 2 “02_magnitudes.py” hizo una versiona mas limpia de los prejios, que resulto más fácil de leer y agradable a la vista. Además de agregar más pruebas

Ejercicio 3
Prompt inicial: “bien okey gemi, sigamos entonces, esa sería la consigna 3, tengo que crear una función comando, que termine en True si el comando termina con un signo de pregunta si mal no entendí, y más adelante agregarle un mensaje de error que yo quiera ?”

Me devolvió un archivo con dos definiciones detalladas “es consulta” y “validar”, donde lo importante fue el orden de los if y como se fueron descartando los errores

Ejercicio 4 – Configuración del canal
Necesito que el próximo script devuelva una lista que sea “canal, display, acoplamiento, sonda, escala” tratando de respetar este orden. 
Los canales deben ser CH1 O CH2, de lo contrario que devuelva None
Esta función es correlativa al ejercicio anterior y tiene que pasar por todos los comandos del ejercicio anterior
La IA devolvió una función concisa que funciono a la perfección.



Ejercicio 5 – Cliente
Prompt: ¿vamos por la 5, acá el script tendría que darme una pregunta verdad? y tiene que devolver una respuesta que este pasada por parsear_idn no ?
La IA: Respondió con una función eficiente y además aclarándome algunas cuestiones que tenía con la función socket  y como funciona la red en el instrumento




Ejercicio 6 – Función Barrer


En este ejercicio la IA me devolvió una función, que cuando la ejecute me tiraba algunos errores en varias líneas. Al principio era en el primer bucle For “canal in canales:” lo cual se soluciono agregando un Append y en otra línea también con las pruebas había dado mal los resultados, lo  cual se agregó un bloque llamado “falso error”


Ejercicio 7 - Verificaciones
Ayúdame a armar el código del ejercicio 7, con sus 3 funciones, es el ejercicio central del trabajo, te paso los datos y la consigna para que puedas observar lo que tiene que devolver y sus condicionales n cada respuesta.
Me devolvió 3 funciones y cada una explicando cómo se resuelve y con sus formulas

Ejercicio 8 – Mediciones
Prompt : realizar un script que se llame 08_log.py , en este trabajo hay que utilizar un bloc de notas con distintas mediciones que nos da la catedra, que te lo adjunto.
la parte A es “analizar línea” donde en cada línea Tenes que clasificar uno de los tres caminos posibles, si se ignora, se rechaza o es válida. Esto siempre es cuando pase todos los filtros y devolves un diccionario con los datos
Parte B leer_log, esto debería abrir el archivo de mediciones.log , lo recorre detalladamente, dentro de ella debe existir una función analizar línea donde debe devolver None, y su motivo, de lo contrario mediciones donde guarde su valor numérico.

La IA en principio devolvió una función que funcionaba, valga la redundancia, daba sus resultado ok, le agregue algunas funciones auxiliares de hora y fecha, que podían hacer que el script funcione con mas precisión, como se hizo en el ejercicio numero 2



9 – Estadística de una seria
okey gemi pasemos al ejercicio 9
hay que hacer una función q que devuelve un diccionario con n , mínimo , máximo , promedio y desvió , o None si la lista esta vacía. b) fuera_de_rango(valores, minimo, maximo) ,
que devuelve las posiciones de los valores que se salen del rango. Los dos extremos del
rango cuentan como adentro.
El desvío estándar de la muestra se calcula dividiendo por n - 1 :
desvió = raíz( suma((v - promedio)^2) / (n - 1) )
Devolución de la IA: realizo una función eficiente, donde me mostro como calcula el desvió estándar solicitado, se realizo las pruebas de control con los datos de mediciones y dio “Pruebas Ok”
Solo realice un cambio en el orden del indicie y verifique que el script funcionaba ya que cuando cambia los números de mediciones daba algunos errores.
Ejercicio 10 - 
Prompt: bien gemi pasemos al ejercicio 10, el informe, "armar informe que devuelve todo el proceso completo en una sola cadena de texto, una línea por serie, con su n máximo, mínimo, promedio, con unidades legibles y el resultado de cada verificación
Aclaración: la función no imprime nada y no abre ningún archivo, como pudiste observar en el pdf
Devolución de la IA: devolvió una función pura que recibe los datos y devuelve el informe en una sola cadena de texto.
Puntualmente no toqué mucho y tampoco se me ocurrieron ideas para agregar debido a que el bloque era bastante largo, si le hice preguntas sobre las funciones y que hacía varias definiciones. Como el finally, varios if not y else.

