%global srcname ly
        

Name:          ly
Version:       1.0.3
Release:       12%{?dist}
Summary:       A TUI display manager
License:       WTFPL
URL:           https://codeberg.org/AnErrupTion/ly
BuildRequires: kernel-devel
BuildRequires: pam-devel
BuildRequires: libxcb-devel
BuildRequires: git
BuildRequires: policycoreutils-devel
BuildRequires: make
BuildRequires: zig
BuildRequires: selinux-policy-devel
Requires:      libxcb
Requires:      pam
Requires:      systemd


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
zig build installnoconf -Ddest_directory=./build -Dcpu=x86_64

cd ../ly-copr/selinux
make -f /usr/share/selinux/devel/Makefile ly.pp


%install
mkdir -p %{buildroot}/etc/
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/lib/systemd/system/
mkdir -p %{buildroot}/etc/pam.d/
mkdir -p %{buildroot}/usr/share/selinux/packages
mkdir -p %{buildroot}/lib/ly
mkdir -p %{buildroot}/usr/lib/systemd/system-preset

cd ly
cp -r build/* %{buildroot}
cp res/ly.service %{buildroot}/usr/lib/systemd/system # I shouldn't have to do this, but with a custom dest_directoy I need to for some reason
cp res/config.ini %{buildroot}/lib/ly

cd ../ly-copr/selinux 
cp ly.pp %{buildroot}/usr/share/selinux/packages

cd ../systemd
cp ly.preset %{buildroot}/usr/lib/systemd/system-preset/99-ly.preset


%post
semodule -n -i /usr/share/selinux/packages/ly.pp
load_policy
restorecon -R /usr/bin/ly; 

systemctl preset ly.service


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
/lib/ly/config.ini
/etc/pam.d/ly
/usr/share/selinux/packages/ly.pp
/usr/lib/systemd/system-preset/99-ly.preset