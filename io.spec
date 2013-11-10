#
# Conditional build
%bcond_with	glfw	# GLFW addon (not ready for glfw 3)
#
Summary:	Io programming language
Summary(pl.UTF-8):	Język programowania Io
Name:		io
Version:	20110912
Release:	1
License:	BSD
Group:		Development/Languages
Source0:	https://github.com/stevedekorte/io/archive/2011.09.12/%{name}-%{version}.tar.gz
# Source0-md5:	880b2d4b41cdfbeb7e8e3fe35e475739
Patch0:		%{name}-link.patch
Patch1:		%{name}-memcached.patch
Patch2:		%{name}-system-libsgml.patch
Patch3:		%{name}-theora.patch
Patch4:		%{name}-addons.patch
Patch5:		%{name}-ode.patch
Patch6:		%{name}-python.patch
URL:		http://iolanguage.org/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-glut-devel
BuildRequires:	cairo-devel
#BuildRequires:	ffmpeg-devel
BuildRequires:	freetype-devel >= 2
%{?with_glfw:BuildRequires:	glfw-devel < 3}
BuildRequires:	gmp-devel
#BuildRequires:	gnustep-gui-devel >= 0.11.0
BuildRequires:	libdbi-devel
BuildRequires:	libedit-devel
BuildRequires:	libevent-devel
BuildRequires:	libffi-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libmemcached-devel >= 1.0.17
BuildRequires:	libogg-devel
BuildRequires:	libpng-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libsgml-devel >= 1.1.4
BuildRequires:	libsndfile-devel
BuildRequires:	libtheora-devel
BuildRequires:	libtiff-devel
BuildRequires:	libuuid-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libxml2-devel >= 2
BuildRequires:	loudmouth-devel
BuildRequires:	lzo-devel
BuildRequires:	mysql-devel
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	ode-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
#BuildRequires:	portaudio-devel >= 18 < 19
BuildRequires:	postgresql-devel
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	qdbm-devel
BuildRequires:	readline-devel
BuildRequires:	sed >= 4.0
#BuildRequires:	soundtouch-devel >= 1.3.0
#BuildRequires:	sqlite-devel >= 2.0
BuildRequires:	sqlite3-devel >= 3.0
BuildRequires:	taglib-devel
BuildRequires:	tokyocabinet-devel
BuildRequires:	yajl-devel
BuildRequires:	zlib-devel
Obsoletes:	io-static
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Io programming language.

%description -l pl.UTF-8
Język programowania Io.

%prep
%setup -q -n io-2011.09.12
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%{__sed} -i -e 's,DESTINATION lib\>,DESTINATION lib${LIB_SUFFIX},' \
	libs/*/CMakeLists.txt \
	addons/*/CMakeLists.txt

%build
install -d build
cd build
%cmake .. \
	-DCURSES_INCLUDE_PATH=/usr/include/ncurses

# build is racy wrt. io_static
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# nothing interesting
%{__rm} $RPM_BUILD_ROOT%{_bindir}/io_static
# to examplesdir?
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/io/addons/*/{samples,tests}
# shouldn't be needed(?)
%{__rm} $RPM_BUILD_ROOT%{_libdir}/io/addons/*/CMakeLists.txt
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/io/addons/*/{_build/{headers,lib,objs},source}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/io/addons/TokyoCabinet/test.db
%{__rm} $RPM_BUILD_ROOT%{_libdir}/io/addons/Yajl/test.io
# kill empty dirs
rmdir --ignore-fail-on-non-empty $RPM_BUILD_ROOT%{_libdir}/io/addons/*/_build/binaries

# XXX: are addons/*/{depends,frameworks,protos} needed?

