%define version 3.7p3
%define filever 37p3
%define release %mkrel 13
%define	major	1
%define	libname	%mklibname canna %{major}

Name:		canna
Summary:	Japanese Kana-Kanji translation engine
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		System/Internationalization
URL:		http://sourceforge.jp/projects/canna/
Source:		Canna%{filever}.tar.bz2
Source1:	canna.init
Patch1:		canna-3.7p1-config.patch
Patch2:		canna-3.7p1-buildfix.patch
Patch3:		canna-3.7p1-fix-str-fmt.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
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
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{libname}-devel
Headers and libraries of Canna for development.


%prep
%setup -q -n Canna%{filever}
%patch1 -p0 -b .conf
%patch2 -p0 -b .build
%patch3 -p0 -b .str

%build
xmkmf
make canna EXTRA_LDOPTIONS="%ldflags" CCOPTIONS="%optflags"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std sysconfdir=%{buildroot}%{_sysconfdir} libCannaDir=%{_libdir}
%__install -D %SOURCE1 %{buildroot}%{_initrddir}/canna

%__install -d %{buildroot}%{_sysconfdir}/logrotate.d
cat << EOF > %{buildroot}%{_sysconfdir}/logrotate.d/canna
/var/log/canna/CANNA?msgs {
    notifempty
    missingok
}
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%_pre_useradd canna %_datadir/canna /sbin/nologin

%post
%_post_service canna

%preun
%_preun_service canna

%postun
%_postun_userdel canna

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files
%defattr(0755,root,root,0755)
%{_sbindir}/*
%{_bindir}/*
%{_initrddir}/*
%defattr(0644,root,root,0755)
%doc CHANGES.jp ChangeLog README README.jp WHATIS WHATIS.jp
%dir %{_var}/lib/canna
%config(noreplace) %{_sysconfdir}/logrotate.d/canna
%config(noreplace) %{_var}/lib/canna/default.canna
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



%changelog
* Wed Feb 02 2011 Funda Wang <fwang@mandriva.org> 3.7p3-13mdv2011.0
+ Revision: 635026
- rebuild
- fix build
- fix str fmt

* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 3.7p3-12mdv2011.0
+ Revision: 616938
- the mass rebuild of 2010.0 packages

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 3.7p3-11mdv2010.0
+ Revision: 436929
- rebuild

* Fri Mar 06 2009 Antoine Ginies <aginies@mandriva.com> 3.7p3-10mdv2009.1
+ Revision: 350661
- rebuild

* Wed Jul 23 2008 Thierry Vignaud <tv@mandriva.org> 3.7p3-9mdv2009.0
+ Revision: 243433
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 3.7p3-7mdv2008.1
+ Revision: 140691
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Sun Feb 04 2007 Christiaan Welvaart <cjw@daneel.dyndns.org>
+ 2007-02-04 13:45:47 (116150)
- rebuild for 2007.1
- Import canna

* Thu Jun 08 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 3.7p3-6mdv2007.0
- fix buildrequires
- fix executable-marked-as-config-file
- fix summary-ended-with-dot

* Wed Apr 05 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.7p3-5mdk
- patch 2: fix build (#21834)

* Fri Aug 12 2005 Nicolas Lécureuil <neoclust@mandriva.org> 3.7p3-4mdk
- fix rpmlint errors (PreReq)

* Fri Aug 12 2005 Nicolas Lécureuil <neoclust@mandriva.org> 3.7p3-3mdk
- fix rpmlint errors (PreReq)

* Sat Jul 09 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.7p3-2mdk
- fix build on x86_64

* Sat Jul 31 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.7p3-1mdk
- new release
- fix buildrequires
- add proper prereq

