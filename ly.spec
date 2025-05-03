%define relabel_files() restorecon -R /usr/bin/ly; 


Name:          ly
Version:       v1.0.3
Release:       %{?dist}
Summary:       A TUI display manager
License:       WTFPL
URL:           https://codeberg.org/AnErrupTion/ly
BuildRequires: pam-devel
BuildRequires: libxcb-devel
BuildRequires: git
BuildRequires: policycoreutils-devel
BuildRequires: make
BuildRequires: zig
BuildRequires: selinux-policy-devel
Requires:      libxcb
Requires:      pam


%description
Ly is a lightweight TUI (ncurses-like) display manager for Linux and BSD.


%prep
git clone https://codeberg.org/AnErrupTion/ly
cd ly
git checkout v1.0.3
cd ..

git clone https://github.com/tywil04/ly-copr


%build
cd ly
zig build

cd ../ly-copr/selinux
make -f /usr/share/selinux/devel/Makefile ly.pp


%install
mkdir -p %{buildroot}/etc/
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/lib/systemd/system/
mkdir -p %{buildroot}/etc/pam.d/
mkdir -p %{buildroot}/usr/share/selinux/packages

cd ly
zig build installexe -Ddest_directory=%{buildroot}
cp res/ly.service %{buildroot}/usr/lib/systemd/system # I shouldn't have to do this, but with a custom dest_directoy I need to for some reason

cd ../ly-copr/selinux 
cp ly.pp %{buildroot}/usr/share/selinux/packages


%post
semodule -n -i /usr/share/selinux/packages/ly.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    %relabel_files
fi;


%postun
if [ $1 -eq 0 ]; then
    semodule -n -r ly
fi;


%files
/usr/bin/ly
/usr/lib/systemd/system/ly.service
/etc/ly/lang/es.ini
/etc/ly/lang/pt.ini
/etc/ly/lang/ru.ini
/etc/ly/lang/en.ini
/etc/ly/lang/fr.ini
/etc/ly/lang/ro.ini
/etc/ly/lang/cat.ini
/etc/ly/lang/cs.ini
/etc/ly/lang/de.ini
/etc/ly/lang/it.ini
/etc/ly/lang/pl.ini
/etc/ly/lang/pt_BR.ini
/etc/ly/lang/sr.ini
/etc/ly/lang/sv.ini
/etc/ly/lang/tr.ini
/etc/ly/lang/uk.ini
/etc/ly/xsetup.sh
/etc/ly/wsetup.sh
/etc/ly/config.ini
/etc/pam.d/ly
/usr/share/selinux/packages/ly.pp
