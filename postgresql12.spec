# configurable build options
%{!?enable_icu:%global enable_icu 1}
%{!?enable_kerberos:%global enable_kerberos 1}
%{!?enable_ldap:%global enable_ldap 1}
%{!?enable_pam:%global enable_pam 1}
%{!?ebable_plpython2:%global enable_plpython2 1}
%{!?enable_pltcl:%global enable_pltcl 1}
%{!?enable_plperl:%global enable_plperl 1}
%{!?enable_ssl:%global enable_ssl 1}
%{!?enable_xml:%global enable_xml 1}
%{!?enable_systemd:%global enable_systemd 1}
%{!?enable_sdt:%global enable_sdt 1}
%{!?enable_selinux:%global enable_selinux 1}
#broken
%{!?enable_plpython3:%global enable_plpython3 0}

%global sname			postgres

%global cmd_update_alt		%{_sbindir}/update-alternatives

%global pg_version_major	12
%global pg_version_prev		11

%global pg_alternative_prio	1200

%global pg_prefix		/usr/postgresql-%pg_version_major
%global pg_bindir		%pg_prefix/bin
%global pg_includedir		%pg_prefix/include
%global pg_mandir		%pg_prefix/share/man
%global pg_datadir		%pg_prefix/share
%global pg_libdir		%pg_prefix/%{_lib}
%global pg_docdir		%pg_prefix/share/doc
%global pg_extdir		%pg_datadir/extension
%global pg_dbdir		/var/lib/postgresql/%pg_version_major
%global pg_dbroot		/var/lib/postgresql
%global pg_rundir		/var/run/postgresql
%global pg_pamdir		%{_sysconfdir}/pam.d

%global pg_prev_prefix		/usr/postgresql-%pg_version_prev
%global pg_prev_bindir		%pg_prev_prefix/bin
%global pg_prev_dbdir		/var/lib/postgresql/%pg_version_prev

%global pg_systemd_service	postgresql-%pg_version_major.service
%global pg_sysvinit_service	postgresql-%pg_version_major

%global pg_libs_conf		%pg_datadir/postgresql-%pg_version_major-libs.conf
%global pg_etc_sysconfig	/etc/sysconfig/pgsql/%pg_version_major

%global pkg_prefix		postgresql%pg_version_major
%global pkg_server		%pkg_prefix-server
%global pkg_libs		%pkg_prefix-libs
%global pkg_docs		%pkg_prefix-docs
%global pkg_contrib		%pkg_prefix-contrib
%global pkg_devel		%pkg_prefix-devel
%global pkg_plperl		%pkg_prefix-plperl
%global pkg_pltcl		%pkg_prefix-pltcl
%global pkg_plpython2		%pkg_prefix-plpython2
%global pkg_pypython3		%pkg_prefix-plpython3

%global requires_main		Requires: %{name}%{?_isa} = %{version}-%{release}
%global requires_server		Requires: %{name}-server%{?_isa} = %{version}-%{release}
%global requires_libs		Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%global requires_libpq5		Requires: %{name}-libpq5%{?_isa} = %{version}-%{release}
%global requires_server_devel	Requires: %{name}-server-devel%{?_isa} = %{version}-%{release}

#	--htmldir=%pg_docdir/html \\\

%global configure_call \\\
	./configure \\\
	--enable-rpath \\\
	--sysconfdir=%{_sysconfdir} \\\
	--prefix=%pg_prefix \\\
	--bindir=%pg_bindir \\\
	--includedir=%pg_includedir \\\
	--mandir=%pg_mandir \\\
	--datadir=%pg_datadir \\\
	--libdir=%pg_libdir \\\
	--with-system-tzdata=%{_datadir}/zoneinfo \\\
	--docdir=%pg_docdir \\\
	--without-llvm \\\
	--enable-nls \\\
	%{?enable_icu:--with-icu} \\\
	%{?enable_plperl:--with-perl} \\\
	%{?enable_pltcl:--with-tcl --with-tclconfig=%{_libdir}} \\\
	%{?enable_plpython2:--with-python} \\\
	%{?enable_plpython3:--with-python} \\\
	%{?enable_ssl:--with-openssl} \\\
	%{?enable_pam:--with-pam} \\\
	%{?enable_kerberos:--with-gssapi} \\\
	%{?enable_sdt:--enable-dtrace} \\\
	--with-uuid=e2fs \\\
	%{?enable_xml:--with-libxml --with-libxslt} \\\
	%{?enable_ldap:--with-ldap} \\\
	%{?enable_selinux:--with-selinux}

