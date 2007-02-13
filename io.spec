Summary:	Io programming language
Summary(pl.UTF-8):	Język programowania Io
Name:		io
Version:	20061207
Release:	1
License:	BSD
Group:		Development/Languages
Source0:	http://www.sigusr1.org/~steve/Io-2006-12-07.tar.gz
# Source0-md5:	077588a5177f3ed65744dc1db7325370
URL:		http://www.iolanguage.com/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-glut-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	freetype-devel
BuildRequires:	glfw-devel
BuildRequires:	gmp-devel
BuildRequires:	gnustep-gui-devel >= 0.11.0
BuildRequires:	libdbi-devel
BuildRequires:	libevent-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libsgml-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libtiff-devel
BuildRequires:	libxml2-devel
BuildRequires:	pcre-devel
#BuildRequires:	portaudio-devel >= 18 < 19
BuildRequires:	postgresql-devel
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	sed >= 4.0
BuildRequires:	soundtouch-devel >= 1.3.0
BuildRequires:	sqlite-devel >= 2.0
BuildRequires:	sqlite3-devel >= 3.0
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	taglib-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Io programming language.

%description -l pl.UTF-8
Język programowania Io.

%package static
Summary:	Static io library
Summary(pl.UTF-8):	Statyczna biblioteka języka io
Group:		Development/Libraries

%description static
Static io library.

%description static -l pl.UTF-8
Statyczna biblioteka języka io.

%prep
%setup -q -n Io-2006-12-07

sed -i -e 's,"-Os -g,"%{rpmcflags},' build/Project.io
sed -i -e 's,ncurses\.h,ncurses/ncurses.h,' addons/Curses/build.io addons/Curses/source/IoCurses.c
# disable, not ported to v19 yet(?)
sed -i -e 's,portaudio.h,portaudio18.h,' addons/PortAudio/build.io
# version check is PLD-incompatible, enforce current version
sed -i -e 's/version = "2\.4"/version = "2.5"/' addons/Python/build.io

%build
%{__make} \
	INSTALL_PREFIX=%{_prefix} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_PREFIX=$RPM_BUILD_ROOT%{_prefix}

# nothing interesting
rm -f $RPM_BUILD_ROOT%{_bindir}/io_static $RPM_BUILD_ROOT%{_libdir}/io/addons/*/{Makefile,build.io}
# to examplesdir?
rm -rf $RPM_BUILD_ROOT%{_libdir}/io/addons/*/{samples,tests}
# shouldn't be needed(?)
rm -rf $RPM_BUILD_ROOT%{_libdir}/io/addons/*/{_build/{headers,lib,objs},source}
# darwin-only
rm -rf $RPM_BUILD_ROOT%{_libdir}/io/addons/AppleExtras
# kill empty dirs
rmdir --ignore-fail-on-non-empty $RPM_BUILD_ROOT%{_libdir}/io/addons/*/{io,resources}

# XXX: are addons/*/{depends,frameworks,protos} needed?

