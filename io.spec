#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_without	tests		# build without tests
#
Summary:	Io programming language
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
Io programming language

%prep
%setup -q -c 

%build
cd release/IoFull-2005-10-17/
rm vm/base/DynLib_OSX.{c,h}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
#install -d $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO
