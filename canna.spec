%define filever 37p3
%define	major	1
%define	libname	%mklibname canna %{major}

Name:		canna
Summary:	Japanese Kana-Kanji translation engine
Version:	3.7p3
Release:	18
License:	MIT
Group:		System/Internationalization
URL:		https://sourceforge.jp/projects/canna/
Source:		Canna%{filever}.tar.bz2
Source1:	canna.service
Source2:	canna-tmpfiles.conf
Patch1:		canna-3.7p1-config.patch
Patch2:		canna-3.7p1-buildfix.patch
Patch3:		canna-3.7p1-fix-str-fmt.patch
Requires:	locales-ja
BuildRequires:	imake

# this is for serviceadd, etc.
Requires(post): rpm-helper
Requires(preun): rpm-helper
# this is for useradd, groupadd, etc.
Requires(pre): rpm-helper
Requires(postun): rpm-helper

%description
Canna is a Japanese Kana-Kanji translation engine.


%package -n	%{libname}
Summary:	Canna libraries
Group:		System/Internationalization

%description -n	%{libname}
Canna libraries.

%package -n	%{libname}-devel
Summary:	Headers and libraries of Canna for development
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	lib%{name}-devel = %{EVRD}

%description -n %{libname}-devel
Headers and libraries of Canna for development.


%prep
%setup -q -n Canna%{filever}
%patch1 -p0 -b .conf
%patch2 -p0 -b .build
%patch3 -p0 -b .str

%build
xmkmf
make canna EXTRA_LDOPTIONS="%{ldflags}" CCOPTIONS="%{optflags}"

%install
%makeinstall_std sysconfdir=%{buildroot}%{_sysconfdir} libCannaDir=%{_libdir}
mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/canna.service

install -d -m 0755 %{buildroot}%{_sysconfdir}/tmpfiles.d
install -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

%__install -d %{buildroot}%{_sysconfdir}/logrotate.d
cat << EOF > %{buildroot}%{_sysconfdir}/logrotate.d/canna
/var/log/canna/CANNA?msgs {
    notifempty
    missingok
}
EOF

%pre
%_pre_useradd canna %{_datadir}/canna /sbin/nologin

%post
if ! grep -q canna /etc/services
then
        echo "canna             5680/tcp" >>/etc/services
fi
%systemd_post canna.service

%preun
%systemd_preun canna.service

%postun
%systemd_postun_with_restart canna.service
%_postun_userdel canna

%files
%defattr(0755,root,root,0755)
%{_sbindir}/*
%{_bindir}/*
%{_unitdir}/*
%defattr(0644,root,root,0755)
%doc CHANGES.jp ChangeLog README README.jp WHATIS WHATIS.jp
%dir %{_var}/lib/canna
%config(noreplace) %{_sysconfdir}/logrotate.d/canna
%config(noreplace) %{_var}/lib/canna/default.canna
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%{_var}/lib/canna/sample
%dir %attr(755,canna,canna) %{_var}/lib/canna/dic
%dir %attr(755,canna,canna) %{_var}/lib/canna/dic/canna
%attr(644,canna,canna) %config(noreplace) %{_var}/lib/canna/dic/*.cbp
%attr(644,canna,canna) %config(noreplace) %{_var}/lib/canna/dic/canna/*
%attr(755,canna,canna) %dir %{_var}/log/canna

%files -n %{libname}
%defattr(0755,root,root,0755)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(0644,root,root,0755)
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/*
