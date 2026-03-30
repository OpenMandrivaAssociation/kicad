Name:		kicad
Version:	10.0.0
Release:	2
Summary:	EDA software suite for creation of schematic diagrams and PCBs
URL:		https://www.kicad.org
License:	GPL-3.0-or-later
Group:		Sciences/Computer science
Source0:	https://gitlab.com/kicad/code/kicad/-/archive/%{version}/kicad-%{version}.tar.gz
Source1:	https://gitlab.com/kicad/services/kicad-doc/-/archive/%{version}/kicad-doc-%{version}.tar.gz
Source2:	https://gitlab.com/kicad/libraries/kicad-templates/-/archive/%{version}/kicad-templates-%{version}.tar.gz
Source3:	https://gitlab.com/kicad/libraries/kicad-symbols/-/archive/%{version}/kicad-symbols-%{version}.tar.gz
Source4:	https://gitlab.com/kicad/libraries/kicad-footprints/-/archive/%{version}/kicad-footprints-%{version}.tar.gz
Source5:	https://gitlab.com/kicad/libraries/kicad-packages3D/-/archive/%{version}/kicad-packages3D-%{version}.tar.gz
# Source the rpmlintrc to clean false positives from build logs.
Source100:	%{name}.rpmlintrc
############################
BuildRequires:	appstream-util
BuildRequires:	boost-devel >= 1.87.0
BuildRequires:	chrpath
BuildRequires:	cmake
BuildRequires:	cmake(absl)
BuildRequires:	cmake(harfbuzz)
BuildRequires:	cmake(opencascade)
BuildRequires:	cmake(openssl)
BuildRequires:	desktop-file-utils
BuildRequires:	doxygen
BuildRequires:	fdupes
BuildRequires:	gcc-c++
BuildRequires:	gettext
BuildRequires:	glibc
BuildRequires:	glibc-devel
BuildRequires:	make
BuildRequires:	ninja
BuildRequires:	nng-devel
BuildRequires:	pkgconfig(appstream-glib)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(fmt)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(glm)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libgit2)
BuildRequires:	pkgconfig(libsecret-1)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(ngspice)
BuildRequires:	pkgconfig(odbc)
BuildRequires:	pkgconfig(pixman-1)
BuildRequires:	pkgconfig(poppler-glib)
BuildRequires:	pkgconfig(protobuf)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(source-highlight)
BuildRequires:	pkgconfig(spnav)
BuildRequires:	pkgconfig(zlib-ng)
BuildRequires:	protobuf-compiler >= 30.2
BuildRequires:	python-wxpython >= 4.0
BuildRequires:	shared-mime-info
BuildRequires:	swig
BuildRequires:	wxgtku3.2-devel

############################
# Documentation
BuildRequires:	po4a
BuildRequires:	asciidoctor

############################
Provides:	bundled(fmt) >= 9.0.0
Provides:	bundled(libdxflib) >= 3.26.4
Provides:	bundled(polyclipping) >= 6.4.2
Provides:	bundled(potrace) >= 1.15

############################
Requires:	pkgconfig(libgit2)
Requires:	pkgconfig(libsecret-1)
Requires:	pkgconfig(ngspice)
Requires:	pkgconfig(odbc)
Requires:	pkgconfig(protobuf)
Requires:	python-wxpython >= 4.0
Suggests:	kicad

Obsoletes:	%{name}-library < %{EVRD}
Obsoletes:	%{name}-unstable < %{EVRD}


%description
KiCad is EDA software to design electronic schematic diagrams and printed
circuit board artwork of up to 32 layers.

#%%patchlist

############################
%package	packages3d
Summary:	3D Models for KiCad
License:	CC-BY-SA-4.0
BuildArch:	noarch
Requires:	kicad >= %{version}-%{release}

%description	packages3d
3D Models for KiCad.

############################
%package	doc
Summary:	Documentation for KiCad
License:	GPL-3.0-or-later or CC-BY-3.0
BuildArch:	noarch
Obsoletes:	%{name}-doc < %{version}

%description	doc
Documentation for KiCad.

############################
%prep
%setup -q -n %{name}-%{version} -a1 -a2 -a3 -a4 -a5
%autopatch -p1

############################
%build

export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export LDFLAGS="%{ldflags} -v -Wl,--verbose --warn-backrefs"

