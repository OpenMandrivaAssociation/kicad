%define	Werror_cflags	%nil
%define	debug_package	%nil
%define _disable_lto 1
%define date %nil

# Use ./update.sh to generate latest tarballs and the corresponding
# specfile fragment

%define	name kicad
%define	version 5.1.0

%define	docname kicad-doc
%define tempname kicad-templates
%define symname kicad-symbols
%define footname kicad-footprints

%define i18nname kicad-i18n

Name:		%{name}
Summary:	An open source program for the creation of electronic schematic diagrams
Version:	%{version}
Release:	1
# git clone https://github.com/KiCad/kicad-source-mirror.git
# pushd kicad-source-mirror
# git archive --format=tar --prefix %{name}-%{version}-$(date +%Y%m%d)/ HEAD | xz -vf > ../%{name}-%{version}-$(date +%Y%m%d).tar.xz
# popd
Source0:	https://launchpad.net/kicad/5.0/5.1.0/%{version}/+download/%{name}-%{version}.tar.xz
Source1:	%{docname}-%{version}.tar.gz
Source2:	%{tempname}-%{version}.tar.gz
Source3:        %{symname}-%{version}.tar.gz
Source4:        %{footname}-%{version}.tar.gz
Source5:	%{i18nname}-%{version}.tar.gz

Source100:	kicad.rpmlintrc
License:	GPLv2+
Group:		Sciences/Computer science
Url:		http://www.kicad-pcb.org
BuildRequires:	fontconfig
BuildRequires:	wxgtku3.0-devel
BuildRequires:	mesa-common-devel
BuildRequires:	imagemagick
BuildRequires:	boost-devel
BuildRequires:	glew-devel
BuildRequires:	cairo-devel
BuildRequires:	openssl-devel
BuildRequires:	gomp-devel
BuildRequires:	cmake
BuildRequires:	pkgconfig(glm)
BuildRequires:	pkgconfig(ngspice)
BuildRequires:	pkgconfig(python2)
BuildRequires:	pkgconfig(sm)
BuildRequires:	curl-devel
BuildRequires:	opencascade-devel
BuildRequires:	wxPythonGTK-devel >= 3.0

BuildRequires:	source-highlight
BuildRequires:	doxygen
BuildRequires:	desktop-file-utils
BuildRequires:	po4a
BuildRequires:	asciidoc
BuildRequires:	a2x
BuildRequires:	perl(Unicode::GCString)
BuildRequires:	swig
Requires:	%{docname}

%description
Kicad is an open source (GPL) program for the creation of electronic
schematic diagrams and printed circuit board artwork.

Kicad is a set of four programs and a project manager:

* Eeschema:	Schematic entry.
* Pcbnew:	Board editor.
* Gerbview:	GERBER viewer (photoplotter documents).
* Cvpcb:	footprint selector for components used in the circuit design.
* Kicad:	project manager.

%package doc
Summary:	Documentation for kicad (creation of electronic schematic diagrams)
License:	GPL
Requires:	%{name}
BuildArch:	noarch

%description doc
Kicad is an open source (GPL) program for the creation of electronic
schematic diagrams and printed circuit board artwork.

Kicad-doc is the documentation for kicad.

%package library
Summary:	Library for kicad (creation of electronic schematic diagrams)
License:	GPL
Requires:	%{name}
BuildArch:	noarch

%description library
Kicad is an open source (GPL) program for the creation of electronic
schematic diagrams and printed circuit board artwork.

Kicad-library is a set of library needed by kicad.

%prep
%setup -q -T -b 0 -n %{name}-%{version}
%setup -q -T -b 1 -n %{docname}-%{version}
%setup -q -T -b 2 -n %{tempname}-%{version}
%setup -q -T -b 3 -n %{symname}-%{version}
%setup -q -T -b 4 -n %{footname}-%{version}
%setup -q -T -b 5 -n %{i18nname}-%{version}

cd ..

# proper libname policy
pushd %{name}-%{version}
sed -i "s|KICAD_PLUGINS lib/kicad/plugins|KICAD_PLUGINS %{_lib}/kicad/plugins|g" CMakeLists.txt
# KICAD_LIB ${CMAKE_INSTALL_PREFIX}/lib
sed -i "s!CMAKE_INSTALL_PREFIX}/lib!CMAKE_INSTALL_PREFIX}/%{_lib}!g" CMakeLists.txt
popd