mv $RPM_BUILD_ROOT%{_libdir}/io/addons/OpenGL/docs OpenGL-docs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/guide.pdf docs/{guide.html,guide_files}  OpenGL-docs
%attr(755,root,root) %{_bindir}/io
%attr(755,root,root) %{_libdir}/libiovmall.so
%dir %{_libdir}/io
%dir %{_libdir}/io/addons
# TODO: split
# R: ffmpeg
%dir %{_libdir}/io/addons/AVCodec
%dir %{_libdir}/io/addons/AVCodec/_build
%dir %{_libdir}/io/addons/AVCodec/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/AVCodec/_build/dll/libIoAVCodec.so
%{_libdir}/io/addons/AVCodec/io
#
%dir %{_libdir}/io/addons/AsyncRequest
%dir %{_libdir}/io/addons/AsyncRequest/_build
%dir %{_libdir}/io/addons/AsyncRequest/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/AsyncRequest/_build/dll/libIoAsyncRequest.so
%{_libdir}/io/addons/AsyncRequest/io
# R: gmp
%dir %{_libdir}/io/addons/BigNum
%dir %{_libdir}/io/addons/BigNum/_build
%dir %{_libdir}/io/addons/BigNum/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/BigNum/_build/dll/libIoBigNum.so
%{_libdir}/io/addons/BigNum/io
#
%dir %{_libdir}/io/addons/Blowfish
%dir %{_libdir}/io/addons/Blowfish/_build
%dir %{_libdir}/io/addons/Blowfish/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Blowfish/_build/dll/libIoBlowfish.so
%{_libdir}/io/addons/Blowfish/io
#
%dir %{_libdir}/io/addons/CGI
%dir %{_libdir}/io/addons/CGI/_build
%dir %{_libdir}/io/addons/CGI/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/CGI/_build/dll/libIoCGI.so
%{_libdir}/io/addons/CGI/io
#
%dir %{_libdir}/io/addons/ContinuedFraction
%dir %{_libdir}/io/addons/ContinuedFraction/_build
%dir %{_libdir}/io/addons/ContinuedFraction/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/ContinuedFraction/_build/dll/libIoContinuedFraction.so
%{_libdir}/io/addons/ContinuedFraction/io
#
%dir %{_libdir}/io/addons/Contracts
%dir %{_libdir}/io/addons/Contracts/_build
%dir %{_libdir}/io/addons/Contracts/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Contracts/_build/dll/libIoContracts.so
%{_libdir}/io/addons/Contracts/io
# R: ncurses
%dir %{_libdir}/io/addons/Curses
%dir %{_libdir}/io/addons/Curses/_build
%dir %{_libdir}/io/addons/Curses/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Curses/_build/dll/libIoCurses.so
%{_libdir}/io/addons/Curses/io
# R: libdbi
%dir %{_libdir}/io/addons/DBI
%dir %{_libdir}/io/addons/DBI/_build
%dir %{_libdir}/io/addons/DBI/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/DBI/_build/dll/libIoDBI.so
%{_libdir}/io/addons/DBI/io
#
%dir %{_libdir}/io/addons/Flux
%dir %{_libdir}/io/addons/Flux/_build
%dir %{_libdir}/io/addons/Flux/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Flux/_build/dll/libIoFlux.so
%{_libdir}/io/addons/Flux/io
# XXX: use system fonts (Free UCS (http://savannah.nongnu.org/projects/freefont/), Vera)
%{_libdir}/io/addons/Flux/resources
#
%dir %{_libdir}/io/addons/Fnmatch
%dir %{_libdir}/io/addons/Fnmatch/_build
%dir %{_libdir}/io/addons/Fnmatch/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Fnmatch/_build/dll/libIoFnmatch.so
# R: OpenGL freetype
%dir %{_libdir}/io/addons/Font
%dir %{_libdir}/io/addons/Font/_build
%dir %{_libdir}/io/addons/Font/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Font/_build/dll/libIoFont.so
# R: glfw
%dir %{_libdir}/io/addons/GLFW
%dir %{_libdir}/io/addons/GLFW/_build
%dir %{_libdir}/io/addons/GLFW/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/GLFW/_build/dll/libIoGLFW.so
# R: OpenGL-GLU libjpeg libpng libtiff
%dir %{_libdir}/io/addons/Image
%dir %{_libdir}/io/addons/Image/_build
%dir %{_libdir}/io/addons/Image/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Image/_build/dll/libIoImage.so
#
%dir %{_libdir}/io/addons/LZO
%dir %{_libdir}/io/addons/LZO/_build
%dir %{_libdir}/io/addons/LZO/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/LZO/_build/dll/libIoLZO.so
%{_libdir}/io/addons/LZO/io
# R: libsndfile
%dir %{_libdir}/io/addons/LibSndFile
%dir %{_libdir}/io/addons/LibSndFile/_build
%dir %{_libdir}/io/addons/LibSndFile/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/LibSndFile/_build/dll/libIoLibSndFile.so
# R: libxml2
%dir %{_libdir}/io/addons/Libxml2
%dir %{_libdir}/io/addons/Libxml2/_build
%dir %{_libdir}/io/addons/Libxml2/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Libxml2/_build/dll/libIoLibxml2.so
%{_libdir}/io/addons/Libxml2/io
#
%dir %{_libdir}/io/addons/MD5
%dir %{_libdir}/io/addons/MD5/_build
%dir %{_libdir}/io/addons/MD5/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/MD5/_build/dll/libIoMD5.so
%{_libdir}/io/addons/MD5/io
# R: gnustep-gui
%dir %{_libdir}/io/addons/ObjcBridge
%dir %{_libdir}/io/addons/ObjcBridge/_build
%dir %{_libdir}/io/addons/ObjcBridge/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/ObjcBridge/_build/dll/libIoObjcBridge.so
%{_libdir}/io/addons/ObjcBridge/io
# R: OpenGL-GLU OpenGL-glut
%dir %{_libdir}/io/addons/OpenGL
%dir %{_libdir}/io/addons/OpenGL/_build
%dir %{_libdir}/io/addons/OpenGL/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/OpenGL/_build/dll/libIoOpenGL.so
%{_libdir}/io/addons/OpenGL/io
# R: portaudio
#%dir %{_libdir}/io/addons/PortAudio
#%dir %{_libdir}/io/addons/PortAudio/_build
#%dir %{_libdir}/io/addons/PortAudio/_build/dll
#%attr(755,root,root) %{_libdir}/io/addons/PortAudio/_build/dll/libIoPortAudio.so
#%{_libdir}/io/addons/PortAudio/io
# R: postgresql-libs
%dir %{_libdir}/io/addons/Postgres
%dir %{_libdir}/io/addons/Postgres/_build
%dir %{_libdir}/io/addons/Postgres/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Postgres/_build/dll/libIoPostgres.so
%{_libdir}/io/addons/Postgres/io
# R: python-libs
%dir %{_libdir}/io/addons/Python
%dir %{_libdir}/io/addons/Python/_build
%dir %{_libdir}/io/addons/Python/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Python/_build/dll/libIoPython.so
#
%dir %{_libdir}/io/addons/Random
%dir %{_libdir}/io/addons/Random/_build
%dir %{_libdir}/io/addons/Random/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Random/_build/dll/libIoRandom.so
#
%dir %{_libdir}/io/addons/Rational
%dir %{_libdir}/io/addons/Rational/_build
%dir %{_libdir}/io/addons/Rational/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Rational/_build/dll/libIoRational.so
%{_libdir}/io/addons/Rational/io
# R: pcre
%dir %{_libdir}/io/addons/Regex
%dir %{_libdir}/io/addons/Regex/_build
%dir %{_libdir}/io/addons/Regex/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Regex/_build/dll/libIoRegex.so
%{_libdir}/io/addons/Regex/io
# R: libsgml
%dir %{_libdir}/io/addons/SGML
%dir %{_libdir}/io/addons/SGML/_build
%dir %{_libdir}/io/addons/SGML/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/SGML/_build/dll/libIoSGML.so
%{_libdir}/io/addons/SGML/io
#
%dir %{_libdir}/io/addons/SHA1
%dir %{_libdir}/io/addons/SHA1/_build
%dir %{_libdir}/io/addons/SHA1/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/SHA1/_build/dll/libIoSHA1.so
%{_libdir}/io/addons/SHA1/io
# R: sqlite
%dir %{_libdir}/io/addons/SQLite
%dir %{_libdir}/io/addons/SQLite/_build
%dir %{_libdir}/io/addons/SQLite/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/SQLite/_build/dll/libIoSQLite.so
%{_libdir}/io/addons/SQLite/io
# R: sqlite3
%dir %{_libdir}/io/addons/SQLite3
%dir %{_libdir}/io/addons/SQLite3/_build
%dir %{_libdir}/io/addons/SQLite3/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/SQLite3/_build/dll/libIoSQLite3.so
%{_libdir}/io/addons/SQLite3/io
# R: libsamplerate
%dir %{_libdir}/io/addons/SampleRateConverter
%dir %{_libdir}/io/addons/SampleRateConverter/_build
%dir %{_libdir}/io/addons/SampleRateConverter/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/SampleRateConverter/_build/dll/libIoSampleRateConverter.so
#
%dir %{_libdir}/io/addons/SkipDB
%dir %{_libdir}/io/addons/SkipDB/_build
%dir %{_libdir}/io/addons/SkipDB/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/SkipDB/_build/dll/libIoSkipDB.so
# R: libevent
%dir %{_libdir}/io/addons/Socket
%dir %{_libdir}/io/addons/Socket/_build
%dir %{_libdir}/io/addons/Socket/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Socket/_build/dll/libIoSocket.so
%{_libdir}/io/addons/Socket/io
# R: soundtouch
%dir %{_libdir}/io/addons/SoundTouch
%dir %{_libdir}/io/addons/SoundTouch/_build
%dir %{_libdir}/io/addons/SoundTouch/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/SoundTouch/_build/dll/libIoSoundTouch.so
#
%dir %{_libdir}/io/addons/Syslog
%dir %{_libdir}/io/addons/Syslog/_build
%dir %{_libdir}/io/addons/Syslog/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Syslog/_build/dll/libIoSyslog.so
#
%dir %{_libdir}/io/addons/SystemCall
%dir %{_libdir}/io/addons/SystemCall/_build
%dir %{_libdir}/io/addons/SystemCall/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/SystemCall/_build/dll/libIoSystemCall.so
%{_libdir}/io/addons/SystemCall/io
# R: taglib
%dir %{_libdir}/io/addons/TagLib
%dir %{_libdir}/io/addons/TagLib/_build
%dir %{_libdir}/io/addons/TagLib/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/TagLib/_build/dll/libIoTagLib.so
#
%dir %{_libdir}/io/addons/Thread
%dir %{_libdir}/io/addons/Thread/_build
%dir %{_libdir}/io/addons/Thread/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Thread/_build/dll/libIoThread.so
#
%dir %{_libdir}/io/addons/Thunder
%dir %{_libdir}/io/addons/Thunder/_build
%dir %{_libdir}/io/addons/Thunder/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Thunder/_build/dll/libIoThunder.so
%{_libdir}/io/addons/Thunder/io
#
%dir %{_libdir}/io/addons/User
%dir %{_libdir}/io/addons/User/_build
%dir %{_libdir}/io/addons/User/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/User/_build/dll/libIoUser.so
#
%dir %{_libdir}/io/addons/Vector
%dir %{_libdir}/io/addons/Vector/_build
%dir %{_libdir}/io/addons/Vector/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Vector/_build/dll/libIoVector.so
%{_libdir}/io/addons/Vector/io
# R: zlib
%dir %{_libdir}/io/addons/Zlib
%dir %{_libdir}/io/addons/Zlib/_build
%dir %{_libdir}/io/addons/Zlib/_build/dll
%attr(755,root,root) %{_libdir}/io/addons/Zlib/_build/dll/libIoZlib.so
%{_libdir}/io/addons/Zlib/io

%files static
%defattr(644,root,root,755)
%{_libdir}/libiovmall.a