# KiCad
# NOTE Keep KICAD_USE_CMAKE_FINDPROTOBUF set OFF, setting this ON will break-
# NOTE the build on modern platforms using CMake.
# NOTE Keep KICAD_WAYLAND set OFF, Wayland is unsuported by upstream at this time.
pushd .
%cmake \
	-DCMAKE_C_COMPILER="/usr/bin/clang" \
	-DCMAKE_CXX_COMPILER="/usr/bin/clang++" \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_INSTALL_DATADIR=%{_datadir} \
	-DCMAKE_INSTALL_DOCDIR=%{_docdir} \
	-DPYTHON_SITE_PACKAGE_PATH=%{python_sitearch} \
	-DKICAD_SCRIPTING_WXPYTHON=ON \
	-DKICAD_BUILD_I18N=ON \
	-DKICAD_BUILD_QA_TESTS=OFF \
	-DKICAD_USE_EGL=ON \
	-DKICAD_WAYLAND=OFF \
	-DKICAD_INSTALL_DEMOS=ON \
	-DKICAD_I18N_UNIX_STRICT_PATH=ON \
	-DKICAD_STDLIB_DEBUG=ON \
	-DKICAD_MAKE_LINK_MAPS=ON \
	-DKICAD_IPC_API=ON \
	-DKICAD_IDF_TOOLS=ON \
	-DKICAD_USE_CMAKE_FINDPROTOBUF=OFF \
	-DKICAD_VERSION_EXTRA=%{release} \
	-DKICAD_DATA=%{_datadir}/%{name} \
	-DKICAD_DOCS=%{_docdir}/%{name} \
	-G Ninja
%ninja_build
popd

# Templates
pushd %{name}-templates-%{version}/
%cmake \
	-G Ninja \
	-DKICAD_DATA=%{_datadir}/%{name}
%ninja_build
popd

# Symbol libraries
pushd %{name}-symbols-%{version}/
%cmake \
	-G Ninja \
	-DKICAD_PACK_SYM_LIBRARIES=ON \
	-DKICAD_DATA=%{_datadir}/%{name}
%ninja_build
popd

# Footprint libraries
pushd %{name}-footprints-%{version}/
%cmake \
	-G Ninja \
	-DKICAD_DATA=%{_datadir}/%{name}
%ninja_build
popd

# 3D models
pushd %{name}-packages3D-%{version}/
%cmake \
	-G Ninja \
	-DKICAD_DATA=%{_datadir}/%{name}
%ninja_build
popd

# Documentation (HTML only)
pushd %{name}-doc-%{version}/
%cmake \
	-G Ninja \
	-DADOC_TOOLCHAIN="ASCIIDOCTOR" \
	-DKICAD_DOC_PATH=%{_docdir}/kicad/help \
	-DPDF_GENERATOR=none \
	-DBUILD_FORMATS=html
%ninja_build -j1
popd

############################
%install

# KiCad application
%ninja_install -C build

# Binaries must be executable to be detected by find-debuginfo.sh
chmod +x %{buildroot}%{python3_sitearch}/_pcbnew.so

# Binaries are not allowed to contain rpaths
chrpath --delete %{buildroot}%{python3_sitearch}/_pcbnew.so

# Install desktop
for desktopfile in %{buildroot}%{_datadir}/applications/*.desktop ; do
	desktop-file-install \
	--dir %{buildroot}%{_datadir}/applications \
	--delete-original                          \
	${desktopfile}
done

# Templates
pushd %{name}-templates-%{version}/
%ninja_install -C build
cp -p LICENSE.md ../LICENSE-templates.md
popd

# Symbol libraries
pushd %{name}-symbols-%{version}/
%ninja_install -C build
cp -p LICENSE.md ../LICENSE-symbols.md
popd

# Footprint libraries
pushd %{name}-footprints-%{version}/
%ninja_install -C build
cp -p LICENSE.md ../LICENSE-footprints.md
popd

# 3D models
pushd %{name}-packages3D-%{version}/
%ninja_install -C build
popd

# Documentation
pushd %{name}-doc-%{version}/
%ninja_install -C build
popd

# find dupes
%fdupes %{buildroot}/%{_docdir}/%{name}/help
%fdupes %{buildroot}/%{_datadir}/%{name}
%fdupes %{buildroot}%{_datadir}/icons/hicolor
for lang in ca de en es fr id it ja pl ru zh ; do
    %fdupes %{buildroot}%{_docdir}/kicad/help/$lang
done

%find_lang %{name}

############################
%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml

############################
%files	-f %{name}.lang
%doc AUTHORS.txt
%attr(0755, root, root) %{_bindir}/*
%{_libdir}/%{name}/
%{_libdir}/libkiapi.so*
%{_libdir}/libkicad_3dsg.so*
%{_libdir}/libkigal.so*
%{_libdir}/libkicommon.so*
%{python3_sitearch}/_pcbnew.so
%{python3_sitearch}/pcbnew.py
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/bash-completion/completions/*
%{_datadir}/icons/hicolor/*/apps/*.*
%{_datadir}/icons/hicolor/*/mimetypes/application-x-*.*
%{_datadir}/mime/packages/*.xml
%{_datadir}/zsh/site-functions/*
%{_metainfodir}/*.metainfo.xml
%license LICENSE*
%exclude %{_datadir}/%{name}/3dmodels/*

%files	packages3d
%{_datadir}/%{name}/3dmodels/*.3dshapes
%license %{name}-packages3D-%{version}/LICENSE*

%files	doc
%{_docdir}/%{name}/help/
%exclude %{_docdir}/%{name}/AUTHORS.txt
%license %{name}-doc-%{version}/LICENSE*
