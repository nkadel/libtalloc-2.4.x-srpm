%global with_python3 1

# No longer python2 compatible
%global with_python2 0

%if (%{with_python2} && ! %{with_python3})
# We need to sent env PYTHON for python2 only build
%global export_waf_python export PYTHON=%{__python2}
%endif

%if (%{with_python2} && %{with_python3})
# python3 is default and therefore python2 need to be set as extra-python
%global extra_python --extra-python=%{__python2}
%endif

Name: libtalloc
Version: 2.3.1
Release: 0%{?dist}
Summary: The talloc library
License: LGPLv3+
URL: https://talloc.samba.org/
Source: https://www.samba.org/ftp/talloc/talloc-%{version}.tar.gz

# Patches

%if 0%{?rhel} > 0
# Addresses python36- versus python3- dependencies
BuildRequires: epel-rpm-macros
%endif

BuildRequires: gcc
BuildRequires: libxslt
BuildRequires: docbook-style-xsl
%if %{with_python2}
BuildRequires: python2-devel
%endif
%if %{with_python3}
BuildRequires: python%{python3_pkgversion}-devel
%endif # with_pythone
BuildRequires: doxygen

Provides: bundled(libreplace)

%description
A library that implements a hierarchical allocator with destructors.

%package devel
Summary: Developer tools for the Talloc library
Requires: libtalloc = %{version}-%{release}

%description devel
Header files needed to develop programs that link against the Talloc library.

%if %{with_python2}
%package -n python2-talloc
Summary: Python bindings for the Talloc library
Requires: libtalloc = %{version}-%{release}
Provides: pytalloc%{?_isa} = %{version}-%{release}
Provides: pytalloc = %{version}-%{release}
Obsoletes: pytalloc < 2.1.3
%{?python_provide:%python_provide python2-talloc}

%description -n python2-talloc
Python 2 libraries for creating bindings using talloc

%package -n python2-talloc-devel
Summary: Development libraries for python2-talloc
Requires: python2-talloc = %{version}-%{release}
Provides: pytalloc-devel%{?_isa} = %{version}-%{release}
Provides: pytalloc-devel = %{version}-%{release}
Obsoletes: pytalloc-devel < 2.1.3
%{?python_provide:%python_provide python2-talloc-devel}

%description -n python2-talloc-devel
Development libraries for python2-talloc
%endif # with_python2

%if %{with_python3}
%package -n python%{python3_pkgversion}-talloc
Summary: Python bindings for the Talloc library
Requires: libtalloc = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-talloc}
%if ! %{with_python2}
Obsoletes:  python2-talloc
%endif

%description -n python%{python3_pkgversion}-talloc
Python 3 libraries for creating bindings using talloc

%package -n python%{python3_pkgversion}-talloc-devel
Summary: Development libraries for python%{python3_pkgversion}-talloc
Requires: python%{python3_pkgversion}-talloc = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-talloc-devel}
%if ! %{with_python2}
Obsoletes:  python2-talloc-devel
%endif

%description -n python%{python3_pkgversion}-talloc-devel
Development libraries for python%{python3_pkgversion}-talloc
%endif # with_python3

%prep
%autosetup -n talloc-%{version} -p1

%build
# workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1217376
export python_LDFLAGS=""

%{?export_waf_python}
%configure --disable-rpath \
           --disable-rpath-install \
           --bundled-libraries=NONE \
           --builtin-libraries=replace \
           --disable-silent-rules \
           %{?extra_python}

make %{?_smp_mflags} V=1
doxygen doxy.config

%check
%{?export_waf_python}
make %{?_smp_mflags} check

%install
%{?export_waf_python}
make install DESTDIR=$RPM_BUILD_ROOT

# Install API docs
cp -a doc/man/* $RPM_BUILD_ROOT/%{_mandir}

%files
%{_libdir}/libtalloc.so.*

%files devel
%{_includedir}/talloc.h
%{_libdir}/libtalloc.so
%{_libdir}/pkgconfig/talloc.pc
%{_mandir}/man3/talloc*.3.gz
%{_mandir}/man3/libtalloc*.3.gz

%if %{with_python2}
%files -n python2-talloc
%{_libdir}/libpytalloc-util.so.*
%{python2_sitearch}/talloc.so

%files -n python2-talloc-devel
%{_includedir}/pytalloc.h
%{_libdir}/pkgconfig/pytalloc-util.pc
%{_libdir}/libpytalloc-util.so
%endif

%if %{with_python3}
%files -n python%{python3_pkgversion}-talloc
%{_libdir}/libpytalloc-util.cpython*.so.*
%{python3_sitearch}/talloc.cpython*.so

%files -n python%{python3_pkgversion}-talloc-devel
%{_includedir}/pytalloc.h
%{_libdir}/pkgconfig/pytalloc-util.cpython-*.pc
%{_libdir}/libpytalloc-util.cpython*.so
%endif

#%%ldconfig_scriptlets
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%if %{with_python2}
#%%ldconfig_scriptlets -n python2-talloc
%post -n python2-talloc -p /sbin/ldconfig
%postun -n python2-talloc -p /sbin/ldconfig
%endif

%if %{with_python3}
#%%ldconfig_scriptlets -n python%{python3_pkgversion}-talloc
%post -n python%{python3_pkgversion}-talloc -p /sbin/ldconfig
%postun -n python%{python3_pkgversion}-talloc -p /sbin/ldconfig
%endif # with_python3

%changelog
* Wed Dec 18 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 2.3.1-0
- Update to 2.3.1

* Wed Sep 4 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 2.3.0-0
- Update to 2.3.0

* Sun Jul 28 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 2.2.0-0
- Update to 2.2.0
- Obsolete python2 packages if python2 disabled
- Disable python2 entirely

* Sun May 12 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 2.1.16-0.4
- Disable python2 building for RHEL 8

* Thu Apr 25 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 2.1.16-0.3
- Update python2/python3 logic to discard python2 for Fedora > 30

* Mon Apr 15 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 2.1.16-0.2
- Add python36 support for RHEL 7

* Tue Mar 19 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 2.1.16-0.1
- Roll back release to avoid rawhide conflicts
- Include python2/python3 workarounds for Fedora python3 defaults
- Revert use of ldconfig_scriptlets
- Simplify with_python logic

* Tue Feb 26 2019 Lukas Slebodnik <lslebodn@fedoraproject.org> - 2.1.16-1
- rhbz#1683211 - libtalloc-2.1.16 is available

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Lukas Slebodnik <lslebodn@fedoraproject.org> - 2.1.15-1
- rhbz#1667471 - libtalloc-2.1.15 is available

* Fri Jul 13 2018 Jakub Hrozek <jhrozek@redhat.com> - 2.1.14-2
- Drop the unneeded ABI hide patch
- Use pathfix.py instead of a local patch to munge the python path

* Thu Jul 12 2018 Jakub Hrozek <jhrozek@redhat.com> - 2.1.14-1
- New upstream release - 2.1.14
- Apply a patch to hide local ABI symbols to avoid issues with new binutils
- Patch the waf script to explicitly call python2 as "env python" doesn't
  yield py2 anymore

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.1.13-2
- Rebuilt for Python 3.7

* Fri Apr 06 2018 Lukas Slebodnik <lslebodn@fedoraproject.org> - 2.1.13-1
- rhbz#1564323 New upstream release - 2.1.13

* Thu Mar 22 2018 Lukas Slebodnik <lslebodn@fedoraproject.org> - 2.1.12-1
- rhbz#1559378 New upstream release - 2.1.12

* Fri Mar 02 2018 Lukas Slebodnik <lslebodn@fedoraproject.org> - 2.1.11-6
- Disable link time optimisation for python3 related libs
- Workaround for rhbz#1548823

* Mon Feb 26 2018 Lukas Slebodnik <lslebodn@fedoraproject.org> - 2.1.11-5
- Add gcc to Buildroot
- https://fedoraproject.org/wiki/Changes/Remove_GCC_from_BuildRoot

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.1.11-3
- Switch to %%ldconfig_scriptlets

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 2.1.11-2
- Rebuilt for switch to libxcrypt

* Sat Jan 13 2018 Lukas Slebodnik <lslebodn@fedoraproject.org> - 2.1.11-1
- rhbz#1534136 New upstream release - 2.1.11

* Wed Nov 29 2017 Merlin Mathesius <mmathesi@redhat.com> - 2.1.10-5
- Cleanup spec file conditionals

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
