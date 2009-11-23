# Buildfile to create packages for the Arch Build System.
# Contributor: Dominik Schacht <dominik.schacht@gmail.com>
pkgname=pynal
pkgver=0.1
pkgrel=1
pkgdesc="Journaling and pdf annotation application."
arch=(any)
url="http://github.com/dominiks/pynal"
license=('BSD')
depends=("python>=2.6" "pyqt>=4.5")
provides=("pynal")
source=($pkgname-$pkgver.tar.gz)

build() {
  cd "$srcdir/$pkgname-$pkgver"

  python setup.py install "--root=$pkgdir" || return 1
}

