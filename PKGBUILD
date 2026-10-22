# Maintainer: Apex <apex@archlinux.local>
pkgname=win11-explorer-git
_pkgname=win11-explorer
pkgver=1.0.0
pkgrel=1
pkgdesc="A 1:1 replica of Windows 11 File Explorer for Arch Linux built with PyQt6 and Fluent Design"
arch=('any')
url="https://github.com/apex/win11-explorer"
license=('MIT')
depends=('python' 'python-pyqt6' 'python-send2trash')
makedepends=('python-build' 'python-installer' 'python-wheel' 'python-setuptools')
source=("git+$url.git"
        "win11-explorer.desktop")
sha256sums=('SKIP'
            'SKIP')

pkgver() {
  cd "$srcdir/$_pkgname"
  printf "1.0.0.r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

build() {
  cd "$srcdir/$_pkgname"
  python -m build --wheel --no-isolation
}

package() {
  cd "$srcdir/$_pkgname"
  python -m installer --destdir="$pkgdir" dist/*.whl

  # Desktop launcher and icon
  install -Dm644 win11-explorer.desktop "$pkgdir/usr/share/applications/win11-explorer.desktop"
  install -Dm644 win11_explorer/resources/icons/explorer.png "$pkgdir/usr/share/icons/hicolor/128x128/apps/win11-explorer.png"
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
