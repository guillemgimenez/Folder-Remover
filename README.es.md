# Folder Remover

[English](README.md) · [Español](README.es.md) · [Català](README.ca.md)

> Busca archivos comprimidos (`.zip`, `.rar`, `.7z`, `.tar.gz`…) y elimina las carpetas descomprimidas que tengan el mismo nombre. Aplicación moderna para Windows 11.

## Qué hace

Si encuentra `fichero_1234.zip` y una carpeta llamada `fichero_1234` en el mismo directorio, propone eliminar la carpeta, ya que su contenido está guardado en el comprimido.

1. Elige la carpeta raíz y pulsa **Buscar**.
2. Revisa la lista de carpetas a eliminar (desmarca las que quieras conservar).
3. Pulsa **Eliminar seleccionadas**: se muestra la lista final y, tras confirmar, se eliminan todas de golpe.

Comprimidos admitidos: `.zip`, `.rar`, `.7z`, `.tar`, `.tar.gz`, `.tgz`, `.tar.bz2`, `.tar.xz`, `.gz`, `.bz2`, `.xz`. No distingue mayúsculas de minúsculas.

## Características

- Interfaz moderna (CustomTkinter) con tema claro/oscuro automático.
- Opción de incluir o no las subcarpetas.
- Por defecto envía las carpetas a la **papelera de reciclaje** (se puede desactivar).
- No se elimina nada sin confirmación explícita.

## Uso

- Con Python 3.9+: doble clic en `ejecutar.bat` (instala las dependencias y lanza el programa).
- Para un `.exe` independiente (sin Python): doble clic en `compilar.bat` → `dist\Limpiador.exe`.

## Licencia

GPL-3.0. Consulta [LICENSE](LICENSE).
