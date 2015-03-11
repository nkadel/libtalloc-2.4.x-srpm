%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif
%{!?python_version: %global python_version %(%{__python} -c "from distutils.sysconfig import get_python_version; print(get_python_version())")}

Name: libtalloc
Version: 2.1.2
Release: 0.1%{?dist}
Group: System Environment/Daemons
Summary: The talloc library
License: LGPLv3+
URL: http://talloc.samba.org/
Source: https://www.samba.org/ftp/talloc/talloc-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: autoconf
BuildRequires: libxslt
BuildRequires: docbook-style-xsl
BuildRequires: python-devel
BuildRequires: doxygen

# Patches

%description
A library that implements a hierarchical allocator with destructors.

%package devel
Group: Development/Libraries
Summary: Developer tools for the Talloc library
Requires: libtalloc = %{version}-%{release}

%description devel
Header files needed to develop programs that link against the Talloc library.

%package -n pytalloc
Group: Development/Libraries
Summary: Developer tools for the Talloc library
Requires: libtalloc = %{version}-%{release}
Obsoletes: pytalloc < %{version}-%{release}

%description -n pytalloc
Pytalloc libraries for creating python bindings using talloc

%package -n pytalloc-devel
Group: Development/Libraries
Summary: Developer tools for the Talloc library
Requires: pytalloc = %{version}-%{release}
Obsoletes: pytalloc-devel < %{version}-%{release}

%description -n pytalloc-devel
Development libraries for pytalloc

%prep
%setup -q -n talloc-%{version}

%build
%configure --disable-rpath \
           --disable-rpath-install \
           --bundled-libraries=NONE \
           --builtin-libraries=replace \
           --disable-silent-rules

make %{?_smp_mflags} V=1
doxygen doxy.config

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Shared libraries need to be marked executable for
# rpmbuild to strip them and include them in debuginfo
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} \;

rm -f $RPM_BUILD_ROOT%{_libdir}/libtalloc.a
rm -f $RPM_BUILD_ROOT/usr/share/swig/*/talloc.i

# Install API docs
cp -a doc/man/* $RPM_BUILD_ROOT/%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

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

%files -n pytalloc
%defattr(-,root,root,-)
%{_libdir}/libpytalloc-util.so.*
%{python_sitearch}/talloc.so

%files -n pytalloc-devel
%defattr(-,root,root,-)
%{_includedir}/pytalloc.h
%{_libdir}/pkgconfig/pytalloc-util.pc
%{_libdir}/libpytalloc-util.so

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%post -n pytalloc -p /sbin/ldconfig
%postun -n pytalloc -p /sbin/ldconfig

%changelog
* Wed Mar 11 2015 Nico Kadel-Garcia <nkadel@gmail.com> - 2.1.2-0.1
- Update to 2.1.2

* Mon Jun 23 2014 Nico Kadel-Garcia <nkadel@gmail.com> - 2.1.1-0.1
- Update to 2.1.1

* Sat Sep 28 2013 Nico Kadel-Garcia <nkadel@gmail.com> - 2.1.0-0.1
- Update to 2.1.0

* Thu Feb 21 2013 Nico Kadel-Garcia <nkadel@gmail.com> - 2.0.8-0.2
- Update to 2.0.8 for Samba 4.0.3
- Discard unneeded autoconf patch

* Mon Oct  8 2012 Jakub Hrozek <jhrozek@redhat.com> - 2.0.7-2
- Obsolete older pytalloc{,-devel} releases to clear the upgrade path
  towards non-multilib pytalloc
- Resolves: rhbz#862062

* Thu Aug 2  2012 Jakub Hrozek <jhrozek@redhat.com> - 2.0.7-1
- New upstream version, resolves rhbz #766335
- Build python bindings to satisfy Samba4 BuildRequires

* Tue Dec 15 2009 Simo Sorce <ssorce@redhat.com> - 2.0.1-1.1
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
