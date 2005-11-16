Summary:	Io programming language
Summary(pl):	Jêzyk programowania Io
Name:		io
Version:	20051017
Release:	1
License:	BSD
Group:		Development/Languages
Source0:	http://www.sigusr1.org/~steve/IoFull-2005-10-17.tar.gz
# Source0-md5:	ae8e1b57a441311bb304f8b3a477ca90
URL:		http://www.iolanguage.com/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Io programming language.

%description -l pl
Jêzyk programowania Io.

%prep
%setup -q -c 

%build
cd release/IoFull-2005-10-17
rm vm/base/DynLib_OSX.{c,h}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO
