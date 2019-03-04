%global date 20170216
%global commit0 4b52afba3a0e4a93e47fe485885fe285851577ff
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           ldoce5viewer
Version:        0
Release:        5.%{date}git%{shortcommit0}%{?dist}
Summary:        Viewer Application for the Longman Dictionary (LDOCE 5)
License:        GPLv3+ and Public Domain
URL:            https://hakidame.net/ldoce5viewer/
Source:         https://github.com/ciscorn/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{version}-%{date}git%{shortcommit0}.tar.gz
# Fix for icon convertin process
# Upstream ref: https://github.com/ciscorn/ldoce5viewer/pull/54
Patch0:         https://github.com/ciscorn/%{name}/commit/728158aea71013f1122e915ca4bf767ffb29df5d.patch#/%{name}-fix-icon-converting-process.patch
# Add Appstream Metadata
# Upstream ref: https://github.com/ciscorn/ldoce5viewer/pull/55
Patch1:         https://github.com/ciscorn/%{name}/commit/66ad086d225b68e45c9785fd21957597e1e8d89b.patch#/%{name}-Add-AppStream-Metadata-file.patch
# Remove 0-sized and unused files
# Upstream ref: https://github.com/ciscorn/ldoce5viewer/pull/56
Patch2:         https://github.com/ciscorn/%{name}/commit/3840ab0a6121e7061c11e5a30b0ebc4dccbdc40e.patch#/%{name}-Remove-0-sized-and-unused-files.patch
BuildArch:      noarch

BuildRequires:  /usr/bin/git
BuildRequires:  desktop-file-utils
BuildRequires:  python2-devel
BuildRequires:  %{py2_dist whoosh}
BuildRequires:  %{py2_dist lxml}
BuildRequires:  PyQt4-devel
BuildRequires:  libappstream-glib
# Required to regenerate icons
BuildRequires:  ImageMagick
BuildRequires:  inkscape
BuildRequires:  python2-pillow

Requires:       gstreamer-python
Requires:       gstreamer-plugins-good
Requires:       gstreamer-plugins-ugly
Requires:       hicolor-icon-theme
Requires:       %{py2_dist whoosh}
Requires:       %{py2_dist lxml}
Requires:       PyQt4


%description
The %{name} is an alternative dictionary viewer for the
Longman Dictionary of Contemporary English 5th Edition (LDOCE 5).

Features:
    - Comprehensive instant search.
    - Pleasant to use.
    - Clean and readable.
    - Full sound playback.
    - Access virtually all of the LDOCE content.
    - Powerful advanced search.
    - Search in definitions and example sentences.
    - Clipboard monitoring.

Note: Before you can use the app, you have to install
      the original LDOCE 5 software from the DVD-ROM.


%prep
%autosetup -S git -n %{name}-%{commit0}

# Update the software version.
sed -i "s#\(__version__.*\ =\ \).*#\1'%{date}'#" %{name}/__init__.py

# Shebang removal
for i in %{name}/__init__.py %{name}/utils/compat.py %{name}.desktop; do
 sed '1{\@^#!/usr/bin/env@d}' $i > $i.tmp &&
 touch -r $i $i.tmp &&
 mv $i.tmp $i
done

# Be sure all necessary files will be regenerated.
make clean
make -C %{name}/qtgui/resources/icons clean

# Correct EOL (preserve timestamps).
for i in COPYING.txt LICENSE.txt; do
    sed 's#\r##g' $i > $i.tmp && \
    touch -r $i $i.tmp && \
    mv $i.tmp $i
done

# Create simple installation instruction.
cat  > INSTALL.txt <<EOF
1. Copy the 'ldoce5.data' directory from the LDOCE5 DVD-ROM [1]
   to an arbitrary location.

2. Start the %{name}

3. The application will ask you the location where you put 'ldoce5.data'.

More information can be obtained from [2].

[1] http://www.longmandictionariesonline.com/
[2] https://hakidame.net/ldoce5viewer/manual/
EOF


%build
%make_build -C %{name}/qtgui/resources/icons
%make_build qtui qtresource
%py2_build


%install
%py2_install

# install desktop file
desktop-file-install \
    --delete-original \
    --dir=%{buildroot}%{_datadir}/applications \
    %{name}.desktop

# install icon file
install -p -m 0644 -D %{name}/qtgui/resources/%{name}.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

# install and validate appdata
install -p -m 0644 -D %{name}.appdata.xml %{buildroot}/%{_datadir}/appdata/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/*.appdata.xml


%files
%doc INSTALL.txt README.md
%license COPYING.txt LICENSE.txt
%{_bindir}/%{name}
%{python2_sitelib}/*
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/*.appdata.xml
%exclude %{python2_sitelib}/%{name}/qtgui/ui/Makefile
%exclude %{python2_sitelib}/%{name}/qtgui/resources/Makefile
%exclude %{python2_sitelib}/%{name}/qtgui/resources/icons/Makefile
%exclude %{python2_sitelib}/%{name}/qtgui/resources/icons/icongen.*


%changelog
* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0-5.20170216git4b52afb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0-4.20170216git4b52afb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 27 2018 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0-3.20170216git4b52afb
- Add patch to remove 0-sized and unused files.

* Tue Feb 27 2018 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0-2.20170216git4b52afb
- Modernize spec file,
- Update to the latest version.

* Fri May 23 2014 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0-1.20140224
- Initial RPM release.
