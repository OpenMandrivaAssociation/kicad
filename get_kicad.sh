# https://github.com/KiCad/kicad-source-mirror.git
git clone https://github.com/KiCad/kicad-source-mirror.git
pushd kicad-source-mirror
git archive --format=tar --prefix kicad-4.0.2-$(date +%Y%m%d)/ HEAD | xz -vf > ../kicad-4.0.2-$(date +%Y%m%d).tar.xz
popd

git clone https://github.com/KiCad/kicad-library.git
pushd kicad-library
git archive --format=tar --prefix kicad-library-4.0.2-$(date +%Y%m%d)/ HEAD | xz -vf > ../kicad-library-4.0.2-$(date +%Y%m%d).tar.xz
popd

git clone https://github.com/KiCad/kicad-i18n.git
pushd kicad-i18n
git archive --format=tar --prefix kicad-i18n-4.0.2-$(date +%Y%m%d)/ HEAD | xz -vf > ../kicad-i18n-4.0.2-$(date +%Y%m%d).tar.xz
popd

git clone https://github.com/KiCad/kicad-doc.git
pushd kicad-doc
git archive --format=tar --prefix kicad-doc-4.0.2-$(date +%Y%m%d)/ HEAD | xz -vf > ../kicad-doc-4.0.2-$(date +%Y%m%d).tar.xz
popd