# addon docs
%{__mv} $RPM_BUILD_ROOT%{_libdir}/io/addons/CFFI/README docs/README.CFFI
%{__mv} $RPM_BUILD_ROOT%{_libdir}/io/addons/HttpClient/README docs/README.HttpClient
%{__mv} $RPM_BUILD_ROOT%{_libdir}/io/addons/HttpClient/TODO docs/TODO.HttpClient
%{__mv} $RPM_BUILD_ROOT%{_libdir}/io/addons/Volcano/README docs/README.Volcano

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md docs/*
%attr(755,root,root) %{_bindir}/io
%attr(755,root,root) %{_libdir}/libbasekit.so
%attr(755,root,root) %{_libdir}/libcoroutine.so
%attr(755,root,root) %{_libdir}/libgarbagecollector.so
%attr(755,root,root) %{_libdir}/libiovmall.so
%dir %{_libdir}/io
%dir %{_libdir}/io/addons

# TODO: split (deps based?)

# R: ffmpeg [disabled as broken in addons/CMakeLists.txt]
%if %{with ffmpeg}
%dir %{_libdir}/io/addons/AVCodec
%dir %{_libdir}/io/addons/AVCodec/_build
%dir %{_libdir}/io/addons/AVCodec/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/AVCodec/_build/dll/libIoAVCodec.so
%{_libdir}/io/addons/AVCodec/io
%endif

%dir %{_libdir}/io/addons/AsyncRequest
%dir %{_libdir}/io/addons/AsyncRequest/_build
%dir %{_libdir}/io/addons/AsyncRequest/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/AsyncRequest/_build/dll/libIoAsyncRequest.so
%{_libdir}/io/addons/AsyncRequest/io
%{_libdir}/io/addons/AsyncRequest/depends
%{_libdir}/io/addons/AsyncRequest/protos

# R: gmp
%dir %{_libdir}/io/addons/BigNum
%dir %{_libdir}/io/addons/BigNum/_build
%dir %{_libdir}/io/addons/BigNum/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/BigNum/_build/dll/libIoBigNum.so
%{_libdir}/io/addons/BigNum/io
%{_libdir}/io/addons/BigNum/depends
%{_libdir}/io/addons/BigNum/protos

%dir %{_libdir}/io/addons/Bitly
%dir %{_libdir}/io/addons/Bitly/_build
%dir %{_libdir}/io/addons/Bitly/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Bitly/_build/dll/libIoBitly.so
%{_libdir}/io/addons/Bitly/io
%{_libdir}/io/addons/Bitly/depends
%{_libdir}/io/addons/Bitly/protos

%dir %{_libdir}/io/addons/Blowfish
%dir %{_libdir}/io/addons/Blowfish/_build
%dir %{_libdir}/io/addons/Blowfish/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Blowfish/_build/dll/libIoBlowfish.so
%{_libdir}/io/addons/Blowfish/io
%{_libdir}/io/addons/Blowfish/depends
%{_libdir}/io/addons/Blowfish/protos

%dir %{_libdir}/io/addons/Box
%dir %{_libdir}/io/addons/Box/_build
%dir %{_libdir}/io/addons/Box/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Box/_build/dll/libIoBox.so
%{_libdir}/io/addons/Box/io
%{_libdir}/io/addons/Box/depends
%{_libdir}/io/addons/Box/frameworks
%{_libdir}/io/addons/Box/protos

# R: libffi
%dir %{_libdir}/io/addons/CFFI
%dir %{_libdir}/io/addons/CFFI/_build
%dir %{_libdir}/io/addons/CFFI/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/CFFI/_build/dll/libIoCFFI.so
%{_libdir}/io/addons/CFFI/io
%{_libdir}/io/addons/CFFI/depends
%{_libdir}/io/addons/CFFI/protos

%dir %{_libdir}/io/addons/CGI
%dir %{_libdir}/io/addons/CGI/_build
%dir %{_libdir}/io/addons/CGI/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/CGI/_build/dll/libIoCGI.so
%{_libdir}/io/addons/CGI/io
%{_libdir}/io/addons/CGI/depends
%{_libdir}/io/addons/CGI/protos

# R: cairo
%dir %{_libdir}/io/addons/Cairo
%dir %{_libdir}/io/addons/Cairo/_build
%dir %{_libdir}/io/addons/Cairo/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Cairo/_build/dll/libIoCairo.so
%{_libdir}/io/addons/Cairo/io
%{_libdir}/io/addons/Cairo/depends
%{_libdir}/io/addons/Cairo/protos

# TODO: Clutter (nothing is built???)
# R: clutter atk glib2 pango cairo

%dir %{_libdir}/io/addons/ContinuedFraction
%dir %{_libdir}/io/addons/ContinuedFraction/_build
%dir %{_libdir}/io/addons/ContinuedFraction/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/ContinuedFraction/_build/dll/libIoContinuedFraction.so
%{_libdir}/io/addons/ContinuedFraction/io
%{_libdir}/io/addons/ContinuedFraction/depends
%{_libdir}/io/addons/ContinuedFraction/protos

# R: ncurses
%dir %{_libdir}/io/addons/Curses
%dir %{_libdir}/io/addons/Curses/_build
%dir %{_libdir}/io/addons/Curses/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Curses/_build/dll/libIoCurses.so
%{_libdir}/io/addons/Curses/io
%{_libdir}/io/addons/Curses/depends
%{_libdir}/io/addons/Curses/protos

# R: libdbi
%dir %{_libdir}/io/addons/DBI
%dir %{_libdir}/io/addons/DBI/_build
%dir %{_libdir}/io/addons/DBI/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/DBI/_build/dll/libIoDBI.so
%{_libdir}/io/addons/DBI/io
%{_libdir}/io/addons/DBI/depends
%{_libdir}/io/addons/DBI/protos

# R(addons): Socket
%dir %{_libdir}/io/addons/DistributedObjects
%dir %{_libdir}/io/addons/DistributedObjects/_build
%dir %{_libdir}/io/addons/DistributedObjects/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/DistributedObjects/_build/dll/libIoDistributedObjects.so
%{_libdir}/io/addons/DistributedObjects/io
%{_libdir}/io/addons/DistributedObjects/depends
%{_libdir}/io/addons/DistributedObjects/protos

# R: libedit
%dir %{_libdir}/io/addons/EditLine
%dir %{_libdir}/io/addons/EditLine/_build
%dir %{_libdir}/io/addons/EditLine/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/EditLine/_build/dll/libIoEditLine.so
%{_libdir}/io/addons/EditLine/depends
%{_libdir}/io/addons/EditLine/protos

%dir %{_libdir}/io/addons/Facebook
%dir %{_libdir}/io/addons/Facebook/_build
%dir %{_libdir}/io/addons/Facebook/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Facebook/_build/dll/libIoFacebook.so
%{_libdir}/io/addons/Facebook/io
%{_libdir}/io/addons/Facebook/depends
%{_libdir}/io/addons/Facebook/protos

# R(addons): OpenGL
%dir %{_libdir}/io/addons/Flux
%dir %{_libdir}/io/addons/Flux/_build
%dir %{_libdir}/io/addons/Flux/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Flux/_build/dll/libIoFlux.so
%{_libdir}/io/addons/Flux/io
# XXX: use system fonts:
# - Free UCS (http://savannah.nongnu.org/projects/freefont/)
# - ProFont (http://www.tobiasjung.net/profont/ ?)
# - Adobe T207
# - Vera
%{_libdir}/io/addons/Flux/resources
%{_libdir}/io/addons/Flux/depends
%{_libdir}/io/addons/Flux/protos

%dir %{_libdir}/io/addons/Fnmatch
%dir %{_libdir}/io/addons/Fnmatch/_build
%dir %{_libdir}/io/addons/Fnmatch/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Fnmatch/_build/dll/libIoFnmatch.so
%{_libdir}/io/addons/Fnmatch/depends

# R: OpenGL freetype
%dir %{_libdir}/io/addons/Font
%dir %{_libdir}/io/addons/Font/_build
%dir %{_libdir}/io/addons/Font/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Font/_build/dll/libIoFont.so
%{_libdir}/io/addons/Font/depends
%{_libdir}/io/addons/Font/protos

# R: glfw OpenGL OpenGL-GLU OpenGL-glut; addons: OpenGL
%if %{with glfw}
%dir %{_libdir}/io/addons/GLFW
%dir %{_libdir}/io/addons/GLFW/_build
%dir %{_libdir}/io/addons/GLFW/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/GLFW/_build/dll/libIoGLFW.so
%endif

# R(addons): Socket SGML
%dir %{_libdir}/io/addons/GoogleSearch
%dir %{_libdir}/io/addons/GoogleSearch/_build
%dir %{_libdir}/io/addons/GoogleSearch/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/GoogleSearch/_build/dll/libIoGoogleSearch.so
%{_libdir}/io/addons/GoogleSearch/io
%{_libdir}/io/addons/GoogleSearch/depends
%{_libdir}/io/addons/GoogleSearch/protos

%dir %{_libdir}/io/addons/HttpClient
%dir %{_libdir}/io/addons/HttpClient/_build
%dir %{_libdir}/io/addons/HttpClient/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/HttpClient/_build/dll/libIoHttpClient.so
%{_libdir}/io/addons/HttpClient/io
%{_libdir}/io/addons/HttpClient/depends
%{_libdir}/io/addons/HttpClient/protos

# R: libjpeg libpng libtiff
%dir %{_libdir}/io/addons/Image
%dir %{_libdir}/io/addons/Image/_build
%dir %{_libdir}/io/addons/Image/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Image/_build/dll/libIoImage.so
%{_libdir}/io/addons/Image/io
%{_libdir}/io/addons/Image/depends
%{_libdir}/io/addons/Image/protos

# R: lzo
%dir %{_libdir}/io/addons/LZO
%dir %{_libdir}/io/addons/LZO/_build
%dir %{_libdir}/io/addons/LZO/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/LZO/_build/dll/libIoLZO.so
%{_libdir}/io/addons/LZO/io
%{_libdir}/io/addons/LZO/depends
%{_libdir}/io/addons/LZO/protos

# R: libsndfile
%dir %{_libdir}/io/addons/LibSndFile
%dir %{_libdir}/io/addons/LibSndFile/_build
%dir %{_libdir}/io/addons/LibSndFile/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/LibSndFile/_build/dll/libIoLibSndFile.so
%{_libdir}/io/addons/LibSndFile/io
%{_libdir}/io/addons/LibSndFile/depends
%{_libdir}/io/addons/LibSndFile/protos

# R: libxml2
%dir %{_libdir}/io/addons/Libxml2
%dir %{_libdir}/io/addons/Libxml2/_build
%dir %{_libdir}/io/addons/Libxml2/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Libxml2/_build/dll/libIoLibxml2.so
%{_libdir}/io/addons/Libxml2/io
%{_libdir}/io/addons/Libxml2/depends
%{_libdir}/io/addons/Libxml2/protos

%dir %{_libdir}/io/addons/Loki
%dir %{_libdir}/io/addons/Loki/_build
%dir %{_libdir}/io/addons/Loki/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Loki/_build/dll/libIoLoki.so
%{_libdir}/io/addons/Loki/io
%{_libdir}/io/addons/Loki/depends
%{_libdir}/io/addons/Loki/protos

# R: loudmouth; addons: SGML
%dir %{_libdir}/io/addons/Loudmouth
%dir %{_libdir}/io/addons/Loudmouth/_build
%dir %{_libdir}/io/addons/Loudmouth/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Loudmouth/_build/dll/libIoLoudmouth.so
%{_libdir}/io/addons/Loudmouth/io
%{_libdir}/io/addons/Loudmouth/depends
%{_libdir}/io/addons/Loudmouth/protos

%dir %{_libdir}/io/addons/MD5
%dir %{_libdir}/io/addons/MD5/_build
%dir %{_libdir}/io/addons/MD5/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/MD5/_build/dll/libIoMD5.so
%{_libdir}/io/addons/MD5/io
%{_libdir}/io/addons/MD5/depends
%{_libdir}/io/addons/MD5/protos

# R: libmemcached
%dir %{_libdir}/io/addons/Memcached
%dir %{_libdir}/io/addons/Memcached/_build
%dir %{_libdir}/io/addons/Memcached/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Memcached/_build/dll/libIoMemcached.so
%{_libdir}/io/addons/Memcached/io
%{_libdir}/io/addons/Memcached/depends
%{_libdir}/io/addons/Memcached/protos

# R: mysql-libs
%dir %{_libdir}/io/addons/MySQL
%dir %{_libdir}/io/addons/MySQL/_build
%dir %{_libdir}/io/addons/MySQL/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/MySQL/_build/dll/libIoMySQL.so
%{_libdir}/io/addons/MySQL/io
%{_libdir}/io/addons/MySQL/depends
%{_libdir}/io/addons/MySQL/protos

%dir %{_libdir}/io/addons/NotificationCenter
%dir %{_libdir}/io/addons/NotificationCenter/_build
%dir %{_libdir}/io/addons/NotificationCenter/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/NotificationCenter/_build/dll/libIoNotificationCenter.so
%{_libdir}/io/addons/NotificationCenter/io
%{_libdir}/io/addons/NotificationCenter/depends
%{_libdir}/io/addons/NotificationCenter/protos

# R: OpenGL ode; addons: OpenGL
%dir %{_libdir}/io/addons/ODE
%dir %{_libdir}/io/addons/ODE/_build
%dir %{_libdir}/io/addons/ODE/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/ODE/_build/dll/libIoODE.so
%{_libdir}/io/addons/ODE/io
%{_libdir}/io/addons/ODE/depends
%{_libdir}/io/addons/ODE/protos

# R: openssl
%dir %{_libdir}/io/addons/Oauth
%dir %{_libdir}/io/addons/Oauth/_build
%dir %{_libdir}/io/addons/Oauth/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Oauth/_build/dll/libIoOauth.so
%{_libdir}/io/addons/Oauth/io
%{_libdir}/io/addons/Oauth/depends
%{_libdir}/io/addons/Oauth/protos

# R: gnustep-gui; addons: Box,Socket,SystemCall [Darwin-specific now, was built on Linux in 2006]
%if 0
%dir %{_libdir}/io/addons/ObjcBridge
%dir %{_libdir}/io/addons/ObjcBridge/_build
%dir %{_libdir}/io/addons/ObjcBridge/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/ObjcBridge/_build/dll/libIoObjcBridge.so
%{_libdir}/io/addons/ObjcBridge/io
%endif

# R(addons): TokyoCabinet
%dir %{_libdir}/io/addons/Obsidian
%dir %{_libdir}/io/addons/Obsidian/_build
%dir %{_libdir}/io/addons/Obsidian/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Obsidian/_build/dll/libIoObsidian.so
%{_libdir}/io/addons/Obsidian/io
%{_libdir}/io/addons/Obsidian/depends
%{_libdir}/io/addons/Obsidian/protos

# R: libogg
%dir %{_libdir}/io/addons/Ogg
%dir %{_libdir}/io/addons/Ogg/_build
%dir %{_libdir}/io/addons/Ogg/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Ogg/_build/dll/libIoOgg.so
%{_libdir}/io/addons/Ogg/io
%{_libdir}/io/addons/Ogg/depends
%{_libdir}/io/addons/Ogg/protos

# R: OpenGL-GLU OpenGL-glut
%dir %{_libdir}/io/addons/OpenGL
%dir %{_libdir}/io/addons/OpenGL/_build
%dir %{_libdir}/io/addons/OpenGL/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/OpenGL/_build/dll/libIoOpenGL.so
%{_libdir}/io/addons/OpenGL/io
%{_libdir}/io/addons/OpenGL/depends
%{_libdir}/io/addons/OpenGL/protos

# R: portaudio [disabled in addons/CMakeLists.txt, no CMakeLists.txt file]
%if 0
%dir %{_libdir}/io/addons/PortAudio
%dir %{_libdir}/io/addons/PortAudio/_build
%dir %{_libdir}/io/addons/PortAudio/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/PortAudio/_build/dll/libIoPortAudio.so
%{_libdir}/io/addons/PortAudio/io
%endif

# R: postgresql-libs
%dir %{_libdir}/io/addons/PostgreSQL
%dir %{_libdir}/io/addons/PostgreSQL/_build
%dir %{_libdir}/io/addons/PostgreSQL/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/PostgreSQL/_build/dll/libIoPostgreSQL.so
%{_libdir}/io/addons/PostgreSQL/io
%{_libdir}/io/addons/PostgreSQL/depends
%{_libdir}/io/addons/PostgreSQL/protos

# R: python-libs
%dir %{_libdir}/io/addons/Python
%dir %{_libdir}/io/addons/Python/_build
%dir %{_libdir}/io/addons/Python/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Python/_build/dll/libIoPython.so
%{_libdir}/io/addons/Python/depends
%{_libdir}/io/addons/Python/protos

# R: qdbm
%dir %{_libdir}/io/addons/QDBM
%dir %{_libdir}/io/addons/QDBM/_build
%dir %{_libdir}/io/addons/QDBM/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/QDBM/_build/dll/libIoQDBM.so
%{_libdir}/io/addons/QDBM/io
%{_libdir}/io/addons/QDBM/depends
%{_libdir}/io/addons/QDBM/protos

%dir %{_libdir}/io/addons/Random
%dir %{_libdir}/io/addons/Random/_build
%dir %{_libdir}/io/addons/Random/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Random/_build/dll/libIoRandom.so
%{_libdir}/io/addons/Random/io
%{_libdir}/io/addons/Random/depends
%{_libdir}/io/addons/Random/protos

%dir %{_libdir}/io/addons/Range
%dir %{_libdir}/io/addons/Range/_build
%dir %{_libdir}/io/addons/Range/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Range/_build/dll/libIoRange.so
%{_libdir}/io/addons/Range/io
%{_libdir}/io/addons/Range/depends
%{_libdir}/io/addons/Range/protos

%dir %{_libdir}/io/addons/Rational
%dir %{_libdir}/io/addons/Rational/_build
%dir %{_libdir}/io/addons/Rational/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Rational/_build/dll/libIoRational.so
%{_libdir}/io/addons/Rational/io
%{_libdir}/io/addons/Rational/depends
%{_libdir}/io/addons/Rational/protos

# R: readline
%dir %{_libdir}/io/addons/ReadLine
%dir %{_libdir}/io/addons/ReadLine/_build
%dir %{_libdir}/io/addons/ReadLine/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/ReadLine/_build/dll/libIoReadLine.so
%{_libdir}/io/addons/ReadLine/depends
%{_libdir}/io/addons/ReadLine/protos

# R: pcre; addons: Range
%dir %{_libdir}/io/addons/Regex
%dir %{_libdir}/io/addons/Regex/_build
%dir %{_libdir}/io/addons/Regex/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Regex/_build/dll/libIoRegex.so
%{_libdir}/io/addons/Regex/io
%{_libdir}/io/addons/Regex/depends
%{_libdir}/io/addons/Regex/protos

# R: libsgml
%dir %{_libdir}/io/addons/SGML
%dir %{_libdir}/io/addons/SGML/_build
%dir %{_libdir}/io/addons/SGML/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/SGML/_build/dll/libIoSGML.so
%{_libdir}/io/addons/SGML/io
%{_libdir}/io/addons/SGML/depends
%{_libdir}/io/addons/SGML/protos

%dir %{_libdir}/io/addons/SHA1
%dir %{_libdir}/io/addons/SHA1/_build
%dir %{_libdir}/io/addons/SHA1/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/SHA1/_build/dll/libIoSHA1.so
%{_libdir}/io/addons/SHA1/io
%{_libdir}/io/addons/SHA1/depends
%{_libdir}/io/addons/SHA1/protos

# R: sqlite [deprecated, no CMakeLists.txt for addon]
%if 0
%dir %{_libdir}/io/addons/SQLite
%dir %{_libdir}/io/addons/SQLite/_build
%dir %{_libdir}/io/addons/SQLite/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/SQLite/_build/dll/libIoSQLite.so
%{_libdir}/io/addons/SQLite/io
%endif

# R: sqlite3
%dir %{_libdir}/io/addons/SQLite3
%dir %{_libdir}/io/addons/SQLite3/_build
%dir %{_libdir}/io/addons/SQLite3/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/SQLite3/_build/dll/libIoSQLite3.so
%{_libdir}/io/addons/SQLite3/io
%{_libdir}/io/addons/SQLite3/depends
%{_libdir}/io/addons/SQLite3/protos

# R: libsamplerate
%dir %{_libdir}/io/addons/SampleRateConverter
%dir %{_libdir}/io/addons/SampleRateConverter/_build
%dir %{_libdir}/io/addons/SampleRateConverter/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/SampleRateConverter/_build/dll/libIoSampleRateConverter.so
%{_libdir}/io/addons/SampleRateConverter/io
%{_libdir}/io/addons/SampleRateConverter/depends
%{_libdir}/io/addons/SampleRateConverter/protos

# TODO: SecureSocket (nothing is built???)
# R: openssl; addons: Socket

# disabled in addons/CMakeLists.txt, no CMakeLists.txt for addon
%if 0
%dir %{_libdir}/io/addons/SkipDB
%dir %{_libdir}/io/addons/SkipDB/_build
%dir %{_libdir}/io/addons/SkipDB/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/SkipDB/_build/dll/libIoSkipDB.so
%endif

# R: libevent
%dir %{_libdir}/io/addons/Socket
%dir %{_libdir}/io/addons/Socket/_build
%dir %{_libdir}/io/addons/Socket/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Socket/_build/dll/libIoSocket.so
%{_libdir}/io/addons/Socket/io
%{_libdir}/io/addons/Socket/depends
%{_libdir}/io/addons/Socket/protos

# R: soundtouch [no CMakeLists.txt for addon]
%if 0
%dir %{_libdir}/io/addons/SoundTouch
%dir %{_libdir}/io/addons/SoundTouch/_build
%dir %{_libdir}/io/addons/SoundTouch/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/SoundTouch/_build/dll/libIoSoundTouch.so
%endif

%dir %{_libdir}/io/addons/SqlDatabase
%dir %{_libdir}/io/addons/SqlDatabase/_build
%dir %{_libdir}/io/addons/SqlDatabase/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/SqlDatabase/_build/dll/libIoSqlDatabase.so
%{_libdir}/io/addons/SqlDatabase/io
%{_libdir}/io/addons/SqlDatabase/depends
%{_libdir}/io/addons/SqlDatabase/protos

%dir %{_libdir}/io/addons/Syslog
%dir %{_libdir}/io/addons/Syslog/_build
%dir %{_libdir}/io/addons/Syslog/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Syslog/_build/dll/libIoSyslog.so
%{_libdir}/io/addons/Syslog/depends
%{_libdir}/io/addons/Syslog/protos

%dir %{_libdir}/io/addons/SystemCall
%dir %{_libdir}/io/addons/SystemCall/_build
%dir %{_libdir}/io/addons/SystemCall/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/SystemCall/_build/dll/libIoSystemCall.so
%{_libdir}/io/addons/SystemCall/io
%{_libdir}/io/addons/SystemCall/depends
%{_libdir}/io/addons/SystemCall/protos

# TagDB - no CMakeLists.txt for addon

# R: taglib
%dir %{_libdir}/io/addons/TagLib
%dir %{_libdir}/io/addons/TagLib/_build
%dir %{_libdir}/io/addons/TagLib/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/TagLib/_build/dll/libIoTagLib.so
%{_libdir}/io/addons/TagLib/io
%{_libdir}/io/addons/TagLib/depends
%{_libdir}/io/addons/TagLib/protos

# R: libtheora; addons: Ogg
%dir %{_libdir}/io/addons/Theora
%dir %{_libdir}/io/addons/Theora/_build
%dir %{_libdir}/io/addons/Theora/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Theora/_build/dll/libIoTheora.so
%{_libdir}/io/addons/Theora/io
%{_libdir}/io/addons/Theora/depends
%{_libdir}/io/addons/Theora/protos

%dir %{_libdir}/io/addons/Thread
%dir %{_libdir}/io/addons/Thread/_build
%dir %{_libdir}/io/addons/Thread/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Thread/_build/dll/libIoThread.so
%{_libdir}/io/addons/Thread/depends
%{_libdir}/io/addons/Thread/protos

# R: tokyocabinet-libs
%dir %{_libdir}/io/addons/TokyoCabinet
%dir %{_libdir}/io/addons/TokyoCabinet/_build
%dir %{_libdir}/io/addons/TokyoCabinet/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/TokyoCabinet/_build/dll/libIoTokyoCabinet.so
%{_libdir}/io/addons/TokyoCabinet/io
%{_libdir}/io/addons/TokyoCabinet/depends
%{_libdir}/io/addons/TokyoCabinet/protos

%dir %{_libdir}/io/addons/Twitter
%dir %{_libdir}/io/addons/Twitter/_build
%dir %{_libdir}/io/addons/Twitter/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Twitter/_build/dll/libIoTwitter.so
%{_libdir}/io/addons/Twitter/io
%{_libdir}/io/addons/Twitter/depends
%{_libdir}/io/addons/Twitter/protos

# R: libuuid
%dir %{_libdir}/io/addons/UUID
%dir %{_libdir}/io/addons/UUID/_build
%dir %{_libdir}/io/addons/UUID/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/UUID/_build/dll/libIoUUID.so
%{_libdir}/io/addons/UUID/io
%{_libdir}/io/addons/UUID/depends
%{_libdir}/io/addons/UUID/protos

%dir %{_libdir}/io/addons/User
%dir %{_libdir}/io/addons/User/_build
%dir %{_libdir}/io/addons/User/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/User/_build/dll/libIoUser.so
%{_libdir}/io/addons/User/depends
%{_libdir}/io/addons/User/protos

# R(addons): Yajl,Socket
%dir %{_libdir}/io/addons/VertexDB
%dir %{_libdir}/io/addons/VertexDB/_build
%dir %{_libdir}/io/addons/VertexDB/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/VertexDB/_build/dll/libIoVertexDB.so
%{_libdir}/io/addons/VertexDB/io
%{_libdir}/io/addons/VertexDB/depends
%{_libdir}/io/addons/VertexDB/protos

%dir %{_libdir}/io/addons/Volcano
%dir %{_libdir}/io/addons/Volcano/_build
%dir %{_libdir}/io/addons/Volcano/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Volcano/_build/dll/libIoVolcano.so
%{_libdir}/io/addons/Volcano/io
%{_libdir}/io/addons/Volcano/depends
%{_libdir}/io/addons/Volcano/protos

# R: libvorbis; addons: Ogg
%dir %{_libdir}/io/addons/Vorbis
%dir %{_libdir}/io/addons/Vorbis/_build
%dir %{_libdir}/io/addons/Vorbis/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Vorbis/_build/dll/libIoVorbis.so
%{_libdir}/io/addons/Vorbis/io
%{_libdir}/io/addons/Vorbis/depends
%{_libdir}/io/addons/Vorbis/protos

# R: yajl
%dir %{_libdir}/io/addons/Yajl
%dir %{_libdir}/io/addons/Yajl/_build
%dir %{_libdir}/io/addons/Yajl/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Yajl/_build/dll/libIoYajl.so
%{_libdir}/io/addons/Yajl/io
%{_libdir}/io/addons/Yajl/depends
%{_libdir}/io/addons/Yajl/protos

# R: zlib
%dir %{_libdir}/io/addons/Zlib
%dir %{_libdir}/io/addons/Zlib/_build
%dir %{_libdir}/io/addons/Zlib/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Zlib/_build/dll/libIoZlib.so
%{_libdir}/io/addons/Zlib/io
%{_libdir}/io/addons/Zlib/depends
%{_libdir}/io/addons/Zlib/protos
