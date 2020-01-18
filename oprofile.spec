Summary: System wide profiler
Name: oprofile
Version: 0.9.9
Release: 22%{?dist}
License: GPLv2+ and LGPLv2+
Group: Development/System
#
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Requires: binutils
Requires: which
Requires(pre): shadow-utils
Requires(postun): shadow-utils
Patch10: oprofile-0.4-guess2.patch
Patch83: oprofile-0.9.7-xen.patch
Patch303: oprofile-num_symbolic.patch
Patch304: oprofile-xml.patch
Patch305: oprofile-rhbz1121205.patch
Patch400: oprofile-haswell.patch
Patch401: oprofile-silvermont.patch
Patch402: oprofile-broadwell.patch
Patch403: oprofile-intelcpuid.patch
Patch500: oprofile-aarch64.patch
Patch600: oprofile-power8.patch
Patch601: oprofile-ppc64le.patch
Patch602: oprofile-ppc64-equivalent.patch
Patch700: oprofile-hugepage.patch
Patch800: oprofile-defaultmask.patch
Patch801: oprofile-extramask.patch
Patch802: oprofile-maskarray.patch
Patch803: oprofile-env.patch
Patch804: oprofile-coverity.patch
Patch900: oprofile-ppc64jvm.patch
Patch1000: oprofile-skylake.patch
Patch1001: oprofile-remap.patch
Patch1002: oprofile-xml2.patch
Patch1003: oprofile-goldmont.patch
Patch1004: oprofile-bz1335145.patch
Patch1005: oprofile-bz1264443.patch
Patch1006: oprofile-captest.patch
Patch1007: oprofile-order.patch
Patch1010: oprofile-rhbz1385007.patch
Patch1011: oprofile-rhbz1426426.patch

URL: http://oprofile.sf.net

#If oprofile doesn't build on an arch, report it and will add ExcludeArch tag.
BuildRequires: qt-devel
BuildRequires: libxslt
BuildRequires: docbook-style-xsl
BuildRequires: docbook-utils
BuildRequires: elinks
BuildRequires: gtk2-devel
BuildRequires: automake
BuildRequires: libtool
BuildRequires: binutils-static
BuildRequires: popt-devel
BuildRequires: java-devel
BuildRequires: jpackage-utils
BuildRequires: java-1.7.0-openjdk-devel
BuildRequires: libpfm-devel >= 4.3.0

BuildRoot: %{_tmppath}/%{name}-root

%description
OProfile is a profiling system for systems running Linux. The
profiling runs transparently during the background, and profile data
can be collected at any time. OProfile makes use of the hardware performance
counters provided on Intel P6, and AMD Athlon family processors, and can use
the RTC for profiling on other x86 processor types.

See the HTML documentation for further details.

%package devel
Summary: Header files and libraries for developing apps which will use oprofile
Group: Development/Libraries
Requires: oprofile = %{version}-%{release}
Provides: oprofile-static = %{version}-%{release}

%description devel

Header files and libraries for developing apps which will use oprofile.

%package gui
Summary: GUI for oprofile
Group: Development/System
Requires: oprofile = %{version}-%{release}

%description gui

The oprof_start GUI for oprofile.

%package jit
Summary: Libraries required for profiling Java and other JITed code
Group: Development/System
Requires: oprofile = %{version}-%{release}
#Requires: java >= 1.6
#Requires: jpackage-utils

%description jit
This package includes a base JIT support library, as well as a Java
agent library.

%prep
%setup -q -n %{name}-%{version}
%patch10 -p1 -b .guess2
%patch83 -p1 -b .xen
%patch303 -p1 -b .num_symbolic
%patch304 -p1 -b .xml
%patch305 -p1 -b .xml
%patch400 -p1 -b .haswell
%patch401 -p1 -b .silvermont
%patch402 -p1 -b .broadwell
%patch403 -p1
%patch500 -p1 -b .aarch64
%patch600 -p1 -b .power8
%patch601 -p1 -b .ppc64le
%patch602 -p1
%patch700 -p1
%patch800 -p1
%patch801 -p1
%patch802 -p1
%patch803 -p1
%patch804 -p1
%patch900 -p1
%patch1000 -p1
%patch1001 -p1
%patch1002 -p1
%patch1003 -p1
%patch1004 -p1
%patch1005 -p1 -b .archive
%patch1006 -p1 -b .captest
%patch1007 -p1 -b .order
%patch1010 -p1 -b .rhbz1385007
%patch1011 -p1 -b .rhbz1426426

