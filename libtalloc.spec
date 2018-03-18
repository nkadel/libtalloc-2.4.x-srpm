%if 0%{?fedora}
%global with_python3 1
%else
%global with_python3 0
%endif

Name: libtalloc
Version: 2.1.11
Release: 0.1%{?dist}
Group: System Environment/Daemons
Summary: The talloc library
License: LGPLv3+
URL: https://talloc.samba.org/
Source: https://www.samba.org/ftp/talloc/talloc-%{version}.tar.gz

BuildRequires: libxslt
BuildRequires: docbook-style-xsl
BuildRequires: python2-devel
%if 0%{?with_python3}
BuildRequires: python3-devel
%endif
BuildRequires: doxygen

Provides: bundled(libreplace)

# Patches

%description
A library that implements a hierarchical allocator with destructors.

%package devel
Group: Development/Libraries
Summary: Developer tools for the Talloc library
Requires: libtalloc = %{version}-%{release}

%description devel
Header files needed to develop programs that link against the Talloc library.

%package -n python2-talloc
Group: Development/Libraries
Summary: Python bindings for the Talloc library
Requires: libtalloc = %{version}-%{release}
Provides: pytalloc%{?_isa} = %{version}-%{release}
Provides: pytalloc = %{version}-%{release}
Obsoletes: pytalloc < 2.1.3
%{?python_provide:%python_provide python2-talloc}

%description -n python2-talloc
Python 2 libraries for creating bindings using talloc

%package -n python2-talloc-devel
Group: Development/Libraries
Summary: Development libraries for python2-talloc
Requires: python2-talloc = %{version}-%{release}
Provides: pytalloc-devel%{?_isa} = %{version}-%{release}
Provides: pytalloc-devel = %{version}-%{release}
Obsoletes: pytalloc-devel < 2.1.3
%{?python_provide:%python_provide python2-talloc-devel}

%description -n python2-talloc-devel
Development libraries for python2-talloc

%if 0%{?with_python3}
%package -n python3-talloc
Group: Development/Libraries
Summary: Python bindings for the Talloc library
Requires: libtalloc = %{version}-%{release}
%{?python_provide:%python_provide python3-talloc}

%description -n python3-talloc
Python 3 libraries for creating bindings using talloc

%package -n python3-talloc-devel
Group: Development/Libraries
Summary: Development libraries for python3-talloc
Requires: python3-talloc = %{version}-%{release}
%{?python_provide:%python_provide python3-talloc-devel}

%description -n python3-talloc-devel
Development libraries for python3-talloc
%endif

%prep
%autosetup -n talloc-%{version} -p1

%build

%if 0%{?with_python3}
PY3_CONFIG_FLAGS=--extra-python=%{__python3}
%else
PY3_CONFIG_FLAGS=""
%endif

%configure --disable-rpath \
           --disable-rpath-install \
           --bundled-libraries=NONE \
           --builtin-libraries=replace \
           --disable-silent-rules \
           $PY3_CONFIG_FLAGS

make %{?_smp_mflags} V=1
doxygen doxy.config

%check
make %{?_smp_mflags} check

%install

make install DESTDIR=$RPM_BUILD_ROOT

# Shared libraries need to be marked executable for
# rpmbuild to strip them and include them in debuginfo
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} \;