%global generate_file \\\
	sed -e 's~@PG_VERSION_MAJOR@~%pg_version_major~g' | \\\
	sed -e 's~@PG_VERSION_PREV@~%pg_version_prev~g' | \\\
	sed -e 's~@PG_DOCDIR@~%pg_docdir~g' | \\\
	sed -e 's~@PG_BINDIR@~%pg_bindir~g' | \\\
	sed -e 's~@PG_DBDIR@~%pg_dbdir~g' | \\\
	sed -e 's~@PG_DBROOT@~%pg_dbroot~g' | \\\
	sed -e 's~@PG_PREV_BINDIR@~%pg_prev_bindir~g' | \\\
	sed -e 's~@PG_PREV_DBDIR@~%pg_prev_dbdir~g' | \\\
	sed -e 's~@PG_RUNDIR@~%pg_rundir~g'

Summary:	PostgreSQL client programs and libraries
Name:		postgresql12
Version:	12.2
Release:	5
License:	PostgreSQL
Url:		https://www.postgresql.org/

Source0:	postgres-%{version}.tar.gz

BuildRequires:	perl
BuildRequires:	glibc-devel
BuildRequires:	bison
BuildRequires:	flex >= 2.5.31
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	readline-devel
BuildRequires:	zlib-devel >= 1.0.4
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	docbook-xsl-stylesheets docbook5-xsl-stylesheets
BuildRequires:	gettext >= 0.10.35
BuildRequires:	libuuid-devel

Requires:	/sbin/ldconfig
Requires:	zlib >= 1.0.4
Requires:	libuuid1

%{?enable_icu:BuildRequires:		libicu-devel}
%{?enable_icu:Requires:			libicu}
%{?enable_kerberos:BuildRequires:	krb5-devel}
%{?enable_ldap:BuildRequires:		openldap2-devel}
%{?enable_pam:BuildRequires:		pam-devel}
%{?enable_plpython2:BuildRequires:	python2-devel}
%{?enable_plpython3:BuildRequires:	python3-devel}
%{?enable_pltcl:BuildRequires:		tcl-devel}
%{?enable_sdt:BuildRequires:		systemtap-sdt-devel}
%{?enable_selinux:BuildRequires:	libselinux-devel >= 2.0.93}
%{?enable_selinux:BuildRequires:	selinux-policy}
%{?enable_selinux:Requires:		libselinux-devel}
%{?enable_selinux:Requires:		selinux-policy}
%{?enable_ssl:Requires:			libopenssl1_1}
%{?enable_ssl:BuildRequires:		libopenssl-1_1-devel}
%{?enable_xml:BuildRequires:		libxml2-devel libxslt-devel}
%{?enable_xml:Requires:			libxml2 libxslt}

%requires_libs

Requires(post):		%cmd_update_alt
Requires(postun):	%cmd_update_alt

Provides:	postgres >= %{version}-%{release}

%description
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The base postgresql package contains the client programs that you'll need to
access a PostgreSQL DBMS server, as well as HTML documentation for the whole
system. These client programs can be located on the same machine as the
PostgreSQL server, or on a remote machine that accesses a PostgreSQL server
over a network connection. The PostgreSQL server can be found in the
%pkg_server sub-package.

If you want to manipulate a PostgreSQL database on a local or remote PostgreSQL
server, you need this package. You also need to install this package
if you're installing the %pkg_server package.

%package libs
Summary:	The shared libraries required for any PostgreSQL clients
Provides:	postgresql-libs = %pg_version_major
Requires:	libopenssl1_0_0
%requires_libpq5

%description libs
The %pkg_libs package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package server
Summary:	The programs needed to create and run a PostgreSQL server
%requires_main
%requires_libs
Requires(pre):		/usr/sbin/useradd /usr/sbin/groupadd
Requires(post):		/sbin/ldconfig
Requires(postun):	/sbin/ldconfig
Requires:		/usr/sbin/useradd, /sbin/chkconfig
Provides:		postgresql-server >= %{version}-%{release}

%description server
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The %pkg_server package contains the programs needed to create
and run a PostgreSQL server, which will in turn allow you to create
and maintain PostgreSQL databases.

%package docs
Summary:	Extra documentation for PostgreSQL
Provides:	postgresql-docs >= %{version}-%{release}

%description docs
The %pkg_docs package includes the SGML source for the documentation
as well as the documentation in PDF format and some extra documentation.
Install this package if you want to help with the PostgreSQL documentation
project, or if you want to generate printed documentation. This package also
includes HTML version of the documentation.

