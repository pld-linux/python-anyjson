#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	anyjson
Summary:	JSON implementation in a common interface
Name:		python-%{module}
Version:	0.3.3
Release:	2
License:	BSD
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/a/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	2ea28d6ec311aeeebaf993cb3008b27c
URL:		https://bitbucket.org/runeh/anyjson
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.612
%if %{with python2}
%{?with_tests:BuildRequires: python-nose}
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-setuptools
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Anyjson loads whichever is the fastest JSON module installed and
provides a uniform API regardless of which JSON implementation is
used.

%package -n python3-%{module}
Summary:	JSON implementation in a common interface
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
Anyjson loads whichever is the fastest JSON module installed and
provides a uniform API regardless of which JSON implementation is
used.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build # %{?with_tests:test}
%endif


%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG README
%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-*.egg-info
%endif

%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGELOG README
%{py3_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py3_sitescriptdir}/%{module}-*.egg-info
%endif
