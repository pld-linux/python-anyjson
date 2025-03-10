#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	anyjson
Summary:	JSON implementation in a common interface
Summary(pl.UTF-8):	Implementacja JSON we wspólnym interfejsie
Name:		python-%{module}
Version:	0.3.3
Release:	11
License:	BSD
Group:		Development/Languages/Python
Source0:	https://files.pythonhosted.org/packages/source/a/anyjson/%{module}-%{version}.tar.gz
# Source0-md5:	2ea28d6ec311aeeebaf993cb3008b27c
# use six instead of 2to3 (which is no longer supported by python3 setuptools)
Patch0:		anyjson-python3.patch
Patch1:		anyjson-do-not-use-2to3.patch
# raise priority of cjson and drop the 'deprecation' warning (it's about as
# alive as half the others), drop jsonlib, jsonlib2 and django.utils.simplejson
# (which are more dead)
Patch2:		%{name}-update-order.patch
URL:		https://pypi.org/project/anyjson/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.4
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-nose
BuildRequires:	python-six
%endif
%endif
%if %{with python3}
BuildRequires:	python3-2to3 >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-nose
BuildRequires:	python3-six
%endif
%endif
Requires:	python-modules >= 1:2.4
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Anyjson loads whichever is the fastest JSON module installed and
provides a uniform API regardless of which JSON implementation is
used.

%description -l pl.UTF-8
Anyjson ładuje najszybszy moduł JSON, jaki jest zainstalowany i
udostępnia jednolite API, niezależnie od używanej implementacji JSON.

%package -n python3-%{module}
Summary:	JSON implementation in a common interface
Summary(pl.UTF-8):	Implementacja JSON we wspólnym interfejsie
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-%{module}
Anyjson loads whichever is the fastest JSON module installed and
provides a uniform API regardless of which JSON implementation is
used.

%description -n python3-%{module} -l pl.UTF-8
Anyjson ładuje najszybszy moduł JSON, jaki jest zainstalowany i
udostępnia jednolite API, niezależnie od używanej implementacji JSON.

%prep
%setup -q -n %{module}-%{version}
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build

%if %{with tests}
# tests must be run using 2to3'd sources
cd build-3/lib
%{__python3} -m nose ../../tests
cd ../..
%endif
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

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE README
%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE README
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
