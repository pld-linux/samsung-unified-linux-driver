%define		shortname	samsung-unified
Summary:	Samsung Unified Linux Driver
Name:		samsung-unified-linux-driver
Version:	2.0.52
Release:	0.1
License:	other
Group:		Applications
Source0:	http://org.downloadcenter.samsung.com/downloadfile/ContentsFile.aspx?VPath=DR/200810/20081024151424062/UnifiedLinuxDriver.tar.gz
# Source0-md5:	ee5d4012a5a89bc647eaca0cf071b359
ExclusiveArch:	i386 i486 i586 i686 athlon %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch i386 i486 i586 i686 athlon
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

%package -n cups-driver-%{shortname}
Summary:	CUPS part of Samsung Unified Linux Driver
Group:		Applications
Requires:	%{name} = %{version}
Requires:	cups
Requires:	ghostscript

%description -n cups-driver-%{shortname}

%package -n sane-driver-%{shortname}
Summary:	SANE part of Samsung Unified Linux Driver
Group:		Applications
Requires:	%{name} = %{version}
Requires:	sane

%description -n sane-driver-%{shortname}

%prep
%setup -q -n cdroot

%build
cd Linux/%{drvarch}/at_root/%{_libdir}
ln -s libmfp.so.1.0.1 libmfp.so.1
ln -s libmfp.so.1 libmfp.so

%install
install -d \
	$RPM_BUILD_ROOT%{_sysconfdir}/sane.d/ \
	$RPM_BUILD_ROOT%{_sanelibdir} \
	$RPM_BUILD_ROOT%{_cupsfilterdir} \
	$RPM_BUILD_ROOT%{_cupsppddir}/samsung/cms/
install -m 0644 \
	Linux/noarch/at_root/%{_sysconfdir}/sane.d/smfp.conf \
	$RPM_BUILD_ROOT%{_sysconfdir}/sane.d/
install -m 0644 \
	Linux/noarch/at_opt/share/ppd/*.ppd \
	$RPM_BUILD_ROOT%{_cupsppddir}/samsung/
install -m 0644 \
	Linux/noarch/at_opt/share/ppd/cms/* \
	$RPM_BUILD_ROOT%{_cupsppddir}/samsung/cms/
install -m 0755 \
	Linux/%{drvarch}/at_root/%{_libdir}/libmfp* \
	$RPM_BUILD_ROOT%{_libdir}
install -m 0755 \
	Linux/%{drvarch}/at_root/usr/lib/cups/filter/* \
	$RPM_BUILD_ROOT%{_cupsfilterdir}
install -m 0755 \
	Linux/%{drvarch}/at_root/%{_sanelibdir}/libsane-smfp* \
	$RPM_BUILD_ROOT%{_sanelibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/libmfp*

%files -n cups-driver-%{shortname}
%defattr(644,root,root,755)
%attr(755,root,root) %{_cupsfilterdir}/*
%dir %{_cupsppddir}/samsung/
%{_cupsppddir}/samsung/*.ppd
%{_cupsppddir}/samsung/cms/*

%files -n sane-driver-%{shortname}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(755,root,root) %{_sanelibdir}/libsane-smfp*