%build
%setup_compile_flags
export CXX="%__cxx -std=c++11"
export LC_ALL=C

# Building kicad

	%cmake \
		-DBUILD_SHARED_LIBS:BOOL=OFF \
		-DKICAD_STABLE_VERSION:BOOL=ON \
		-DKICAD_wxUSE_UNICODE=ON \
		-DCMAKE_BUILD_TYPE=Release \
		-DKICAD_SKIP_BOOST=ON \
		-DKICAD_REPO_NAME=stable \
		-DBUILD_GITHUB_PLUGIN=ON \
		-DwxWidgets_CONFIG_EXECUTABLE=%{_bindir}/wx-config

	#ugly workaround to fix build
	#dunno what causes the extra ; in CXX_FLAGS which causes the failure
	find . -name flags.make -exec sed -i -e 's,-pthread;-fpermissive,-pthread -fpermissive,g' {} \;
	find . -name link.txt -exec sed -i -e 's,-pthread;-fpermissive,-pthread -fpermissive,g' {} \;

	%make_build
	
cd ..

# Building kicad-doc
pushd %{docname}-%{version}
	%cmake \
		-DKICAD_STABLE_VERSION:BOOL=ON \
		-DKICAD_wxUSE_UNICODE=ON \
		-DCMAKE_BUILD_TYPE=Release \
		-DBUILD_FORMATS=html
	%make_build
popd


# Building kicad-i18n
pushd %{i18nname}-%{version}
	%cmake \
		-DKICAD_STABLE_VERSION:BOOL=ON \
		-DCMAKE_BUILD_TYPE=Release \
		-DKICAD_I18N_UNIX_STRICT_PATH=ON
	%make_build
popd

# Building kicad-symbols
pushd %{symname}-%{version}
        %cmake \
                -DKICAD_STABLE_VERSION:BOOL=ON \
                -DCMAKE_BUILD_TYPE=Release 
        %make_build
popd

# Building kicad-footprints
pushd %{footname}-%{version}
        %cmake \
                -DKICAD_STABLE_VERSION:BOOL=ON \
                -DCMAKE_BUILD_TYPE=Release
        %make_build
popd

# Building kicad-templates
pushd %{tempname}-%{version}
        %cmake \
                -DKICAD_STABLE_VERSION:BOOL=ON \
                -DCMAKE_BUILD_TYPE=Release
        %make_build
popd
%install
cd ../

# Installing kicad-symbols
pushd %{symname}-%{version}
       make -C build DESTDIR=%buildroot install
popd

# Installing kicad-footprints
pushd %{footname}-%{version}
       make -C build DESTDIR=%buildroot install
popd

# Installing kicad-templates
pushd %{tempname}-%{version}
       make -C build DESTDIR=%buildroot install
popd

# Installing kicad-packages3D
pushd %{symname}-%{version}
       make -C build DESTDIR=%buildroot install
popd

# Installing kicad-doc
pushd %{docname}-%{version}
	make -C build DESTDIR=%buildroot install
popd

# Installing kicad-i18n
pushd %{i18nname}-%{version}
	make -C build DESTDIR=%buildroot install
	%find_lang %{name}
popd

# Installing kicad-%{version}
pushd %{name}-%{version}
	make -C build DESTDIR=%buildroot install

	# create desktop file
	desktop-file-install --vendor='' \
		--remove-category='Scientific' \
		--add-category='Science;Electronics;Education' \
		--dir=%buildroot%{_datadir}/applications \
		%buildroot%{_datadir}/applications/*.desktop

popd

%files -f %{name}.lang
%{_bindir}/*
%{_iconsdir}/*/*/*
%{_datadir}/%{name}/demos/
%{_datadir}/%{name}/template/
%{_datadir}/applications
%{_datadir}/mime/packages/kicad*.xml
%{_datadir}/%{name}/plugins
%{_datadir}/%{name}/scripting
%{_libdir}/%{name}
%{_datadir}/appdata/*.xml
%{py2_puresitedir}/*
%{_libdir}/*.so*

%files doc
%doc %{_datadir}/doc/%{name}

%files library
%{_datadir}/%{name}/modules
%{_datadir}/%{name}/library
