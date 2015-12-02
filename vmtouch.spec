Name: vmtouch
Summary: the Virtual Memory Toucher
Version: 1.0.1
Release: 1
Source: %{name}-%{name}-%{version}.zip
Vendor: hoytech
License: GPL
ExclusiveOS: linux
Group: Applications/System
Provides: %{name}
URL: https://github.com/hoytech/vmtouch/
BuildRoot: %{_tmppath}/%{name}-%{version}-root
# do not generate debugging packages by default - older versions of rpmbuild
# may instead need:
#%define debug_package %{nil}
%debug_package %{nil}
# macros for finding system files to update at install time (pci.ids, pcitable)
Requires: kernel

%description
vmtouch is a tool for learning about and controlling
the file system cache of unix and unix-like systems.
It is BSD licensed so you can basically do whatever
you want with it.

%prep
%setup -n %{name}-%{name}-%{version}

%build
make clean
make

%install
make install BINDIR=%{buildroot}%{_sbindir} MANDIR=%{buildroot}%{_mandir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_sbindir}/vmtouch
%{_sbindir}/watch-vmtouch
%{_mandir}/man8/vmtouch.8.gz
%doc CHANGES
%doc README
%doc TODO

%changelog
* Fri Oct 16 2015 1.0.1
  * Change default max file size (specified with -m) to
    SIZE_MAX instead of 500m. This is 4G on 32-bit systems
    and effectively unlimited on 64-bit systems.
    (Thanks Erik Garrison)
  * -p mode which lets you view/touch/evict/lock ranges of
    files instead of just whole files. (Thanks Justas Lavišius)
  * Update debian packaging files. (Thanks Luka Blaskovic)
  * Fix bug that prevented you from trying to crawl your
    entire filesystem from the root.
  * Fix to work with glibc 2.20. (Thanks Jim Garrison)
  * Fix format string warning when compiling with clang.
    (Thanks Mikolaj Golub)
  * Cleaner and better Makefile. (Thanks Emmanuel Kasper and
    Mikolaj Golub)
  * Don't double-count the same file that just happens to have
    multiple hard-links to it. (Thanks Carsten Otto)
  * Add option to wait for daemon mode to finish mlocking.
    (Thanks Kristofer Karlsson)
* Mon Dec 4 2012 0.8.0
  * Patch from Marc Brooker: avoid overflowing stack when
    allocating array for mincore() output
  * Patch from Federico Lucifredi: Avoid ugly NaNs in output
  * Full OS X support: msync(2) evicts pages on this system
  * HP-UX support from Shane Seymour (thanks!)
  * Patch from soarpenguin: detect invalid size formats


