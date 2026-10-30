# Folder Remover

[English](README.md) · [Español](README.es.md) · [Català](README.ca.md)

> Cerca fitxers comprimits (`.zip`, `.rar`, `.7z`, `.tar.gz`…) i elimina les carpetes descomprimides que tinguin el mateix nom. Aplicació moderna per a Windows 11.

## Què fa

Si troba `fitxer_1234.zip` i una carpeta anomenada `fitxer_1234` al mateix directori, proposa eliminar la carpeta, ja que el seu contingut està desat al comprimit.

1. Tria la carpeta arrel i prem **Buscar**.
2. Revisa la llista de carpetes a eliminar (desmarca les que vulguis conservar).
3. Prem **Eliminar seleccionades**: es mostra la llista final i, després de confirmar, s'eliminen totes d'un cop.

Comprimits admesos: `.zip`, `.rar`, `.7z`, `.tar`, `.tar.gz`, `.tgz`, `.tar.bz2`, `.tar.xz`, `.gz`, `.bz2`, `.xz`. No distingeix majúscules de minúscules.

## Característiques

- Interfície moderna (CustomTkinter) amb tema clar/fosc automàtic.
- Opció d'incloure o no les subcarpetes.
- Per defecte envia les carpetes a la **paperera de reciclatge** (es pot desactivar).
- No s'elimina res sense confirmació explícita.

## Ús

- Amb Python 3.9+: doble clic a `ejecutar.bat` (instal·la les dependències i inicia el programa).
- Per a un `.exe` independent (sense Python): doble clic a `compilar.bat` → `dist\Limpiador.exe`.

## Llicència

GPL-3.0. Consulta [LICENSE](LICENSE).
