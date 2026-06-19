# Tools — Mapa visual del campus

`generate_campus_map.py` genera un archivo **HTML interactivo** con todos los
nodos, caminos y entradas de edificio que usa la app, leyendo directamente los
tres `.plist` de la carpeta `../Data/`. Es una ayuda visual para revisar y dar
seguimiento al grafo de navegacion (no forma parte de la app; es una utilidad
de apoyo).

## Como se usa

Necesitas **Python 3** (ya viene en macOS). Desde esta carpeta `Tools/`:

```bash
python3 generate_campus_map.py
```

Eso crea `campus_map.html` aqui mismo. Abrelo con doble clic o:

```bash
open campus_map.html
```

> Requiere internet al abrirlo, porque carga la libreria Leaflet y los mapas de
> OpenStreetMap desde la web.

### Opciones

```bash
# Usar plists de otra carpeta (p. ej. unos nuevos en Downloads)
python3 generate_campus_map.py --data ~/Downloads

# Elegir donde guardar el HTML
python3 generate_campus_map.py --out ~/Desktop/campus_map.html
```

## Que muestra el mapa

| Elemento | Color | Origen |
|----------|-------|--------|
| Caminos accesibles | azul | `ListaCaminos.plist` (`accesible = true`) |
| Caminos regulares | naranja | `ListaCaminos.plist` (`accesible = false`) |
| Nodos | verde | `Coords.plist` |
| Entradas de edificio | rojo | `ListaEdificios.plist` (`coord` + `nombre`) |

Las casillas de la leyenda (arriba a la derecha) prenden/apagan cada capa, y al
hacer clic en un punto aparece su **indice** (y el nombre si es un edificio).
Ese indice es el mismo que se usa como `punto1` / `punto2` en `ListaCaminos.plist`
y dentro de `coord` en `ListaEdificios.plist`, asi que sirve para depurar
conexiones del grafo.

## Detalle importante de los datos

En `Coords.plist` los nombres de las llaves estan **invertidos** a proposito
(se conservan asi en la app):

- `longitud` contiene en realidad la **latitud** (~25.6x)
- `latitud` contiene en realidad la **longitud** (~-100.2x)

El script ya lo maneja. Los nodos con coordenada `0,0` se marcan como invalidos
y no se dibujan.

## Para regenerar tras editar los datos

1. Edita los `.plist` en `../Data/`.
2. Vuelve a correr `python3 generate_campus_map.py`.
3. Refresca el HTML en el navegador.
