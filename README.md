# Folder Remover

[English](README.md) · [Español](README.es.md) · [Català](README.ca.md)

> Finds compressed files (`.zip`, `.rar`, `.7z`, `.tar.gz`…) and deletes the extracted folders that have the same name. A modern Windows 11 app.

## What it does

If it finds `file_1234.zip` and a folder called `file_1234` in the same directory, it offers to delete the folder, since its contents are already stored in the archive.

1. Choose a root folder and click **Search**.
2. Review the list of folders to delete (untick any you want to keep).
3. Click **Delete selected**: a window shows the final list, and after you confirm, all folders are deleted at once.

Supported archives: `.zip`, `.rar`, `.7z`, `.tar`, `.tar.gz`, `.tgz`, `.tar.bz2`, `.tar.xz`, `.gz`, `.bz2`, `.xz`. Matching is case-insensitive.

## Features

- Modern interface (CustomTkinter) with automatic light/dark theme.
- Option to include or skip subfolders.
- Sends folders to the **Recycle Bin** by default (can be turned off).
- Nothing is deleted without explicit confirmation.

## Usage

- With Python 3.9+: double-click `ejecutar.bat` (installs dependencies and starts the app).
- For a standalone `.exe` (no Python needed): double-click `compilar.bat` → `dist\Limpiador.exe`.

## License

GPL-3.0. See [LICENSE](LICENSE).
