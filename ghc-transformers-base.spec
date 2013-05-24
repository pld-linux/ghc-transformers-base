%define		pkgname	transformers-base
Summary:	This package provides a straightforward port of monadLib's BaseM typeclass to transformers.
Name:		ghc-%{pkgname}
Version:	0.4.1
Release:	1
License:	BSD
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/transformers-base/%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	bd99282e2daae5eecd1c953b7b77c990
URL:		http://hackage.haskell.org/package/transformers-base/
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-transformers
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

%description
This package provides a straightforward port of monadLib's BaseM typeclass to transformers.

%package doc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu %{pkgname}
Group:		Documentation

%description doc
HTML documentation for %{pkgname}.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%{__rm} -rf $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
