# Flujo de cartas fianza

## Fuentes de información
| Tipo  | Descripción                                                           | Ubicación                                                                                                                                                                                                      |
|-------|-----------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| vídeo | Contiene la sesión de reunión donde se explica el problema de negocio | [enlace](https://us-east-1.console.aws.amazon.com/s3/object/videoscasosuso?region=us-east-1&bucketType=general&prefix=Revisi%C3%B3n+flujo+cartas+fianza-20250908_163258-Grabaci%C3%B3n+de+la+reuni%C3%B3n.mp4) |


## Composición de la tabla

### Tabla de reportes regulatorios
Una de las principales fuentes de información es la BDC01  (Reporte regulatorio)

  - **ccr**: Código de crédito, es único, es sobre el cual se debe iterar
  - **ccl**: Código de cliente.
  - **csbs**: Código SBS, es un código interno conocido por los clientes
  - **ncl**: Nombre de cliente
  - **<span style="color:red">kco</span>**: Indica que es el saldo
  - **<span style="color:red">ccco</span>**: El número de cuenta contable
  - **<span style="color:red">Convenio con FMV</span>**: Es una marca que indica que tiene un convenio

### Tablas internas
  - **ccr**: Código de crédito, es único, es sobre el cual se debe iterar
  - **ccl**: Código de cliente.
  - **ncl**: Nombre de cliente
  - **<span style="color:red">saldo carta fianza</span>**: Indica el saldo de la carta fianza

### Observaciones de la composición de la tabla
- La tabla incluirá tanto el kco del mes y del mes anterior
- La tabla incluirá el ccco del mes y del mes anterior
- La tabla incluirá una marca indicando si tiene un convenio con el fondo mi vivienda (FMV)

## Problema de negocio
Cuando existe una reducción, debe estar sustentado en las cartas fianza; estas cartas pertenecen al fondo mi vivienda
el cual es el fondo que la emite; tiene información asociada al nombre del cliente (<span style="color:yellow">promotor para el fondo mi vivienda</span>),
el detalle de saldo.
> "Se debe identificar los casos donde hubo una reducción y verificar si se encuentra con el sustento documentario (la carta fianza) que permita respaldar
> esa reducción"

> "Solo se hará la revisión sobre los elementos que tengan la marca de convenio con FMV"

## Campos de metadata a extraer (tanto para reporte regulatorios como tablas internas)
- **N° de crédito**: Número de crédito (código de credito)
- **Nombre del cliente**: Nombre del cliente
- **Saldo mes anterior**:Indica el saldo del mes anterior
- **saldo mes actual**: Indica el saldo del mes actual
- **diferencias**: Indica la diferencia entre el mes actual y el anterior
- **reducción del saldo FMV**:

## Operativa del problema de negocio

>Toda carta fianza lleva como nombre el código del crédito; pueden existir más de una carta para el mismo número de crédito; por lo cual
> se agrega un sufijo indicando _1, _2, _3.

### Tabla esperada
La tabla esperada es un consolidado

| N ° crédito | fecha | Nombre de cliente | Saldo Mes Anterior | Saldo mes Actual | Diferencias | Reducción del saldo FMV |
|-------------|-------|-------------------|--------------------|------------------|-------------|-------------------------|

> El proceso ETL debe capturar todos los metadatos solicitados para la tabla

> Se debe realizar la diferencia de los saldos (KCO) las cuáles deben estar justificadas en las cartas fianzas; estos saldos
> resultan el acumulado; por ejemplo si para un código de crédito (1) existen las cartas 1_1 y 1_2 la suma de las reducciones
> o diferencias debe ser la misma que se encuentra registrada en la tabla BDC01 de donde se extrajo el código de crédito

### Observaciones de la operativa
-Existen cartas que contienen más de un proyecto, para discernir se debe obtener el campo **<span style="color:red"> N° de garantía </span>**  el cual en realidad contiene
el nombre del proyecto



# Preguntas
- ¿El número de crédito, es el código de crédito?