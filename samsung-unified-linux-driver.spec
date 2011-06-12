
%define		shortname	samsung-unified
Summary:	Samsung Unified Linux Driver
Name:		samsung-unified-linux-driver
Version:	3.0.80
Release:	0.1
License:	other
Group:		Applications
Source0:	http://www.bchemnet.com/suldr/UnifiedLinuxDriver-3.00.80.tar.gz
# Source0-md5:	4bcf37e3c71a4f16424eb5f47e93420e
BuildRequires:	cups-devel
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{ix86}
%define	drvarch i386
%endif
%ifarch %{x8664}
%define drvarch x86_64
%endif
%define 	_cupsdatadir	%(cups-config --datadir 2>/dev/null)
%define 	_cupslibdir		%(cups-config --serverbin 2>/dev/null)
%define		_cupsppddir		%{_cupsdatadir}/model
%define 	_cupsfilterdir	%{_cupslibdir}/filter
%define		_sanelibdir		%{_libdir}/sane

%description
Samsung Unified Linux Driver

%package -n cups-driver-%{shortname}
Summary:	CUPS part of Samsung Unified Linux Driver
Group:		Applications
Requires:	%{name} = %{version}
Requires:	cups
Requires:	ghostscript

%description -n cups-driver-%{shortname}
CUPS part of Samsung Unified Linux Driver

%package -n sane-driver-%{shortname}
Summary:	SANE part of Samsung Unified Linux Driver
Group:		Applications
Requires:	%{name} = %{version}
Requires:	sane

%description -n sane-driver-%{shortname}
SANE part of Samsung Unified Linux Driver

%prep
%setup -q -n cdroot

%build
test -d Linux/%{drvarch}/at_root/%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT%{_sysconfdir}/sane.d/ \
	$RPM_BUILD_ROOT%{_sanelibdir} \
	$RPM_BUILD_ROOT%{_cupsfilterdir} \
	$RPM_BUILD_ROOT%{_cupsppddir}/samsung/cms/
install \
	Linux/noarch/at_root/%{_sysconfdir}/sane.d/smfp.conf \
	$RPM_BUILD_ROOT%{_sysconfdir}/sane.d/
install \
	Linux/noarch/at_opt/share/ppd/*.ppd \
	$RPM_BUILD_ROOT%{_cupsppddir}/samsung/
install \
	Linux/noarch/at_opt/share/ppd/cms/* \
	$RPM_BUILD_ROOT%{_cupsppddir}/samsung/cms/
install \
	Linux/%{drvarch}/at_root/%{_libdir}/libmfp* \
	$RPM_BUILD_ROOT%{_libdir}
ln -s libmfp.so.1.0.1 $RPM_BUILD_ROOT%{_libdir}/libmfp.so.1
ln -s libmfp.so.1 $RPM_BUILD_ROOT%{_libdir}/libmfp.so
install \
	Linux/%{drvarch}/at_root%{_libdir}/cups/filter/* \
	$RPM_BUILD_ROOT%{_cupsfilterdir}
install \
	Linux/%{drvarch}/at_root/%{_sanelibdir}/libsane-smfp* \
	$RPM_BUILD_ROOT%{_sanelibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmfp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmfp.so.?

%files -n cups-driver-%{shortname}
%defattr(644,root,root,755)
%attr(755,root,root) %{_cupsfilterdir}/*
%dir %{_cupsppddir}/samsung/
%{_cupsppddir}/samsung/*.ppd
%{_cupsppddir}/samsung/cms/*

%files -n sane-driver-%{shortname}
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(755,root,root) %{_sanelibdir}/libsane-smfp*