%package contrib
Summary:	Contributed source and binaries distributed with PostgreSQL
%requires_main
%requires_libs
Provides:	postgresql-contrib >= %{version}-%{release}

%description contrib
The %pkg_contrib package contains various extension modules that are
included in the PostgreSQL distribution.

## libpq -- postgresql client library
%package libpq5
Summary:	Contributed source and binaries distributed with PostgreSQL

%description libpq5
Postgresql client library

%files libpq5
%pg_libdir/libpq.so.*
%pg_datadir/locale/*/LC_MESSAGES/libpq5*.mo

%post libpq5
%cmd_update_alt --install %_libdir/libpq.so.5 pgsql-libpq5 %pg_libdir/libpq.so.5 %pg_alternative_prio

%postun libpq5
%cmd_update_alt --remove pgsql-libpq5 %pg_libdir/libpq.so.5

%package server-devel
Summary:	PostgreSQL development files for server extensions
Requires:	zlib
%{?enable_icu:Requires:	libicu}
%{?enable_pam:Requires:	pam}
%{?enable_xml:Requires:	libxml2 libxslt}

%description server-devel
PostgreSQL server development header files and libraries

%files server-devel
%defattr(-,root,root)
%pg_libdir/pgxs/*
%{_bindir}/pg_config-%pg_version_major

## generic devel package
%package devel
Summary:	PostgreSQL development header files and libraries
%requires_main
%requires_libs
%requires_server_devel

%description devel
The %pkg_devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server. It also contains the ecpg
Embedded C Postgres preprocessor. You need to install this package if you want
to develop applications which will interact with a PostgreSQL server.

%files devel -f pg_devel.lst
%defattr(-,root,root)
%pg_includedir/*
%pg_bindir/ecpg
%pg_libdir/libpq.so
%pg_libdir/libecpg.so
%pg_libdir/libpq.a
%pg_libdir/libecpg.a
%pg_libdir/libecpg_compat.so
%pg_libdir/libecpg_compat.a
%pg_libdir/libpgcommon.a
%pg_libdir/libpgcommon_shlib.a
%pg_libdir/libpgport.a
%pg_libdir/libpgport_shlib.a
%pg_libdir/libpgtypes.so
%pg_libdir/libpgtypes.a
%pg_libdir/pkgconfig/*
%pg_mandir/man1/ecpg.*
%pg_mandir/man3/*
%pg_mandir/man7/*


%if %enable_plperl
%package plperl
Summary:	The Perl procedural language for PostgreSQL
%requires_main
%requires_server
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Provides:	postgresql-plperl >= %{version}-%{release}

%description plperl
The %pkg_plperl package contains the PL/Perl procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Perl.

%endif

%if %enable_plpython2
%package plpython2
Summary:	The Python procedural language for PostgreSQL
%requires_main
%requires_server
Provides:	postgresql-plpython >= %{version}-%{release}
Provides:	%{name}-plpython2%{?_isa} = %{version}-%{release}
Requires:	libpython2_7-1_0

%description plpython2
The %pkg_plpython2 package contains the PL/Python procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Python.

%endif

%if %enable_plpython3
%package plpython3
Summary:	The Python3 procedural language for PostgreSQL
%requires_main
%requires_server
Provides:	postgresql-plpython3 >= %{version}-%{release}
Requires:	python3-libs

%description plpython3
The %pkg_plpython3 package contains the PL/Python3 procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Python 3.

%endif

%if %enable_pltcl
%package pltcl
Summary:	The Tcl procedural language for PostgreSQL
%requires_main
%requires_server
Requires:	tcl
Provides:	postgresql-pltcl >= %{version}-%{release}

%description pltcl
PostgreSQL is an advanced Object-Relational database management
system. The %pkg_pltcl package contains the PL/Tcl language
for the backend.
%endif

%global __perl_requires postgresql-%pg_version_major-filter-requires-perl-Pg.sh

%prep
%setup -q -n %{sname}-%{version}
./autogen.sh

%build

# plpython requires separate configure/build runs to build against python 2
# versus python 3. Our strategy is to do the python 3 run first, then make
# distclean and do it again for the "normal" build. Note that the installed
# Makefile.global will reflect the python 2 build, which seems appropriate
# since that's still considered the default plpython version.
%if %enable_plpython3

export PYTHON=/usr/bin/python3

%{configure_call}

# We need to build PL/Python and a few extensions:
# Build PL/Python
cd src/backend
MAKELEVEL=0 %{__make} submake-generated-headers
cd ../..
cd src/pl/plpython
%{__make} all
cd ..
# save built form in a directory that "make distclean" won't touch
%{__cp} -a plpython plpython3
cd ../..
# Build some of the extensions with PY3 support
for p3bl in %{python3_build_list} ; do
	p3blpy3dir="$p3bl"3
	pushd contrib/$p3bl
	MAKELEVEL=0 %{__make} %{?_smp_mflags} all
	cd ..
	# save built form in a directory that "make distclean" won't touch
	%{__cp} -a $p3bl $p3blpy3dir
	popd
done
# must also save this version of Makefile.global for later
%{__cp} src/Makefile.global src/Makefile.global.python3

%{__make} distclean

%endif

unset PYTHON
# Explicitly run Python2 here -- in future releases,
# Python3 will be the default.
export PYTHON=/usr/bin/python2

# Normal (not python3) build begins here
%{configure_call}

MAKELEVEL=0 %{__make} %{?_smp_mflags} all docs
%{__make} %{?_smp_mflags} -C contrib all
#%if %enable_uuid
#%{__make} %{?_smp_mflags} -C contrib/uuid-ossp all
#%endif

%install
%{__rm} -rf %buildroot

%{__make} DESTDIR=%buildroot install install-docs

%if %enable_plpython3
	%{__mv} src/Makefile.global src/Makefile.global.save
	%{__cp} src/Makefile.global.python3 src/Makefile.global
	touch -r src/Makefile.global.save src/Makefile.global
	# Install PL/Python3
	pushd src/pl/plpython3
	%{__make} DESTDIR=%buildroot install
	popd

	for p3bl in %{python3_build_list} ; do
		p3blpy3dir="$p3bl"3

		# Install jsonb_plpython3
		pushd contrib/$p3blpy3dir
		%{__make} DESTDIR=%buildroot install
		popd
	done

	%{__mv} -f src/Makefile.global.save src/Makefile.global
%endif

%{__make} -C contrib DESTDIR=%buildroot install
#%if %enable_uuid
#%{__make} -C contrib/uuid-ossp DESTDIR=%buildroot install
#%endif

# multilib header hack; note pg_config.h is installed in two places!
# we only apply this to known Red Hat multilib arches, per bug #177564
#case `uname -i` in
#	i386 | x86_64 | ppc | ppc64 | s390 | s390x)
#		%{__mv} %buildroot/%pg_includedir/pg_config.h %buildroot/%pg_includedir/pg_config_`uname -i`.h
#		%{__install} -m 644 postgresql-%pg_version_major-pg_config.h %buildroot/%pg_includedir/pg_config.h
#		%{__mv} %buildroot/%pg_includedir/server/pg_config.h %buildroot/%pg_includedir/server/pg_config_`uname -i`.h
#		%{__install} -m 644 postgresql-%pg_version_major-pg_config.h %buildroot/%pg_includedir/server/pg_config.h
#		%{__mv} %buildroot/%pg_includedir/ecpg_config.h %buildroot/%pg_includedir/ecpg_config_`uname -i`.h
#		%{__install} -m 644 postgresql-%pg_version_major-ecpg_config.h %buildroot/%pg_includedir/ecpg_config.h
#		;;
#	*)
#	;;
#esac

%{__mkdir} -p %buildroot/%pg_pamdir
cat postgresql.pam.in | %generate_file > %buildroot/%pg_pamdir/postgresql-%pg_version_major.pam

# This is only for systemd supported distros:
%if %enable_systemd

cat postgresql-setup.in | %generate_file > %buildroot/%pg_bindir/postgresql-setup
chmod 755 %buildroot/%pg_bindir/postgresql-setup

cat postgresql-check-db-dir.in | %generate_file > %buildroot/%pg_bindir/postgresql-check-db-dir
chmod 755 %buildroot/%pg_bindir/postgresql-check-db-dir

%{__mkdir} -p %buildroot/%{_unitdir}
cat postgresql.service.in | %generate_file > %buildroot/%{_unitdir}/%pg_systemd_service

%else

%{__install} -d %buildroot/%{_initrddir}
cat postgresql.init.in | %generate_file > %buildroot/%{_initrddir}/%pg_sysvinit_service
chmod 755 %buildroot/%{_initrddir}/%pg_sysvinit_service

%endif

# Create the directory for sockets.
%{__install} -d -m 755 %buildroot/%pg_rundir

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
%{__install} -d -m 700 %buildroot/%pg_dbdir/data

# backups of data go here...
%{__install} -d -m 700 %buildroot/%pg_dbdir/backups

# Create the multiple postmaster startup directory
%{__install} -d -m 700 %buildroot/%pg_etc_sysconfig

# Install linker conf file under postgresql installation directory.
# We will install the latest version via alternatives.
%{__install} -d -m 755 %buildroot/%pg_datadir/

cat postgresql-libs.conf.in | %generate_file > %buildroot/%pg_libs_conf
chmod u=rw,go=r %buildroot/%pg_libs_conf

mkdir -p %buildroot/%{_bindir}
ln -s %pg_bindir/pg_config %buildroot/%{_bindir}/pg_config-%pg_version_major

# Fix some more documentation
# gzip doc/internals.ps
#%{__mkdir} -p %buildroot/%pg_docdir/html
#%{__mv} doc/src/sgml/html doc
#%{__mkdir} -p %buildroot/%pg_mandir/

# initialize file lists
%{__cp} /dev/null main.lst
%{__cp} /dev/null libs.lst
%{__cp} /dev/null server.lst
%{__cp} /dev/null devel.lst
%{__cp} /dev/null plperl.lst
%{__cp} /dev/null pltcl.lst
%{__cp} /dev/null plpython2.lst
%{__cp} /dev/null pg_plpython3.lst
%{__cp} /dev/null pg_checksums.lst

%find_lang ecpg-%pg_version_major
%find_lang ecpglib6-%pg_version_major
%find_lang initdb-%pg_version_major
%find_lang pg_archivecleanup-%pg_version_major
%find_lang pg_basebackup-%pg_version_major
%find_lang pg_checksums-%pg_version_major
%find_lang pg_config-%pg_version_major
%find_lang pg_controldata-%pg_version_major
%find_lang pg_ctl-%pg_version_major
%find_lang pg_dump-%pg_version_major
%find_lang pg_resetwal-%pg_version_major
%find_lang pg_rewind-%pg_version_major
%find_lang pg_test_fsync-%pg_version_major
%find_lang pg_test_timing-%pg_version_major
%find_lang pg_upgrade-%pg_version_major
%find_lang pg_waldump-%pg_version_major
%find_lang pgscripts-%pg_version_major
%if %enable_plperl
%find_lang plperl-%pg_version_major
cat plperl-%pg_version_major.lang > pg_plperl.lst
%endif
%find_lang plpgsql-%pg_version_major
%if %enable_plpython2
%find_lang plpython-%pg_version_major
cat plpython-%pg_version_major.lang > pg_plpython2.lst
%endif
%if %enable_plpython3
# plpython3 shares message files with plpython
%find_lang plpython-%pg_version_major
cat plpython-%pg_version_major.lang >> pg_plpython3.lst
%endif

%if %enable_pltcl
%find_lang pltcl-%pg_version_major
cat pltcl-%pg_version_major.lang > pg_pltcl.lst
%endif
%find_lang postgres-%pg_version_major
%find_lang psql-%pg_version_major

touch pg_libs.lst
cat pg_config-%pg_version_major.lang ecpg-%pg_version_major.lang ecpglib6-%pg_version_major.lang > pg_devel.lst
cat initdb-%pg_version_major.lang pg_ctl-%pg_version_major.lang psql-%pg_version_major.lang pg_dump-%pg_version_major.lang pg_basebackup-%pg_version_major.lang pg_rewind-%pg_version_major.lang pg_upgrade-%pg_version_major.lang pg_test_timing-%pg_version_major.lang pg_test_fsync-%pg_version_major.lang pg_archivecleanup-%pg_version_major.lang pg_waldump-%pg_version_major.lang pgscripts-%pg_version_major.lang > pg_main.lst
cat postgres-%pg_version_major.lang pg_resetwal-%pg_version_major.lang pg_checksums-%pg_version_major.lang pg_controldata-%pg_version_major.lang plpgsql-%pg_version_major.lang > pg_server.lst

%pre server
groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
useradd -M -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
	-c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :

%post server
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
%if %enable_systemd
   /bin/systemctl daemon-reload >/dev/null 2>&1 || :
   %systemd_post %pg_systemd_service
%else
   chkconfig --add %pg_sysvinit_service
%endif
fi

# postgres' .bash_profile.
# We now don't install .bash_profile as we used to in pre 9.0. Instead, use cat,
# so that package manager will be happy during upgrade to new major version.
echo "[ -f /etc/profile ] && source /etc/profile
PGDATA=%pg_dbdir/data
export PGDATA
# If you want to customize your settings,
# Use the file below. This is not overridden
# by the RPMS.
[ -f /var/lib/pgsql/.pgsql_profile ] && source /var/lib/pgsql/.pgsql_profile" > /var/lib/pgsql/.bash_profile
chown postgres: /var/lib/pgsql/.bash_profile
chmod 700 /var/lib/pgsql/.bash_profile

%preun server
if [ $1 -eq 0 ] ; then
%if %enable_systemd
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable %pg_systemd_service >/dev/null 2>&1 || :
	/bin/systemctl stop %pg_systemd_service >/dev/null 2>&1 || :
%else
	/sbin/service %pg_sysvinit_service condstop >/dev/null 2>&1
	chkconfig --del %pg_sysvinit_service

%endif
fi

%postun server
/sbin/ldconfig
%if %enable_systemd
 /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
 /sbin/service %pg_sysvinit_service condrestart >/dev/null 2>&1
%endif
if [ $1 -ge 1 ] ; then
 %if %enable_systemd
	# Package upgrade, not uninstall
	/bin/systemctl try-restart %pg_systemd_service >/dev/null 2>&1 || :
 %else
   /sbin/service %pg_sysvinit_service condrestart >/dev/null 2>&1
 %endif
fi

# Create alternatives entries for common binaries and man files
%post

for cmd in pg_ctl pg_config psql clusterdb createdb createuser dropdb dropuser pg_basebackup pg_dump pg_dumpall pg_restore reindexdb vacuumdb ; do
    %cmd_update_alt --install %{_bindir}/${cmd}        pgsql-${cmd}    %pg_bindir/${cmd}        %pg_alternative_prio
    %cmd_update_alt --install %{_mandir}/man1/${cmd}.1 pgsql-${cmd}man %pg_mandir/man1/${cmd}.1 %pg_alternative_prio
done

%post libs
%cmd_update_alt --install /etc/ld.so.conf.d/postgresql-pgdg-libs.conf pgsql-ld-conf %pg_libs_conf %pg_alternative_prio
/sbin/ldconfig

# Drop alternatives entries for common binaries and man files
%postun
if [ "$1" -eq 0 ]; then
  for cmd in psql clusterdb createdb createuser dropdb dropuser pg_basebackup pg_dump pg_dumpall pg_restore reindexdb vacuumdb ; do
    %cmd_update_alt --remove pgsql-${cmd}    %pg_bindir/psql
    %cmd_update_alt --remove pgsql-${cmd}man %pg_mandir/man1/${cmd}.1
  done
fi

%postun libs
if [ "$1" -eq 0 ]; then
  %cmd_update_alt --remove pgsql-ld-conf %pg_libs_conf
  /sbin/ldconfig
fi

%clean
%{__rm} -rf %buildroot


%files -f pg_main.lst
%defattr(-,root,root)
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES COPYRIGHT
%pg_bindir/clusterdb
%pg_bindir/createdb
%pg_bindir/createuser
%pg_bindir/dropdb
%pg_bindir/dropuser
%pg_bindir/pgbench
%pg_bindir/pg_archivecleanup
%pg_bindir/pg_basebackup
%pg_bindir/pg_config
%pg_bindir/pg_dump
%pg_bindir/pg_dumpall
%pg_bindir/pg_isready
%pg_bindir/pg_restore
%pg_bindir/pg_rewind
%pg_bindir/pg_test_fsync
%pg_bindir/pg_test_timing
%pg_bindir/pg_receivewal
%pg_bindir/pg_upgrade
%pg_bindir/pg_waldump
%pg_bindir/psql
%pg_bindir/reindexdb
%pg_bindir/vacuumdb
%pg_datadir/errcodes.txt
%pg_mandir/man1/clusterdb.*
%pg_mandir/man1/createdb.*
%pg_mandir/man1/createuser.*
%pg_mandir/man1/dropdb.*
%pg_mandir/man1/dropuser.*
%pg_mandir/man1/pgbench.1
%pg_mandir/man1/pg_archivecleanup.1
%pg_mandir/man1/pg_basebackup.*
%pg_mandir/man1/pg_config.*
%pg_mandir/man1/pg_dump.*
%pg_mandir/man1/pg_dumpall.*
%pg_mandir/man1/pg_isready.*
%pg_mandir/man1/pg_receivewal.*
%pg_mandir/man1/pg_restore.*
%pg_mandir/man1/pg_rewind.1
%pg_mandir/man1/pg_test_fsync.1
%pg_mandir/man1/pg_test_timing.1
%pg_mandir/man1/pg_upgrade.1
%pg_mandir/man1/pg_waldump.1
%pg_mandir/man1/psql.*
%pg_mandir/man1/reindexdb.*
%pg_mandir/man1/vacuumdb.*

%files docs
%defattr(-,root,root)
#%doc doc/src/*
#%doc *-A4.pdf
#%doc src/tutorial
#%doc doc/html
%pg_docdir/*
%exclude %pg_docdir/extension/*.example

%files contrib
%defattr(-,root,root)
%pg_docdir/extension/*.example
%pg_libdir/_int.so
%pg_libdir/adminpack.so
%pg_libdir/amcheck.so
%pg_libdir/auth_delay.so
%pg_libdir/autoinc.so
%pg_libdir/auto_explain.so
%pg_libdir/bloom.so
%pg_libdir/btree_gin.so
%pg_libdir/btree_gist.so
%pg_libdir/citext.so
%pg_libdir/cube.so
%pg_libdir/dblink.so
%pg_libdir/earthdistance.so
%pg_libdir/file_fdw.so*
%pg_libdir/fuzzystrmatch.so
%pg_libdir/insert_username.so
%pg_libdir/isn.so
%pg_libdir/hstore.so
%if %enable_plperl
%pg_libdir/hstore_plperl.so
%pg_libdir/jsonb_plperl.so
%pg_extdir/jsonb_plperl*.sql
%pg_extdir/jsonb_plperl*.control
%endif
%pg_libdir/lo.so
%pg_libdir/ltree.so
%pg_libdir/moddatetime.so
%pg_libdir/pageinspect.so
%pg_libdir/passwordcheck.so
%pg_libdir/pgcrypto.so
%pg_libdir/pgrowlocks.so
%pg_libdir/pgstattuple.so
%pg_libdir/pg_buffercache.so
%pg_libdir/pg_freespacemap.so
%pg_libdir/pg_prewarm.so
%pg_libdir/pg_stat_statements.so
%pg_libdir/pg_trgm.so
%pg_libdir/pg_visibility.so
%pg_libdir/postgres_fdw.so
%pg_libdir/refint.so
%pg_libdir/seg.so
%if %enable_ssl
%pg_libdir/sslinfo.so
%endif
%if %enable_selinux
%pg_libdir/sepgsql.so
%pg_datadir/contrib/sepgsql.sql
%endif
%pg_libdir/tablefunc.so
%pg_libdir/tcn.so
%pg_libdir/test_decoding.so
%pg_libdir/tsm_system_rows.so
%pg_libdir/tsm_system_time.so
%pg_libdir/unaccent.so
%if %enable_xml
%pg_libdir/pgxml.so
%pg_extdir/xml2*
%endif
#%if %enable_uuid
%pg_libdir/uuid-ossp.so
%pg_extdir/uuid-ossp*
#%endif
%pg_extdir/adminpack*
%pg_extdir/amcheck*
%pg_extdir/autoinc*
%pg_extdir/bloom*
%pg_extdir/btree_gin*
%pg_extdir/btree_gist*
%pg_extdir/citext*
%pg_extdir/cube*
%pg_extdir/dblink*
%pg_extdir/dict_int*
%pg_extdir/dict_xsyn*
%pg_extdir/earthdistance*
%pg_extdir/file_fdw*
%pg_extdir/fuzzystrmatch*
%pg_extdir/hstore.control
%pg_extdir/hstore--*.sql
%pg_extdir/hstore_plperl*
%pg_extdir/insert_username*
%pg_extdir/intagg*
%pg_extdir/intarray*
%pg_extdir/isn*
%pg_extdir/lo*
%pg_extdir/ltree.control
%pg_extdir/ltree--*.sql
%pg_extdir/moddatetime*
%pg_extdir/pageinspect*
%pg_extdir/pg_buffercache*
%pg_extdir/pg_freespacemap*
%pg_extdir/pg_prewarm*
%pg_extdir/pg_stat_statements*
%pg_extdir/pg_trgm*
%pg_extdir/pg_visibility*
%pg_extdir/pgcrypto*
%pg_extdir/pgrowlocks*
%pg_extdir/pgstattuple*
%pg_extdir/postgres_fdw*
%pg_extdir/refint*
%pg_extdir/seg*
%pg_extdir/hstore_plpython3u--1.0.sql
%pg_extdir/hstore_plpython3u.control
%pg_extdir/jsonb_plpython3u--1.0.sql
%pg_extdir/jsonb_plpython3u.control
%pg_extdir/ltree_plpython3u--1.0.sql
%pg_extdir/ltree_plpython3u.control
%if %enable_ssl
%pg_extdir/sslinfo*
%endif
%pg_extdir/tablefunc*
%pg_extdir/tcn*
%pg_extdir/tsm_system_rows*
%pg_extdir/tsm_system_time*
%pg_extdir/unaccent*
%pg_bindir/oid2name
%pg_bindir/vacuumlo
%pg_bindir/pg_recvlogical
%pg_bindir/pg_standby
%pg_mandir/man1/oid2name.1
%pg_mandir/man1/pg_recvlogical.1
%pg_mandir/man1/pg_standby.1
%pg_mandir/man1/vacuumlo.1

%files libs -f pg_libs.lst
%defattr(-,root,root)
%pg_libdir/libecpg.so*
%pg_libdir/libpgfeutils.a
%pg_libdir/libpgtypes.so.*
%pg_libdir/libecpg_compat.so.*
%pg_libdir/libpqwalreceiver.so
%config(noreplace) %attr (644,root,root) %pg_libs_conf

%files server -f pg_server.lst
%defattr(-,root,root)
%if %enable_systemd
%pg_bindir/postgresql-setup
%pg_bindir/postgresql-check-db-dir
%{_unitdir}/%pg_systemd_service
%else
%config(noreplace) %{_initrddir}/%pg_sysvinit_service
%endif
%if %enable_pam
%config(noreplace) /etc/pam.d/*
%endif
%attr (755,root,root) %dir %pg_etc_sysconfig
%pg_bindir/initdb
%pg_bindir/pg_controldata
%pg_bindir/pg_ctl
%pg_bindir/pg_checksums
%pg_bindir/pg_resetwal
%pg_bindir/postgres
%pg_bindir/postmaster
%pg_mandir/man1/initdb.*
%pg_mandir/man1/pg_controldata.*
%pg_mandir/man1/pg_ctl.*
%pg_mandir/man1/pg_resetwal.*
%pg_mandir/man1/pg_checksums.*
%pg_mandir/man1/postgres.*
%pg_mandir/man1/postmaster.*
%pg_datadir/postgres.bki
%pg_datadir/postgres.description
%pg_datadir/postgres.shdescription
%pg_datadir/system_views.sql
%pg_datadir/*.sample
%pg_datadir/timezonesets/*
%pg_datadir/tsearch_data/*.affix
%pg_datadir/tsearch_data/*.dict
%pg_datadir/tsearch_data/*.ths
%pg_datadir/tsearch_data/*.rules
%pg_datadir/tsearch_data/*.stop
%pg_datadir/tsearch_data/*.syn
%pg_libdir/dict_int.so
%pg_libdir/dict_snowball.so
%pg_libdir/dict_xsyn.so
%pg_libdir/euc2004_sjis2004.so
%pg_libdir/pgoutput.so
%pg_libdir/plpgsql.so
%dir %pg_extdir
%pg_extdir/plpgsql*

%dir %pg_libdir
%dir %pg_datadir
%attr(700,postgres,postgres) %dir %pg_dbroot
%attr(700,postgres,postgres) %dir %pg_dbdir
%attr(700,postgres,postgres) %dir %pg_dbdir/data
%attr(700,postgres,postgres) %dir %pg_dbdir/backups
%attr(755,postgres,postgres) %dir %pg_rundir
%pg_libdir/*_and_*.so
%pg_datadir/information_schema.sql
%pg_datadir/snowball_create.sql
%pg_datadir/sql_features.txt


%if %enable_plperl
%files plperl -f pg_plperl.lst
%defattr(-,root,root)
%pg_libdir/plperl.so
%pg_extdir/plperl*
%endif

%if %enable_pltcl
%files pltcl -f pg_pltcl.lst
%defattr(-,root,root)
%pg_libdir/pltcl.so
%pg_extdir/pltcl*
%endif

%if %enable_plpython2
%files plpython2 -f pg_plpython2.lst
%defattr(-,root,root)
%pg_libdir/plpython2.so
%pg_extdir/plpython2u*
%pg_extdir/plpythonu*
%pg_libdir/hstore_plpython2.so
%pg_libdir/jsonb_plpython2.so
%pg_libdir/ltree_plpython2.so
%pg_extdir/*_plpythonu*
%pg_extdir/*_plpython2u*
%endif

%if %enable_plpython3
%files plpython3 -f pg_plpython3.lst
%pg_extdir/plpython3*
%pg_libdir/plpython3.so
%pg_libdir/hstore_plpython3.so
%pg_libdir/jsonb_plpython3.so
%pg_libdir/ltree_plpython3.so
%pg_extdir/*_plpython3u*
%endif

%changelog
* Tue Feb 11 2020 Enrico Weigelt, metux IT consult <info@metux.net> - 12.2
- Refactored packaging for SLES12