./autogen.sh

%build

#The CXXFLAGS below is temporary to work around
# bugzilla #113909
CXXFLAGS=-g;     export CXXFLAGS

%configure \
--enable-gui=qt4 \
--with-java=/usr/lib/jvm/java

make CFLAGS="%{optflags}"

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1

make DESTDIR=%{buildroot} INSTALL="install -p" install

# We want the manuals in the special doc dir, not the generic doc install dir.
# We build it in place and then move it away so it doesn't get installed
# twice. rpm can specify itself where the (versioned) docs go with the
# %%doc directive.
mkdir docs.installed
mv %{buildroot}%{_datadir}/doc/oprofile/* docs.installed/

mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{_libdir}/oprofile" > %{buildroot}/etc/ld.so.conf.d/oprofile-%{_arch}.conf

%pre
getent group oprofile >/dev/null || groupadd -r -g 16 oprofile
getent passwd oprofile >/dev/null || \
useradd -g oprofile -d /var/lib/oprofile -M -r -u 16 -s /sbin/nologin \
    -c "Special user account to be used by OProfile" oprofile
exit 0

%postun
# do not try to remove existing oprofile user or group

%files
%defattr(-,root,root)
%doc  docs.installed/*
%doc COPYING

%{_bindir}/ocount
%{_bindir}/ophelp
%{_bindir}/opimport
%{_bindir}/opannotate
%{_bindir}/opcontrol
%{_bindir}/opgprof
%{_bindir}/opreport
%{_bindir}/oprofiled
%{_bindir}/oparchive
%{_bindir}/opjitconv
%{_bindir}/op-check-perfevents
%{_bindir}/operf

%{_mandir}/man1/*

%{_datadir}/oprofile

%files devel
%defattr(-,root,root)

%{_includedir}/opagent.h

%files gui
%defattr(-,root,root)

%{_bindir}/oprof_start

%post jit -p /sbin/ldconfig

%postun jit -p /sbin/ldconfig

%files jit
%defattr(-,root,root)

%{_libdir}/oprofile
%{_sysconfdir}/ld.so.conf.d/*

%changelog
* Tue Mar 21 2017 William Cohen <wcohen@redhat.com> - 0.9.9-22
- Update ppc64/ppc64le support. rhbz1385007
- Add recognition check for POWER8NV and POWER8NVL. rhbz1426426

* Wed Oct 19 2016 William Cohen <wcohen@redhat.com> - 0.9.9-21
- Fix Intel Goldmont default event

* Tue Aug 9 2016 William Cohen <wcohen@redhat.com> - 0.9.9-20
- Ensure that the perf events setup before ocount execs child.

* Mon Aug 8 2016 William Cohen <wcohen@redhat.com> - 0.9.9-19
- Allow operation /proc/sys/kernel/perf_event_paranoid == 2.

* Wed Jul 6 2016 William Cohen <wcohen@redhat.com> - 0.9.9-18
- Store profiling data with oparchive.

* Thu May 12 2016 William Cohen <wcohen@redhat.com> - 0.9.9-17
- Define some  Intel broadwell default unit masks by names
- Add support for Harrisonville (Denverton SoC)
- Add support for Skylake-SP server
- Add support for Kabylake-U/Y
- Add support for Kabylake-H/S
- Make Nehalem, Westmere, and Haswell event names unique.

* Tue Aug 25 2015 William Cohen <wcohen@redhat.com> - 0.9.9-16
- Improved handling of remapped anonymous regions
- Correct XML generation.

* Wed Jul 8 2015 William Cohen <wcohen@redhat.com> - 0.9.9-15
- Add support for Intel skylake processors.

* Fri Jun 26 2015 William Cohen <wcohen@redhat.com> - 0.9.9-14
- Recognize Intel Broadwell-DE.

* Fri Jun 5 2015 William Cohen <wcohen@redhat.com> - 0.9.9-13
- Further fix to allow operf to record information for Java anon_huges.

* Fri Jun 5 2015 William Cohen <wcohen@redhat.com> - 0.9.9-12
- Eliminate some coverity warnings.

* Tue Apr 7 2015 William Cohen <wcohen@redhat.com> - 0.9.9-11
- Avoid setting POSIXLY_CORRECT for the children tasks of operf and ocount.
- Fix handling of default unit masks longer than 11 char.
- Fix extra and default unitmasks selection.
- Allow operf to record information for Java anon_huges.

* Wed Oct 1 2014 Will Cohen <wcohen@redhat.com> - 0.9.9-7
- Correct identification power8le. rhbz1148525

* Wed Sep 17 2014 Will Cohen <wcohen@redhat.com> - 0.9.9-6
- Update support for Intel Silvermont (Avoton).
- Enable configure for ppc64le.

* Mon Aug 18 2014 Will Cohen <wcohen@redhat.com> - 0.9.9-5
- Update Intel Haswell events.
- Add support for Intel Silvermont (Avoton).
- Add support for Intel Broadwell.
- Add support for aarch64.
- Update IBM power8 events.

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.9.9-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.9.9-3
- Mass rebuild 2013-12-27

* Tue Aug 06 2013 Will Cohen <wcohen@redhat.com> - 0.9.9-2
- rhbz993994 Eliminate versioned doc pages.

* Mon Jul 29 2013 Will Cohen <wcohen@redhat.com> - 0.9.9-1
- Rebase on oprofile.
- Trim changelog entries

* Mon Jul 15 2013 Will Cohen <wcohen@redhat.com> - 0.9.8-10
- rhbz949028: Man page scan results for oprofile

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 19 2012 Will Cohen <wcohen@redhat.com> - 0.9.8-3
- Use buildid support instead of crc checks. rhbz #877187

* Mon Oct 15 2012 Will Cohen <wcohen@redhat.com> - 0.9.8-2
- Cleanup configure.
- Add libpfm-devel to the buildrequires.

* Tue Sep 04 2012 Will Cohen <wcohen@redhat.com> - 0.9.8-1
- Rebase on oprofile-0.9.8.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 5 2012 Will Cohen <wcohen@redhat.com> - 0.9.7-4
- Fix autogen.sh to avoid false match.

* Wed Apr 4 2012 Will Cohen <wcohen@redhat.com> - 0.9.7-3
- Use correct macros for /etc and /user/share. rhbz #226222
- Consistently use macros for buildroot.
- Preserve timestamp for installed files.
- Remove the clean section.
- Fix the source location.
- Remove unneeded BuildRequires: binutils-devel
- Remove unneeded depends.
- Correct Buildreq to java-1.7.0-openjdk-devel.
- Fix macro-in-comment and macro-in-changelog
- Remove '.' from Summary lines
- Correct license GPLv2+ and LGPLv2+.
- Do not remove oprofile user or group.

* Tue Jan 10 2012 Will Cohen <wcohen@redhat.com> - 0.9.7-2
- Remove duplicate -r option in %%pre useradd Resolves: rhbz #772841

* Tue Nov 29 2011 Will Cohen <wcohen@redhat.com> - 0.9.7-1
- Rebase on oprofile-0.9.7.

* Tue Jun 07 2011 Will Cohen <wcohen@redhat.com> - 0.9.6-21
- Correct CVE-2011-1760. Resolves: rhbz #701508

* Tue Apr 5 2011 Will Cohen <wcohen@redhat.com> - 0.9.6-20
- Re-enable xenoprof patch.

* Thu Mar 31 2011 Will Cohen <wcohen@redhat.com> - 0.9.6-19
- Provide oprofile-static.

* Tue Mar 15 2011 Will Cohen <wcohen@redhat.com> - 0.9.6-18
- Clean up rpmlint complaints.

* Tue Mar 15 2011 Will Cohen <wcohen@redhat.com> - 0.9.6-17
- Correct oprofile user information.

* Thu Mar 10 2011 Will Cohen <wcohen@redhat.com> - 0.9.6-16
- Remove obsolete configure options.

* Thu Mar 10 2011 Will Cohen <wcohen@redhat.com> - 0.9.6-15
- Use QT4.

* Fri Feb 25 2011 Will Cohen <wcohen@redhat.com> - 0.9.6-14
- Add processors models for Intel westmere and core i7.

* Wed Feb 09 2011 Will Cohen <wcohen@redhat.com> - 0.9.6-12
- Eliminate illegal mutable use.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 6 2011 Will Cohen <wcohen@redhat.com> - 0.9.6-10
- Corrections for i386/arch_perfmon filters.
- Make nehalem events available.
- Add AMD family 12/14/15h support.
- Add Intel westemere support.
- opcontrol numeric argument checking.

* Wed Apr 21 2010 Will Cohen <wcohen@redhat.com> - 0.9.6-6
- Bump version and rebuild.

* Wed Apr 14 2010 Will Cohen <wcohen@redhat.com> - 0.9.6-5
- Handle debuginfo section differences. rhbz554639

* Mon Apr 5 2010 Will Cohen <wcohen@redhat.com> - 0.9.6-3
- Include Buildrequires for binutils-static.

* Fri Dec 11 2009 Will Cohen <wcohen@redhat.com> - 0.9.6-2
- Clean up oprofile.spec file.

* Tue Nov 24 2009 Will Cohen <wcohen@redhat.com> - 0.9.6-1
- Rebase on OProfile 0.9.6.

* Wed Oct 21 2009 Will Cohen <wcohen@redhat.com> - 0.9.5-4
- Switch to using ExcludeArch.

* Wed Oct 7 2009 Will Cohen <wcohen@redhat.com> - 0.9.5-3
- Allow timer mode to work.
- Correct location for addditional files in man pages. Resolves: rhbz #508669

* Fri Sep 4 2009 Will Cohen <wcohen@redhat.com> - 0.9.5-2
- Bump version and rebuild.

* Mon Aug 3 2009 Will Cohen <wcohen@redhat.com> - 0.9.5-1
- Rebase on OProfile 0.9.5.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Will Cohen <wcohen@redhat.com> - 0.9.4-12
- Add shadow-utils to requires. Resolves: rhbz #501357
- Add LGPL license to provided java support. Resolves: rhbz #474666
- Correct handling of --verbose. Resolves: rhbz #454969

* Mon May 11 2009 Will Cohen <wcohen@redhat.com> - 0.9.4-9
- Assign specific UID and GID to oprofile.

* Thu Apr 23 2009 Will Cohen <wcohen@redhat.com> - 0.9.4-7
- Backport Intel Architecture Perfmon support. Resolves: rhbz #497230

* Wed Apr 8 2009 Will Cohen <wcohen@redhat.com> - 0.9.4-6
- Test for basename declaration.

* Wed Apr 8 2009 Will Cohen <wcohen@redhat.com> - 0.9.4-5
- Bump version and rebuild.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 29 2008 Dennis Gilmore <dennis@ausil.us> - 0.9.4-3
- build sparcv9 not sparc

* Mon Jul 21 2008 Will Cohen <wcohen@redhat.com> - 0.9.4-2
- Correct oprofile.spec.

* Fri Jul 18 2008 Will Cohen <wcohen@redhat.com> - 0.9.4-1
- Update to orprofile 0.9.4.

* Mon Jun 23 2008 Will Cohen <wcohen@redhat.com> - 0.9.3-18
- Fix default location for vmlinux. rhbz #451539

* Fri Apr 04 2008 Will Cohen <wcohen@redhat.com> - 0.9.3-17
- Use older qt3-devel. rhbz #440949

* Fri Feb 15 2008 Will Cohen <wcohen@redhat.com> - 0.9.3-16
- Corrections for compilation with gcc-4.3.

* Fri Jan 18 2008 Will Cohen <wcohen@redhat.com> - 0.9.3-15
- Deal with xenoprof conlficts with cell. Resolves: rhbz #250852

* Fri Jan 18 2008 Will Cohen <wcohen@redhat.com> - 0.9.3-14
- Bump format version. Check version properly. Resolves: rhbz #394571

* Fri Jan 18 2008 Will Cohen <wcohen@redhat.com> - 0.9.3-13
- Disable profiling in hypervisor on 970MP to prevent lost interrupts.
  Resolves: rhbz #391251

* Fri Jan 18 2008 Will Cohen <wcohen@redhat.com> - 0.9.3-12
- Use more incluse set of kernel ranges. Resolves: rhbz #307111

* Fri Jan 18 2008 Will Cohen <wcohen@redhat.com> - 0.9.3-11
- Update AMD family 10h events to match AMD documentation Resolves: rhbz #232956

* Mon Nov 12 2007 Will Cohen <wcohen@redhat.com> - 0.9.3-7
- Should correct missing 'test' in patch.

* Mon Oct 8 2007 Will Cohen <wcohen@redhat.com> - 0.9.3-5
- Should be popt-devel to BuildRequires.

* Mon Oct 8 2007 Will Cohen <wcohen@redhat.com> - 0.9.3-5
- Add popt to BuildRequires.

* Mon Oct 8 2007 Will Cohen <wcohen@redhat.com> - 0.9.3-4
- Allow short forms of --list-events (-l)  and --dump (-d).
  Resolves: rhbz#234003.

* Tue Aug 21 2007 Will Cohen <wcohen@redhat.com> - 0.9.3-3
- rebuild

* Wed Jul 25 2007 Will Cohen <wcohen@redhat.com> - 0.9.3-2
- Re-enable xen patch.

* Tue Jul 17 2007 Will Cohen <wcohen@redhat.com> - 0.9.3-1
- Rebase on 0.9.3 release.
- Disable xen patch until fixed.

* Mon May 21 2007 Will Cohen <wcohen@redhat.com> - 0.9.2-9
- Fix up rpmlint complaints.

* Wed Mar 21 2007 Will Cohen <wcohen@redhat.com> - 0.9.2-8
- Add AMD family 10 support. Resolves: rhbz#232956.

* Wed Mar 21 2007 Will Cohen <wcohen@redhat.com> - 0.9.2-7
- Correct description for package.
- Correct backtrace documentation. Resolves: rhbz#214793.
- Correct race condition. Resolves: rhbz#220116.


* Fri Nov 3 2006 Will Cohen <wcohen@redhat.com> - 0.9.2-3
- Add dist tag to build.

* Fri Sep 22 2006 Will Cohen <wcohen@redhat.com> - 0.9.2-2
- Rebase on 0.9.2 release.

* Thu Aug 24 2006 Will Cohen <wcohen@redhat.com>
- Update xenoprof patch.

* Wed Jul 19 2006 Jesse Keating <jkeating@redhat.com> - 0.9.1-15
- rebuild
- remove silly release definition

* Wed Jul 12 2006 Will Cohen <wcohen@redhat.com>
- Support for Intel Woodcrest. (#183081)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.9.1-13.1.1.1
- rebuild

* Mon Jul 10 2006 Will Cohen <wcohen@redhat.com>
- Add power6 support. (#196505)

* Fri Jul 7 2006 Will Cohen <wcohen@redhat.com>
- Support for power5+. (#197728)
- Fix PPC64 events and groups. (#197895)

* Wed Jun 07 2006 Will Cohen <wcohen@redhat.com>
- Put oprof_start in to oprofile-gui.

* Wed Jun 07 2006 Will Cohen <wcohen@redhat.com> - 0.9.1-10.1.1
- Bump version and rebuild.

* Sat May 13 2006 Will Cohen <wcohen@redhat.com> - 0.9.1-9.1.1
- Add xenoprof patch.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.9.1-8.1.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Will Cohen <wcohen@redhat.com>
- Complete path for which and dirname in opcontrol.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.9.1-7.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Dec 22 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Dec 05 2005 Will Cohen <wcohen@redhat.com>
- Correct anon namespace issue.

* Fri Nov 11 2005 Will Cohen <wcohen@redhat.com>
- Add alpha and sparcs to exclusivearch.

* Tue Jul 26 2005 Will Cohen <wcohen@redhat.com>
- Rebase on OProfile 0.9.1.
- Add MIPS 24K files to manifest.

* Wed Jun 08 2005 Will Cohen <wcohen@redhat.com>
- Rebase on OProfile 0.9.

* Wed Apr 13 2005 Will Cohen <wcohen@redhat.com>
- Add which dependency.

* Tue Apr 05 2005 Will Cohen <wcohen@redhat.com>
- Backport ppc64 patch for synthesizing dotted symbols.

* Mon Mar 21 2005 Will Cohen <wcohen@redhat.com>
- Bump release.
- Rebase on 0.8.2 release.

* Mon Mar 14 2005 Will Cohen <wcohen@redhat.com>
- Bump rebuild with gcc4.

* Wed Feb  9 2005 Will Cohen <wcohen@redhat.com>
- Do not need -D_FORTIFY_SOURCE=2
 
* Wed Feb  9 2005 Will Cohen <wcohen@redhat.com>
- Rebuild for -D_FORTIFY_SOURCE=2
 
* Fri Oct 15 2004 Will Cohen <wcohen@redhat.com>
- Additional ppc64 support for ppc64/970.

* Thu Oct 7 2004 Will Cohen <wcohen@redhat.com>
- Correct opcontrol check for Power 4/5.

* Fri Oct 1 2004 Will Cohen <wcohen@redhat.com>
- Add support for Power 4/5 performance monitoring hardware.

* Wed Sep 22 2004 Will Cohen <wcohen@redhat.com>
- Add logic to use preferred symbol names.

* Wed Sep 15 2004 Will Cohen <wcohen@redhat.com>
- Clean up file manifests.

* Mon Sep 13 2004 Will Cohen <wcohen@redhat.com>
- Rebase on 0.8.1 release.

* Wed Jul 7 2004 Will Cohen <wcohen@redhat.com>
- Add oparchive patch.

* Mon Jun 21 2004 Will Cohen <wcohen@redhat.com>
- bump version

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 20 2004 Will Cohen <wcohen@redhat.com>
- Eliminate AUTOMAKE and ACLOCAL definitions.
- Correct QTDIR and add oprof_start to file manifests.

* Tue May 11 2004 Will Cohen <wcohen@redhat.com>
- Remove wildcards in the file manifests.
- Correct build directory.
- Use the 0.8 release tarball.

* Tue Mar 23 2004 Will Cohen <wcohen@redhat.com>
- Bump version and rebuild.

* Mon Mar 15 2004 Will Cohen <wcohen@redhat.com>
- Correct cvs checkin.

* Thu Feb 19 2004 Will Cohen <wcohen@redhat.com>
- Use automake 1.6.

* Wed Jan 21 2004 Will Cohen <wcohen@redhat.com>
- Rebase on 8.0 cvs snapshot.

* Mon Dec 01 2003 Will Cohen <wcohen@redhat.com>
- Turn on debug info patch.

* Mon Nov 24 2003 Will Cohen <wcohen@redhat.com>
- Rebase on 7.1 cvs snapshot.

* Fri Sep 26 2003 Will Cohen <wcohen@redhat.com>
- Reenable separatedebug and filepos patch.

* Thu Sep 4 2003 Will Cohen <wcohen@redhat.com>
- Limit to i386.
- Everything but x86_64.
- Turn on x86_64.

* Mon Aug 11 2003 Will Cohen <wcohen@redhat.com>
- Add gtk2-devel to build requirements.

* Thu Aug 07 2003 Will Cohen <wcohen@redhat.com>
- adapt to 0.7cvs.

* Wed Jul 30 2003 Will Cohen <wcohen@redhat.com>
- handle sample files names with spaces.
- clean spec file.
- revise opcontrol --reset.

* Fri Jul 25 2003 Will Cohen <wcohen@redhat.com>
- Restrict PATH in opcontrol.

* Wed Jul 09 2003 Will Cohen <wcohen@redhat.com>
- Patch for testing code coverage.
- Better handling of 2.5 module information.

* Fri Jun 27 2003 Will Cohen <wcohen@redhat.com>
- move to oprofile 0.5.4 pristine tarball.

* Fri Jun 13 2003 Will Cohen <wcohen@redhat.com>
- Bitmask check.

* Wed Jun 11 2003 Will Cohen <wcohen@redhat.com>
- Update AMD events.

* Fri Jun 06 2003 Will Cohen <wcohen@redhat.com>
- Build for ppc64.

* Thu Jun 05 2003 Will Cohen <wcohen@redhat.com>
- put in s390.
- Fix includes for asserts.
- Make sure elinks is available for html to txt conversion.

* Fri May 23 2003 Will Cohen <wcohen@redhat.com>
- Avoid library name collisions.

* Thu May 22 2003 Will Cohen <wcohen@redhat.com>
- Turn on ppc build.
- Turn off ppc build.
- Package op_list.h.

* Mon May 19 2003 Will Cohen <wcohen@redhat.com>
- Correct typo.

* Thu Apr 24 2003 Will Cohen <wcohen@redhat.com>
- check min event counts.
- revised op_to_source output to avoid changing line count.
- p4event events revised.
- hammer events revised.

* Wed Apr 23 2003 Will Cohen <wcohen@redhat.com>
- re-enable ppc build.

* Wed Apr 16 2003 Will Cohen <wcohen@redhat.com>
- Use /proc/ksym for module information.
- Correct separate debuginfo handling.
- Configure with --enable-abi.

* Tue Apr 1 2003 Will Cohen <wcohen@redhat.com>
- Correct path finding for daemon and op_help.

* Mon Mar 31 2003 Will Cohen <wcohen@redhat.com>
- Fix name collisons with /usr/lib/libdb.a.

* Fri Mar 28 2003 Will Cohen <wcohen@redhat.com>
- clean up spec file.
- turn off ppc build.

* Mon Mar 24 2003 Will Cohen <wcohen@redhat.com>
- getc instead of fgetc to improve performance.

* Thu Mar 20 2003 Will Cohen <wcohen@redhat.com>
- produce oprofile-devel.

* Thu Mar 13 2003 Will Cohen <wcohen@redhat.com>
- fix opvisualise patch format.

* Wed Mar 12 2003 Will Cohen <wcohen@redhat.com>
- add cmoller changes to fix warnings in opvisualise.

* Tue Mar 11 2003 Will Cohen <wcohen@redhat.com>
- setup to build on ppc.
- turn on op_visualise for ia64.
- remove unused patches.

* Mon Mar 10 2003 Will Cohen <wcohen@redhat.com>
- re-enable op_visualise.

* Fri Mar 7 2003 Will Cohen  <wcohen@redhat.com>
- move to oprofile 0.5.1 pristine tarball.
- change libdb abi.

* Fri Feb 14 2003 Will Cohen <wcohen@redhat.com>
- Requires binutils not perl.

* Thu Feb 13 2003 Will Cohen <wcohen@redhat.com>
- correct x86_64 sys_lookup_dcookie.
- correct applications of patches.

* Mon Feb 10 2003 Will Cohen <wcohen@redhat.com>
- rebuilt.
- handle stale locks
- opcontrol rtc patch
- update manpage info

* Fri Feb 7 2003 Will Cohen <wcohen@redhat.com>
- turn on build for ppc64
- change order op_visualise searches lib directories.
- revise oprofile-0.4-deprecate patch.
- utils/oprofile kernel range check, --save, and do_dump corrections.
- update gui to use "--separate=library".

* Thu Feb 6 2003 Will Cohen <wcohen@redhat.com>
- Fix dumping.

* Fri Jan 31 2003 Will Cohen <wcohen@redhat.com>
- Syscall value for x86_64.
- Update manpage and documentation.
- Revise utils/* to deprecate old.
- Include CPU_P4_HT2 in op_help.c
- Revise how CPU_TIMER_INT handled.
- Apply cookie patch for all archs.
- Correct autogen.sh location.

* Mon Jan 27 2003 Will Cohen <wcohen@redhat.com>
- Add Hammer specific events.

* Fri Jan 24 2003 Will Cohen <wcohen@redhat.com>
- Hack to get correct syscall for ia64.
- Hack to get get timer interupt data.
- Fix doc/Makefile.am.

* Wed Jan 22 2003 Will Cohen <wcohen@redhat.com>
- Add patch for separate debug infomation.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan 16 2003 Will Cohen <wcohen@redhat.com>
- Add support for P4 HT.

* Wed Jan 15 2003 Will Cohen <wcohen@redhat.com>
- Add support for x86_64.

* Tue Jan 07 2003 Will Cohen <wcohen@redhat.com>
- Revise op_visualise patch to check opendir() results.

* Mon Jan 06 2003 Will Cohen <wcohen@redhat.com>
- Patch to fix op_visualise seg fault on startup.

* Thu Jan 02 2003 Will Cohen <wcohen@redhat.com>
- Correct argument type in daemon/oprofiled.c.
- Correct QTDIR.

* Wed Dec 18 2002 Will Cohen <wcohen@redhat.com>
- Correct reporting of interrupts in oprof_start. 

* Wed Dec 18 2002 Will Cohen <wcohen@redhat.com>
- Rebuilt against new kernel

* Fri Dec 13 2002 Will Cohen <wcohen@redhat.com>
- Use opcontrol in oprof_start.

* Thu Dec 12 2002 Will Cohen <wcohen@redhat.com>
- Correct opvisualise problem.

* Tue Dec 10 2002 Will Cohen <wcohen@redhat.com>
- Add opcontrol, op_dump, op_visualise, ia64 support,
  and debugging information.

* Fri Dec 06 2002 Will Cohen <wcohen@redhat.com>
- Change to use OProfile 0.4 release and kernel support.

* Sat Nov 30 2002 Tim Powers <timp@redhat.com> 0.3-0.20021108.1
- rebuild against current version of libbfd

* Tue Aug 06 2002 Will Cohen <wcohen@redhat.com>
- Change to avoid assumption on executable name

* Fri Aug 02 2002 Will Cohen <wcohen@redhat.com>
- Move to 0.4cvs sources.

* Mon Jul 29 2002 Will Cohen <wcohen@redhat.com>
- localize nr_counter code
- add ia64 arch
- guess path to vmlinux.

* Sun Jul 28 2002 Will Cohen <wcohen@redhat.com>
- adjust structure to fit ia64 oprofile module.

* Thu Jul 25 2002 Will Cohen <wcohen@redhat.com>
- recognize ia64 cpu and events.

* Tue Jul 23 2002 Will Cohen <wcohen@redhat.com>
- changes to turn of warning as error on ia64.

* Tue Jul 23 2002 Will Cohen <wcohen@redhat.com>
- changes to allow compilation on ia64.

* Mon Jul 22 2002 Will Cohen <wcohen@redhat.com>
- pick better Red Hat Linux default image file in /boot.

* Sun Jul 14 2002 Will Cohen <wcohen@redhat.com>
- use older OProfile 0.2 kernel<->daemon API.

* Thu Jul 11 2002 Will Cohen <wcohen@redhat.com>
- avoid oprof_start installing the oprofile module

* Tue Jul 02 2002 Will Cohen <wcohen@redhat.com>
- avoid building and installing the oprofile module

* Tue May 28 2002 Jeff Johnson <jbj@redhat.com>
- create package.
