%define	Werror_cflags	%nil
%define	debug_package	%nil
%define _disable_lto 1
%define date %nil

# Use ./update.sh to generate latest tarballs and the corresponding
# specfile fragment

%define	name kicad
%define	version 4.0.5

%define	docname kicad-doc

%define	libname kicad-library

%define i18nname kicad-i18n

Name:		%{name}
Summary:	An open source program for the creation of electronic schematic diagrams
Epoch:		1
Version:	%{version}
Release:	0.1
# git clone https://github.com/KiCad/kicad-source-mirror.git
# pushd kicad-source-mirror
# git archive --format=tar --prefix %{name}-%{version}-$(date +%Y%m%d)/ HEAD | xz -vf > ../%{name}-%{version}-$(date +%Y%m%d).tar.xz
# popd
Source0:	%{name}-%{version}.tar.xz
Source1:	%{docname}-%{version}.tar.gz
Source2:	%{libname}-%{version}.tar.gz
Source3:	%{i18nname}-%{version}.tar.gz
Source4:	get_kicad.sh
Source100:	kicad.rpmlintrc
License:	GPLv2+
Group:		Sciences/Computer science
Url:		http://www.kicad-pcb.org
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
BuildRequires:	curl-devel

BuildRequires:	desktop-file-utils
BuildRequires:	po4a
BuildRequires:	asciidoc
BuildRequires:	dblatex
BuildRequires:	perl(Unicode::GCString)
Requires:	%{libname}
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
%setup -q -T -b 2 -n %{libname}-%{version}
%setup -q -T -b 3 -n %{i18nname}-%{version}
cd ..

# proper libname policy
pushd %{name}-%{version}
sed -i "s|KICAD_PLUGINS lib/kicad/plugins|KICAD_PLUGINS %{_lib}/kicad/plugins|g" CMakeLists.txt
# KICAD_LIB ${CMAKE_INSTALL_PREFIX}/lib
sed -i "s!CMAKE_INSTALL_PREFIX}/lib!CMAKE_INSTALL_PREFIX}/%{_lib}!g" CMakeLists.txt
popd

%build
%setup_compile_flags
export LC_ALL=C
cd ../

# Building kicad-doc
pushd %{docname}-%{version}
	%cmake \
		-DKICAD_STABLE_VERSION:BOOL=ON \
		-DKICAD_wxUSE_UNICODE=ON \
		-DCMAKE_BUILD_TYPE=Release \
		-DBUILD_FORMATS=html
	%make
popd

# Building kicad-library
pushd %{libname}-%{version}
	%cmake \
		-DKICAD_STABLE_VERSION:BOOL=ON \
		-DCMAKE_BUILD_TYPE=Release
	%make
popd

# Building kicad
pushd %{name}-%{version}

	%cmake \
		-DBUILD_SHARED_LIBS:BOOL=OFF \
		-DKICAD_STABLE_VERSION:BOOL=ON \
		-DKICAD_wxUSE_UNICODE=ON \
		-DCMAKE_BUILD_TYPE=Release \
		-DKICAD_SKIP_BOOST=ON \
		-DKICAD_REPO_NAME=stable \
		-DBUILD_GITHUB_PLUGIN=ON

	#ugly workaround to fix build
	#dunno what causes the extra ; in CXX_FLAGS which causes the failure
	find . -name flags.make -exec sed -i -e 's,-pthread;-fpermissive,-pthread -fpermissive,g' {} \;
	find . -name link.txt -exec sed -i -e 's,-pthread;-fpermissive,-pthread -fpermissive,g' {} \;

	%make
popd


# Building kicad-i18n
pushd %{i18nname}-%{version}
	%cmake \
		-DKICAD_STABLE_VERSION:BOOL=ON \
		-DCMAKE_BUILD_TYPE=Release \
		-DKICAD_I18N_UNIX_STRICT_PATH=ON
	%make
popd

%install
cd ../

# Installing kicad-doc
pushd %{docname}-%{version}
	make -C build DESTDIR=%buildroot install
popd

# Installing kicad-library
pushd %{libname}-%{version}
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

	# create icons
	mkdir -p %{buildroot}%{_miconsdir} %{buildroot}%{_iconsdir} %{buildroot}%{_liconsdir}
	convert -resize 16x16 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg %{buildroot}%{_miconsdir}/%{name}.png
	convert -resize 32x32 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg %{buildroot}%{_iconsdir}/%{name}.png
	convert -resize 48x48 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg %{buildroot}%{_liconsdir}/%{name}.png
popd

%files -f %{name}.lang
%{_bindir}/*
%{_libdir}/%{name}/plugins/*.xsl
%{_iconsdir}/*/*/*
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/%{name}/demos/
%{_datadir}/%{name}/template/
%{_datadir}/applications
%{_datadir}/mime/packages/kicad.xml
%{_datadir}/mimelnk/application/*.desktop

%files doc
%doc %{_datadir}/doc/%{name}

%files library
%{_datadir}/%{name}/library
%{_datadir}/%{name}/modules
