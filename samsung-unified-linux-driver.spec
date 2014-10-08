# TODO:
#	- consider arm arch
#
# Conditional build:
%bcond_with	license_agreement	# generates package

%define		shortname	samsung-unified
%define		base_name	samsung-unified-linux-driver
%define		rel	0.2
Summary:	Samsung Unified Linux Driver
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
Version:	1.00.27.04
Release:	%{rel}%{?with_license_agreement:wla}
License:	non-distributable
Group:		Applications
%if %{with license_agreement}
Source0:	http://downloadcenter.samsung.com/content/DR/201407/20140709160646372/ULD_V%{version}.tar.gz
# NoSource0-md5:	5be0d4cc76cd204c02e89bd3799683bf
NoSource:	0
%else
Source1:	http://svn.pld-linux.org/svn/license-installer/license-installer.sh
# Source3-md5:	329c25f457fea66ec502b7ef70cb9ede
%endif
%if %{with license_agreement}
BuildRequires:	rpmbuild(macros) >= 1.357
BuildRequires:	sed >= 4.0
BuildRequires:	cups-devel
%else
Requires:	rpm-build-tools >= 4.4.37
Requires:	rpmbuild(macros) >= 1.544
%endif
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Epoch:		1

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
%define		_enable_debug_packages	0

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
Requires:	sane-backend

%description -n sane-driver-%{shortname}
SANE part of Samsung Unified Linux Driver

%prep
%if %{with license_agreement}
%setup -q -n uld

%build
test -d %{drvarch}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{without license_agreement}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{base_name}}

sed -e '
	s/@BASE_NAME@/%{base_name}/g
	s/@TARGET_CPU@/%{_target_cpu}/g
	s-@VERSION@-%{version}-g
	s-@RELEASE@-%{release}-g
	s,@SPECFILE@,%{_datadir}/%{base_name}/%{base_name}.spec,g
	s,@DATADIR@,%{_datadir}/%{base_name},g
' %{SOURCE1} > $RPM_BUILD_ROOT%{_bindir}/%{base_name}.install

cp -p %{_specdir}/%{base_name}.spec $RPM_BUILD_ROOT%{_datadir}/%{base_name}
%else
install -d \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_sysconfdir}/sane.d/ \
	$RPM_BUILD_ROOT%{_sanelibdir} \
	$RPM_BUILD_ROOT%{_cupsfilterdir} \
	$RPM_BUILD_ROOT%{_cupsppddir}/samsung/cms/
install \
	noarch/%{_sysconfdir}/smfp.conf \
	$RPM_BUILD_ROOT%{_sysconfdir}/sane.d/
install \
	noarch/share/ppd/*.ppd \
	$RPM_BUILD_ROOT%{_cupsppddir}/samsung/
install \
	noarch/share/ppd/cms/* \
	$RPM_BUILD_ROOT%{_cupsppddir}/samsung/cms/
install \
	%{drvarch}/libscmssc.so \
	$RPM_BUILD_ROOT%{_libdir}
#ln -s libmfp.so.1.0.1 $RPM_BUILD_ROOT%{_libdir}/libmfp.so.1
#ln -s libmfp.so.1 $RPM_BUILD_ROOT%{_libdir}/libmfp.so
install \
	%{drvarch}/{pstosecps,rastertospl} \
	$RPM_BUILD_ROOT%{_cupsfilterdir}
install \
	%{drvarch}/libsane-smfp* \
	$RPM_BUILD_ROOT%{_sanelibdir}
install \
	%{drvarch}/smfpnetdiscovery \
	$RPM_BUILD_ROOT%{_bindir}
%{__cp} noarch/license/eula.txt eula.txt
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%if %{without license_agreement}
%attr(755,root,root) %{_bindir}/%{base_name}.install
%{_datadir}/%{base_name}
%else
%doc eula.txt
%attr(755,root,root) %{_libdir}/libscmssc.so
%endif

%if %{with license_agreement}
%files -n cups-driver-%{shortname}
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/smfpnetdiscovery
%attr(755,root,root) %{_cupsfilterdir}/*
%dir %{_cupsppddir}/samsung/
%{_cupsppddir}/samsung/*.ppd
%dir %{_cupsppddir}/samsung/cms
%{_cupsppddir}/samsung/cms/*

%files -n sane-driver-%{shortname}
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(755,root,root) %{_sanelibdir}/libsane-smfp*
%endif
