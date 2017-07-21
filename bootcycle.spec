%define version 1.0

summary: Boot cycle detection
name: bootcycle
version: %{version}
release: 1
source: %{name}-%{version}.tar.gz
license: GPL
exclusiveos: linux
group: Utilities/System
BuildRoot: /var/tmp/%{name}-%{version}-root

%description
This package contains the system tool bootcycle(8) for maintaining a count of
system reboots. Shuts down the system if enough consecutive reboots occur
without the system remaining up for a minimum time.

%prep
%setup
%build

%install
mkdir -p $RPM_BUILD_ROOT/usr/sbin
mkdir -p $RPM_BUILD_ROOT/var/lib/misc
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man8
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d

install -o root -g root -m 750 bootcycle $RPM_BUILD_ROOT/usr/sbin
install -o root -g root -m 750 bootcycle-wait $RPM_BUILD_ROOT/usr/sbin
install -o root -g root -m 644 bootcycle.conf $RPM_BUILD_ROOT/etc
install -o root -g root -m 644 bootcycle.status $RPM_BUILD_ROOT/var/lib/misc
install -o root -g root -m 644 bootcycle.logrotate $RPM_BUILD_ROOT/etc/logrotate.d/bootcycle

gzip -c bootcycle.8 > $RPM_BUILD_ROOT/%{_mandir}/man8/bootcycle.8.gz

%files
/usr/sbin/bootcycle
/usr/sbin/bootcycle-wait
/etc/bootcycle.conf
/var/lib/misc/bootcycle.status
%{_mandir}/man8/bootcycle.8.gz
/etc/logrotate.d/bootcycle

%clean
rm -rf $RPM_BUILD_ROOT

%post
# create the empty log file
touch /var/log/bootcycle.log

# append call to bootcycle to the rc.sysinit file
SYSINIT_FILE=/etc/rc.d/rc.sysinit
BOOTCYCLE_FILE=/usr/sbin/bootcycle

if grep $BOOTCYCLE_FILE $SYSINIT_FILE > /dev/null
then
    # bootcycle already being called by rc.sysinit
    exit
fi

# Append code to rc.sysinit to execute bootcycle after each boot
cat >> $SYSINIT_FILE <<EOF

# Execute the bootcycle program to detect frequent reboots
if [ -x $BOOTCYCLE_FILE ];
then
    setsid $BOOTCYCLE_FILE
fi
EOF
