%global _hardened_build 1

Name:		geoipupdate3
Version:	3.1.1
Release:	1%{?dist}
Summary:	Update GeoIP2 and GeoIP Legacy binary databases from MaxMind
License:	GPLv2
URL:		http://dev.maxmind.com/geoip/geoipupdate/
Source0:	http://github.com/maxmind/geoipupdate/releases/download/v%{version}/geoipupdate-%{version}.tar.gz
Source1:	geoipupdate3.cron
BuildRequires:	coreutils
BuildRequires:	gcc
BuildRequires:	libcurl-devel
BuildRequires:	make
BuildRequires:	zlib-devel
BuildRequires:	perl(strict)

%description
The GeoIP Update program performs automatic updates of GeoIP2 and GeoIP
Legacy binary databases.

%package cron
Summary:	Cron job to do weekly updates of GeoIP databases
BuildArch:	noarch
Requires:	%{name} = %{version}-%{release}
Requires:	crontabs

%description cron
Cron job for weekly updates to GeoIP Legacy database from MaxMind.

%prep
%setup -q -n geoipupdate-%{version}

%build
%configure --disable-static --disable-dependency-tracking
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
mv %{buildroot}/%{_bindir}/geoipupdate %{buildroot}/%{_bindir}/geoipupdate3
mv %{buildroot}/%{_mandir}/man1/geoipupdate.1 %{buildroot}/%{_mandir}/man1/geoipupdate3.1
rm %{buildroot}/%{_mandir}/man5/GeoIP.conf.5

# We'll package the documentation ourselves
rm -rf %{buildroot}%{_datadir}/doc/geoipupdate

rm %{buildroot}%{_sysconfdir}/GeoIP.conf

install -D -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/cron.weekly/geoipupdate3

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc conf/GeoIP.conf.default README.md ChangeLog.md
%{_bindir}/geoipupdate3
%{_mandir}/man1/geoipupdate3.1*

%files cron
%config(noreplace) %{_sysconfdir}/cron.weekly/geoipupdate

%changelog
