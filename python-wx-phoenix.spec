%global pkgname wx-phoenix-gtk3
%global py2_builddir python2
%global py3_builddir python3
%global tarname wxPython_Phoenix
%global snapshot_version dev2875+9b743cf
%global with_tests 0
%global sum New implementation of wxPython, a GUI toolkit for Python
%global desc \
wxPython-Phoenix is a is a new implementation of wxPython focused on improving\
speed, maintainability and extensibility. Just like "Classic" wxPython it wraps\
the wxWidgets C++ toolkit and provides access to the user interface portions of\
the wx API, enabling Python applications to have a GUI on Windows, Macs or Unix\
systems with a native look and feel and requiring very little (if any) platform\
specific code.

Name:           python-wx-phoenix
Version:        3.0.3
Release:        0.11.%{snapshot_version}%{?dist}
Summary:        %{sum}
Group:          Development/Languages
License:        LGPLv2+ and wxWidgets
URL:            http://wiki.wxpython.org/ProjectPhoenix
Source0:        http://wxpython.org/Phoenix/snapshot-builds/%{tarname}-%{version}.%{snapshot_version}.tar.gz
Patch0:         unbundle-sip.patch
Patch1:         remove-version-warning.patch
Patch2:         revert-glcanvas-header-changes.patch
Patch3:         revert-listevent-header-changes.patch
Patch4:         revert-propdlg-header-changes.patch

BuildRequires:  doxygen
BuildRequires:  waf
BuildRequires:  wxGTK3-devel
# For tests
%if 0%{?with_tests}
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  numpy python3-numpy
%if 0%{?fedora} < 24
BuildRequires:  python-PyPDF2 python3-PyPDF2
%else
BuildRequires:  python2-PyPDF2 python3-PyPDF2
%endif
%endif

%description %{desc}

%package -n python2-%{pkgname}
Summary:        ${sum}
%{?python_provide:%python_provide python2-%{pkgname}}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-six
BuildRequires:  sip-devel >= 4.19.1
Requires:       python2-six
Requires:       sip >= 4.19.1

%description -n python2-%{pkgname} %{desc}

%package -n python3-%{pkgname}
Summary:        %{sum}
%{?python_provide:%python_provide python3-%{pkgname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-sip-devel >= 4.19.1
BuildRequires:  python3-six
Requires:       python3-sip >= 4.19.1
Requires:       python3-six

%description -n python3-%{pkgname} %{desc}

%package        docs
Group:          Documentation
Summary:        Documentation and samples for wxPython
BuildArch:      noarch

%description docs
Documentation, samples and demo application for wxPython.


%prep
%setup -c -q

mv %{tarname}-%{version}.%{snapshot_version} %{py2_builddir}
pushd %{py2_builddir}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
sed -i -e "s|WX_CONFIG = 'wx-config'|WX_CONFIG = 'wx-config-3.0'|" build.py
rm -rf sip/siplib
popd
cp -a %{py2_builddir} %{py3_builddir}


%build
pushd %{py2_builddir}
DOXYGEN=%{_bindir}/doxygen SIP=%{_bindir}/sip %{__python2} -u build.py dox touch etg --nodoc sip build_py --use_syswx --gtk3 bdist_egg
popd
pushd %{py3_builddir}
DOXYGEN=%{_bindir}/doxygen SIP=%{_bindir}/python3-sip %{__python3} -u build.py dox touch etg --nodoc sip build_py --use_syswx --gtk3
popd


%install
mkdir -p %{buildroot}%{python2_sitearch}
pushd %{py2_builddir}
easy_install -m -d %{buildroot}%{python2_sitearch} -Z dist/*.egg
popd
pushd %{py3_builddir}
%{__python3} build.py install_py --destdir=%{buildroot}
popd
rm -f %{buildroot}%{_bindir}/*


%check
%if 0%{?with_tests}
pushd %{py2_builddir}
xvfb-run -a %{__python2} build.py test --verbose || true
popd
pushd %{py3_builddir}
xvfb-run -a %{__python3} build.py test --verbose || true
popd
%endif


%files -n python2-%{pkgname}
%license %{py2_builddir}/license/*
%{python2_sitearch}/*

%files -n python3-%{pkgname}
%license %{py3_builddir}/license/*
%{python3_sitearch}/*

%files docs
%doc %{py2_builddir}/docs %{py2_builddir}/demo %{py2_builddir}/samples


%changelog
* Sun Mar 26 2017 Scott Talbert <swt@techie.net> - 3.0.3-0.11.dev2875+9b743cf
- Update to dev2875+9b743cf

* Sat Feb 18 2017 Scott Talbert <swt@techie.net> - 3.0.3-0.10.dev2828+929a8af
- Update to dev2828+929a8af

* Sun Feb 05 2017 Scott Talbert <swt@techie.net> - 3.0.3-0.9.dev2768+b0c24a5
- Update to dev2768+b0c24a5

* Fri Feb 03 2017 Scott Talbert <swt@techie.net> - 3.0.3-0.8.dev2747+22cbbb8
- rebuilt

* Sat Dec 10 2016 Scott Talbert <swt@techie.net> - 3.0.3-0.7.dev2747+22cbbb8
- Update to dev2747+22cbbb8

* Tue Dec 06 2016 Scott Talbert <swt@techie.net> - 3.0.3-0.6.dev2733+2de746b
- Update to dev2733+2de746b

* Mon Dec 05 2016 Scott Talbert <swt@techie.net> - 3.0.3-0.5.dev2680+55dda48
- One more patch to fix wxMemoryFSHandler

* Mon Nov 14 2016 Scott Talbert <swt@techie.net> - 3.0.3-0.4.dev2680+55dda48
- Update to dev2680+55dda48

* Thu Oct 06 2016 Scott Talbert <swt@techie.net> - 3.0.3-0.3.dev2472+78ae39a
- Add another patch to fix wxMemoryFSHandler

* Mon Oct 03 2016 Scott Talbert <swt@techie.net> - 3.0.3-0.2.dev2472+78ae39a
- Add patch to fix wxMemoryFSHandler

* Tue Aug 30 2016 Scott Talbert <swt@techie.net> - 3.0.3-0.1.dev2472+78ae39a
- Update to dev2472+78ae39a

* Sun Aug 21 2016 Scott Talbert <swt@techie.net> - 3.0.3-0.1.dev2454+53f3c37
- Update to dev2454+53f3c37

* Sat Jul 30 2016 Scott Talbert <swt@techie.net> - 3.0.3-0.1.dev2295+a108359
- Initial packaging