rm -f $RPM_BUILD_ROOT%{_libdir}/libtalloc.a
rm -f $RPM_BUILD_ROOT/usr/share/swig/*/talloc.i

# Install API docs
cp -a doc/man/* $RPM_BUILD_ROOT/%{_mandir}

%files
%defattr(-,root,root,-)
%{_libdir}/libtalloc.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/talloc.h
%{_libdir}/libtalloc.so
%{_libdir}/pkgconfig/talloc.pc
%{_mandir}/man3/talloc*.3.gz
%{_mandir}/man3/libtalloc*.3.gz

%files -n python2-talloc
%defattr(-,root,root,-)
%{_libdir}/libpytalloc-util.so.*
%{python_sitearch}/talloc.so

%files -n python2-talloc-devel
%defattr(-,root,root,-)
%{_includedir}/pytalloc.h
%{_libdir}/pkgconfig/pytalloc-util.pc
%{_libdir}/libpytalloc-util.so

%if 0%{?with_python3}
%files -n python3-talloc
%defattr(-,root,root,-)
%{_libdir}/libpytalloc-util.cpython*.so.*
%{python3_sitearch}/talloc.cpython*.so

%files -n python3-talloc-devel
%defattr(-,root,root,-)
%{_includedir}/pytalloc.h
%{_libdir}/pkgconfig/pytalloc-util.cpython-*.pc
%{_libdir}/libpytalloc-util.cpython*.so
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n python2-talloc -p /sbin/ldconfig
%postun -n python2-talloc -p /sbin/ldconfig

%if 0%{?with_python3}
%post -n python3-talloc -p /sbin/ldconfig
%postun -n python3-talloc -p /sbin/ldconfig
%endif

%changelog
* Sat Mar 17 2018 Nico Kadel-Garcia <nkadel@gmail.com> - 2.1.11-0.1
- Update to 2.1.11

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Lukas Slebodnik  <lslebodn@redhat.com> - 2.1.10-2
- fix location of pkgconfig files for libpytalloc*

* Mon Jul 24 2017 Lukas Slebodnik  <lslebodn@redhat.com> - 2.1.10-1
- rhbz#1473997 New upstream release - 2.1.10
- enable unit tests

* Thu Jul 06 2017 Andreas Schneider <asn@redhat.com> - 2.1.9-2
- Install pytalloc-util for python3 as well

* Tue Feb 28 2017 Lukas Slebodnik  <lslebodn@redhat.com> - 2.1.9-1
- rhbz#1427352 New upstream release - 2.1.9
- rhbz#1401225 - Rename python packages to match packaging guidelines
  https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.1.8-2
- Rebuild for Python 3.6

* Thu Jul 28 2016 Jakub Hrozek <jhrozek@redhat.com> - 2.1.8-1
- New upstream release - 2.1.8

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.7-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri May  6 2016 Jakub Hrozek <jhrozek@redhat.com> - 2.1.7-1
- New upstream release - 2.1.7
- Resolves: rhbz#1333790 - libtalloc-2.1.7 is available

* Wed Mar  9 2016 Jakub Hrozek <jhrozek@redhat.com> - 2.1.6-1
- New upstream release - 2.1.6

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 11 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Nov 11 2015 Jakub Hrozek <jhrozek@redhat.com> - 2.1.5-1
- New upstream release - 2.1.5

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Oct 14 2015 Jakub Hrozek <jhrozek@redhat.com> - 2.1.4-1
- New upstream release - 2.1.4

* Wed Jul 22 2015 Jakub Hrozek <jhrozek@redhat.com> - 2.1.3-1
- New upstream release - 2.1.3
- Resolves: rhbz#1241928 - Switch libtalloc to use python3
- Rename pytalloc to python-talloc (Miro Hrončok <mhroncok@redhat.com>)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 13 2015 Jakub Hrozek <jhrozek@redhat.com> - 2.1.2-1
- New upstream release - 2.1.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Jakub Hrozek <jhrozek@redhat.com> - 2.1.1-1
- New upstream release

* Sun Dec 15 2013 Jakub Hrozek <jhrozek@redhat.com> - 2.1.0-3
- Bump NVR in order to tag a build

* Tue Sep 10 2013 Jakub Hrozek <jhrozek@redhat.com> - 2.1.0-2
- New upstream release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 01 2012 Jakub Hrozek <jhrozek@redhat.com> - 2.0.8-1
- New upstream release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 01 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.7-3
- Add patch to ignore --disable-silent-rules
- Package API docs into libtalloc-devel

* Wed Nov 23 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.7-2
- Add explicit mention of the bundled libreplace
- https://fedorahosted.org/fpc/ticket/120

* Fri Nov 04 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.7-1
- New upstream release
- Required for new Samba 4 alpha builds

* Mon Aug 08 2011 Simo Sorce <ssorce@redhat.com> - 2.0.6-1
- New upstream release
- Fixes various bugs with talloc_free_children and freeing complex
  hierarchies with many siblinbgs.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.5-7
- Let rpmbuild strip binaries, make build more verbose.
- Resolves rhbz#669477 - libtalloc 2.0.5-6 binaries not stripped,
-                        empty -debuginfo
- Original patch by Ville SkyttÃ¤ <ville.skytta@iki.fi>

* Wed Jan 12 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.5-6
- Install python bindings in the correct location

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.5-5
- Run ldconfig on pytalloc

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.5-4
- Fix build failure on 32-bit platforms

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.5-3
- New version from upstream
- Add support for pytalloc
- Convert to new WAF build-system

* Tue Dec 15 2009 Simo Sorce <ssorce@redhat.com> - 2.0.1-1
- New version from upstream
- Also stop building the compat lib, it is not necessary anymore

* Tue Sep  8 2009 Simo Sorce <ssorce@redhat.com> - 2.0.0-0
- New version from upstream.
- Build also sover 1 compat library to ease packages migration

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Simo Sorce <ssorce@redhat.com> - 1.3.1-1
- Original tarballs had a screw-up, rebuild with new fixed tarballs from
  upstream.

* Tue Jun 16 2009 Simo Sorce <ssorce@redhat.com> - 1.3.1-0
- New Upstream release.

* Wed May 6 2009 Simo Sorce <ssorce@redhat.com> - 1.3.0-0
- First public independent release from upstream
