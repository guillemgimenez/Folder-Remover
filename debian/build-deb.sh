#!/bin/sh
# Genera dist/folder-remover_<version>_all.deb (Debian / Ubuntu / Mint...)
set -e
VERSION="${1:-1.0.0}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PKG="$ROOT/build/folder-remover_${VERSION}_all"

rm -rf "$PKG"
mkdir -p "$PKG/DEBIAN" "$PKG/opt/folder-remover" "$PKG/usr/bin" "$PKG/usr/share/applications"

install -m 644 "$ROOT/limpiador.py" "$ROOT/requirements.txt" "$PKG/opt/folder-remover/"
install -m 755 "$ROOT/debian/folder-remover.sh" "$PKG/usr/bin/folder-remover"
install -m 644 "$ROOT/debian/folder-remover.desktop" "$PKG/usr/share/applications/"
install -m 755 "$ROOT/debian/postinst" "$ROOT/debian/prerm" "$PKG/DEBIAN/"

cat > "$PKG/DEBIAN/control" <<CTRL
Package: folder-remover
Version: $VERSION
Section: utils
Priority: optional
Architecture: all
Depends: python3 (>= 3.9), python3-tk, python3-venv, python3-pip
Maintainer: Guillem Gimenez <ggimenez@olot.cat>
Description: Elimina carpetas descomprimidas que ya existen como comprimido
 Busca archivos comprimidos (zip, rar, 7z, tar.gz...) y elimina las carpetas
 con el mismo nombre, mostrando antes la lista y pidiendo confirmación.
CTRL

mkdir -p "$ROOT/dist"
dpkg-deb --build --root-owner-group "$PKG" "$ROOT/dist/"
echo "Listo: dist/folder-remover_${VERSION}_all.deb"
