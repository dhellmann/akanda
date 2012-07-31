#!/bin/sh
#  ___                   ____ ____  ____
# / _ \ _ __   ___ _ __ | __ ) ___||  _ \
#| | | | '_ \ / _ \ '_ \|  _ \___ \| | | |
#| |_| | |_) |  __/ | | | |_) |__) | |_| |
# \___/| .__/ \___|_| |_|____/____/|____/
#      | |
#      |_| ----------------Akanda Live CD-
#
# This script creates an Akanda Live CD - powered by OpenBSD and Twisted - and
# lets you customize it
#
#
# Copyright (c) 2009 Reiner Rottmann. Released under the BSD license.
# Copyright (c) 2012 New Dream Network, LLC (DreamHost).
#
# First release 2009-06-20
# Akanda release 2012-07-29
#
# Notes:
#
# * Modified for use with Akanda by Murali Raju - murali.raju@dreamhost.com -
#   2012

###############################################################################
# Defaults
###############################################################################
MAJ=5                    # Version major number
MIN=1                    # Version minor number
ARCH=i386                # Architecture
TZ=US/Eastern            # Time zones are in /usr/share/zoneinfo
# The base sets that should be installed on the akanda live cd
SETS="base etc man"
# Additional packages that should be installed on the akanda live cd
PACKAGES="python-2.7.1p12 rsync-3.0.9 git py-pip gmake curl wget"


WDIR=/tmp/akanda-livecdx            # Working directory
CDBOOTDIR=$WDIR/$MAJ.$MIN/$ARCH        # CD Boot directory

# Mirror to use to download the OpenBSD files
#BASEURL=http://ftp-stud.fht-esslingen.de/pub/OpenBSD
BASEURL=http://openbsd.mirrors.pair.com
MIRROR=$BASEURL/$MAJ.$MIN/$ARCH
PKG_PATH=$BASEURL/$MAJ.$MIN/packages/$ARCH
DNS=8.8.8.8            # Google DNS Server to use in live cd (change accordingly)


CLEANUP=no                    # Clean up downloaded files and workdir (disabled by default)

# End of user configuration
###############################################################################

# global variables

SCRIPTNAME=$(basename $0 .sh)

EXIT_SUCCESS=0
EXIT_FAILED=1
EXIT_ERROR=2
EXIT_BUG=10

VERSION="1.0.0"

# base functions

# In case of an error it is wise to show the correct usage of the script.
function usage {
    echo >&2
    echo -e "Usage: $SCRIPTNAME \t[-A <arch>] [-h] [-M <major>] [-m <minor>] [-P <packages>]" >&2
    echo -e "                   \t\t[-S <sets>] [-T <timezone>] [-V] [-W <workdir>] [-U <url>]" >&2
    echo >&2
    echo "This program creates an OpenBSD live cd and lets you customize it." >&2
    echo "The software is released under BSD license. Use it at your own risk!" >&2
    echo "Copyright (c) 2009 Reiner Rottmann. Email: reiner[AT]rottmann.it" >&2
    echo "Modified for Akanda by Murali Raju. Email: murali.raju[AT]dreamhost.com" >&2
    echo >&2
    echo -e "  -A :\tselect architecture (default: $ARCH)" >&2
    echo -e "  -h :\tgive this help list" >&2
    echo -e "  -M :\tselect OpenBSD major version (default: $MAJ)" >&2
    echo -e "  -m :\tselect OpenBSD minor version (default: $MIN)" >&2
    echo -e "  -P :\tselect additional packages to install" >&2
    echo -e "      \t(default: $PACKAGES)" >&2
    echo -e "  -S :\tselect base sets (default: $SETS)" >&2
    echo -e "  -T :\tselect timezone (default: $TZ)" >&2
    echo -e "  -U :\tselect url of nearest OpenBSD mirror (default: $MIRROR)" >&2
    echo -e "  -u :\tselect url of nearest OpenBSD from mirror list (requires wget)" >&2
    echo -e "  -V :\tprint version" >&2
    echo -e "  -W :\tselect working directory (default: $WDIR)" >&2
    echo >&2
    echo -e "Example:" >&2
    echo -e "# $SCRIPTNAME -A i386 -M 4 -m 5 -W /tmp/livecd" >&2
    echo >&2
    [[ $# -eq 1 ]] && exit $1 || exit $EXIT_FAILED
}

# own functions
# This function lets the user choose an OpenBSD mirror
function choosemirror {
    req="wget"
    for i in $req
    do
        if ! which $i >/dev/null; then
            echo "Missing $i. Exiting."
            exit $EXIT_ERROR
        fi
    done

    mirrorlist=$(wget -q -O - http://www.openbsd.org/ftp.html#ftp | sed -n 's#<a href=\"\(ftp://.*\)/">#\1#p'|sort)

    echo "Please select mirror from the list below:"

    mirr=""
    while [ -z "$mirr" ] ; do
            m=1
            for i in $mirrorlist
            do
                    echo $m. "$i"
                    m=$(($m+1))
            done
            echo -n "Your choice? : "
            read choice
            mirr=$(echo "$mirrorlist" | sed -n $choice,${choice}p| sed s#^\ *##g)
    done
    BASEURL=$mirr
    MIRROR=$BASEURL/$MAJ.$MIN/$ARCH
    PKG_PATH=$BASEURL/$MAJ.$MIN/packages/$ARCH
    CDBOOTDIR=$WDIR/$MAJ.$MIN/$ARCH
}

# This function may be used for cleanup before ending the program
function cleanup {
    echo
}


# This is the main function that creates the OpenBSD livecd
function livecd {
    echo "[*] Akanda (powered by OpenBSD) LiveCD script"
    echo "[*] The software is released under BSD license. Use it at your own risk!" >&2
    echo "[*] Copyright (c) 2009 Reiner Rottmann." >&2
    echo "[*] Modified for Akanda by Murali Raju. Email: murali.raju[AT]dreamhost.com" >&2
    echo "[*] This script is released under the BSD License."
    uname -a | grep OpenBSD || echo "[*] WARNING: This software should run on an OpenBSD System!"
    date
    echo "[*] Setting up the build environment..."
    mkdir -p $WDIR

     if [[ $CHMIRROR = y ]] ; then
        echo "[*] Selecting OpenBSD mirror..."
        choosemirror
        echo $MIRROR
    fi

    # Create CD Boot directory
    mkdir -p $CDBOOTDIR && cd $CDBOOTDIR

    echo "[*] Downloading files needed for CD Boot..."
    CDBOOTFILES="cdbr cdboot bsd"
    cd $CDBOOTDIR && for i in $CDBOOTFILES; do test -f $CDBOOTDIR/$i || ftp -o $CDBOOTDIR/$i -m $MIRROR/$i; done


    echo "[*] Downloading file sets ($SETS)..."
    cd $WDIR && for i in $SETS; do test -f $WDIR/$i$MAJ$MIN.tgz || ftp -o $WDIR/$i$MAJ$MIN.tgz -m $MIRROR/$i$MAJ$MIN.tgz; done

    echo "[*] Extracting file sets ($SETS)..."
    cd $WDIR && for i in $SETS; do tar xzpf $WDIR/$i$MAJ$MIN.tgz; done

    if [ $CLEANUP="yes" ];then
        echo "[*] Deleting file set tarballs ($SETS)..."
        cd $WDIR && for i in $SETS; do rm -f $WDIR/$i$MAJ$MIN.tgz; done
    fi

    echo "[*] Populating dynamic device directory..."
    cd $WDIR/dev && $WDIR/dev/MAKEDEV all

    echo "[*] Creating boot configuration..."
    echo "set image $MAJ.$MIN/$ARCH/bsd" > $WDIR/etc/boot.conf

    echo "[*] Creating fstab entries..."
    cat >/$WDIR/etc/fstab <<EOF
    swap /tmp mfs rw,auto,-s=120000 0 0
    swap /var mfs rw,auto,-P/mfsvar 0 0
    swap /etc mfs rw,auto,-P/mfsetc 0 0
    swap /root mfs rw,auto,-P/mfsroot 0 0
    swap /dev mfs rw,auto,-P/mfsdev 0 0
EOF

    echo "[*] Creating motd file..."
    cat >$WDIR/etc/motd <<EOF

  ___                   ____ ____  ____
 / _ \\ _ __   ___ _ __ | __ ) ___||  _ \\
| | | | '_ \\ / _ \\ '_ \\|  _ \\___ \\| | | |
| |_| | |_) |  __/ | | | |_) |__) | |_| |
 \\___/| .__/ \\___|_| |_|____/____/|____/
      | |
      |_| -----------------Akanda Live CD-

Welcome to Akanda: Powered by OpenBSD - the proactively secure Unix-like operating system.


EOF

    echo "[*] Creating dhcp client configuration..."
    cat >$WDIR/etc/dhclient.conf <<EOF
    initial-interval 1;
    request subnet-mask,
    broadcast-address,
    routers, domain-name,
    domain-name-servers,
    host-name;
EOF

    echo "[*] Setting name..."
    cat > $WDIR/etc/myname <<EOF
    akanda
EOF

    echo "[*] Setting hostname.em0 to dhcp..."
    cat > $WDIR/etc/hostname <<EOF
    dhcp
EOF

    echo "[*] Modifying rc.local..."
    cat >>$WDIR/etc/rc.local <<EOF
# If you have enough memory, this speeds up some bins, but you must
# add /binmfs/bin and /binmfs/sbin to your path, before /bin and /sbin
# mymem=`sysctl hw.physmem | cut -f 2 -d =`
# if [ \$mymem -gt 268000000 ]
# then
#         mount_mfs -s 48000 swap /binmfs >/dev/null 2>&1
#         mkdir /binmfs/bin
#         mkdir /binmfs/sbin
#         /bin/cp -rp /bin /binmfs
#         /bin/cp -rp /sbin /binmfs
# fi

# Select keyboard language
echo "Select keyboard language (by number):"
select klang in us de es it fr be jp nl ru uk sv no pt br hu tr dk sg pl sf lt la lv
do
        /sbin/kbd \$klang
        break
done

# function for setting the timezone
sub_timezone() {

   while :
   do
      echo -n "What timezone are you in? ('?' for list) "
      read zone

      if [ \${zone} = "?" ]
      then
         ls -F /usr/share/zoneinfo
      fi

      if [ -d /usr/share/zoneinfo/\${zone} ]
      then
         ls -F /usr/share/zoneinfo/\${zone}
         echo -n "What sub-timezone of \${zone} are you in? "
         read subzone
         zone="\${zone}/\${subzone}"
      fi

      if [ -f /usr/share/zoneinfo/\${zone} ]
      then
         echo "Setting local timezone to \${zone} ..."
         rm /etc/localtime
         ln -sf /usr/share/zoneinfo/\${zone} /etc/localtime
         echo "done"
         return
      fi
   done
}

# Select timezone
echo -n "Do you want to configure the timezone? (y/N): "
read timeconf
if [ ! -z \$timeconf ]
then
   if [ \$timeconf = "y" ] || [ \$timeconf = "Y" ] || [ \$timeconf = "yes"] || [ \$timeconf = "Yes" ]
   then
      sub_timezone
   fi
fi

# Configure network interface
myif=\$(ifconfig | awk -F: '/^[a-z][a-z]+[0-3]: flags=/ { print \$1 }' | grep -v lo | grep -v enc | grep -v pflog)
for thisif in \$myif
do
   ifconfig \$thisif up
   echo "starting dhclient \$thisif in background"
   dhclient -q \$thisif 2>/dev/null &
done

# If you have enough memory, you can populate /usr/local to RAM
if [ \$mymem -gt 500000000 ]
then
        echo -n "Do you want /usr/local loading to RAM (y/N)? "
        read ownpack
        if [ ! -z \$ownpack ]
        then
           if [ \$ownpack = "y" ] || [ \$ownpack = "Y" ] || [ \$ownpack = "yes" ] || [ \$ownpack = "Yes" ]
           then
              echo "Loading ... please wait ..."
              if [ \$mymem -gt 800000000 ]
              then
                 mount_mfs -s 691200 -P /usr/local-cd swap /usr/local
              else
                 mount_mfs -s 473088 -P /usr/local-cd swap /usr/local
              fi
           fi
         fi
fi

# Password for root
echo -n "Do you want to set a password for root(y/N)?"
read rootpass
if [ ! -z \$rootpass ]
then
   if [ \$rootpass = "y" ] || [ \$rootpass = "Y" ] || [ \$rootpass = "Yes" ] || [ \$rootpass = "yes" ] || [ \$rootpass = "YES" ]
   then
      passwd root
   fi
else
   echo "password for root not set (password empty)"
fi

EOF
    echo "[*] Modifying the library path..."
    echo >> $WDIR/root/.cshrc << EOF
    # Workaround for missing libraries:
    export LD_LIBRARY_PATH=/usr/local/lib
    EOF
        echo >> $WDIR/root/.profile << EOF
    # Workaround for missing libraries:
    export LD_LIBRARY_PATH=/usr/local/lib
    EOF
        echo >> $WDIR/etc/profile/.cshrc << EOF
    # Workaround for missing libraries:
    export LD_LIBRARY_PATH=/usr/local/lib
    EOF
        echo >> $WDIR/etc/profile/.profile << EOF
    # Workaround for missing libraries:
    export LD_LIBRARY_PATH=/usr/local/lib
    EOF

    echo "[*] Using DNS ($DNS) in livecd environment..."
    echo "nameserver $DNS" > $WDIR/etc/resolv.conf

    echo "[*] Installing additional packages..."
    cat > $WDIR/tmp/packages.sh <<EOF
    #!/bin/sh
    export PKG_PATH=$(echo $PKG_PATH | sed 's#\ ##g')
    for i in $PACKAGES
    do
        pkg_add -i \$i
    done
EOF

    echo "[*] Copying akanda to /var/..."
    cp -r /root/repos/akanda $WDIR/var


    chmod +x $WDIR/tmp/packages.sh
    chroot $WDIR /tmp/packages.sh
    rm $WDIR/tmp/packages.sh

    echo "[*] Entering Akanda livecd builder (chroot environment)."
    echo "[*] Once you have finished your modifications, type \"exit\""
cat <<EOF


**These steps will eventually be automated as part of the build process in further revisions**

Setup environment:

export PKG_PATH=$(echo $PKG_PATH | sed 's#\ ##g')

To get rid load libraries erros, run:

export LD_LIBRARY_PATH=/usr/local/lib

ln -sf /usr/local/bin/python2.7 /usr/local/bin/python
ln -sf /usr/local/bin/python2.7-2to3 /usr/local/bin/2to3
ln -sf /usr/local/bin/python2.7-config /usr/local/bin/python-config
ln -sf /usr/local/bin/pydoc2.7  /usr/local/bin/pydoc
ln -sf /usr/local/bin/pip-2.7 /usr/local/bin/pip

Install deps:

pip install netaddr repoze.lru txroutes

Install Akanda:

**You may have to generate a new ssh key and add it to github for the akanda install to continue**

cd /var
git clone git@github.com:dreamhost/akanda.git
cd akanda
gmake install-dev


EOF
    chroot $WDIR

    echo "[*] Deleting sensitive information..."
    cd $WDIR && rm -i root/{.history,.viminfo}
    cd $WDIR && rm -i home/*/{.history,.viminfo}

    echo "[*] Empty log files..."
    for log_file in $(find $WDIR/var/log -type f)
    do
        echo "" > $log_file
    done

    echo "[*] Remove ports and src (only on live cd)..."
    rm -rf $WDIR/usr/{src,ports,xenocara}/*

    echo "[*] Removing ssh host keys..."
    rm $WDIR/etc/ssh/*key*

    echo "[*] Saving creation timestamp..."
    date > $WDIR/etc/livecd-release

    echo "[*] Saving default timezone..."
    ln -s /usr/share/zoneinfo/$TZ $WDIR/etc/localtime


    echo "[*] Creating mfs-mount directories..."
    cp -rp $WDIR/var $WDIR/mfsvar
    rm -r $WDIR/var/*
    cp -rp $WDIR/root $WDIR/mfsroot
    cp -rp $WDIR/etc $WDIR/mfsetc
    mkdir $WDIR/mfsdev
    cp -p $WDIR/dev/MAKEDEV $WDIR/mfsdev/
    cd $WDIR/mfsdev && $WDIR/mfsdev/MAKEDEV all

    echo "[*] Creating Akanda live-cd iso..."
    cd /
    mkhybrid -l -R -o $WDIR/livecd$MAJ$MIN-$ARCH.iso -b $MAJ.$MIN/$ARCH/cdbr -c $MAJ.$MIN/$ARCH/boot.catalog $WDIR

    echo "[*] Your modified Akanda iso is in $WDIR/livecd$MAJ$MIN-$ARCH.iso"
    ls -lh $WDIR/livecd$MAJ$MIN-$ARCH.iso

    if [ $CLEANUP="yes" ];then
        echo "[*] Cleanup"
        echo -n "Do you want to delete the working directory $WDIR? (y/N): "
        read deletewdir
        if [ ! -z $deletewdir ]
        then
            if [ $deletewdir = "y" ] || [ $deletewdir = "Y" ] || [ $deletewdir = "yes"] || [ $deletewdir = "Yes" ]
            then
                rm -rf $WDIR
               fi
        fi
    fi

    echo "[*] Please support the OpenBSD project by buying official cd sets or donating some money!"
    echo "[*] Enjoy Akanda!"
    date
    echo "[*] Done."
}

# Evaluate the command line options
while getopts 'A:hM:m:P:S:T:U:uvVW:' OPTION ; do
        case $OPTION in
        A)      ARCH=${OPTARG}
                ;;
    h)      usage $EXIT_ERFOLG
                ;;
    M)      MAJ=${OPTARG}
                ;;
    m)      MIN=${OPTARG}
                ;;
    P)      PACKAGES=${OPTARG}
                ;;
    S)      SETS=${OPTARG}
                ;;
    T)      TZ=${OPTARG}
                ;;
    U)      BASEURL=${OPTARG}
                ;;
    u)      CHMIRROR=y
                ;;
        v)      VERBOSE=y
                ;;
        V)      echo $VERSION
                exit $EXIT_ERROR
                ;;
    W)      WDIR=${OPTARG}
                ;;

        \?)     echo "Unknown option \"-$OPTARG\"." >&2
                usage $EXIT_ERROR
                ;;
        :)      echo "Option \"-$OPTARG\" needs an argument." >&2
                usage $EXIT_ERROR
                ;;
        *)      echo "" >&2
                usage $EXIT_ERROR
                ;;
        esac
done

# Skip already used arguments
shift $(( OPTIND - 1 ))

# Loop over all arguments
for ARG ; do
        if [[ $VERBOSE = y ]] ; then
                echo -n "Argument: "
        fi
        #echo $ARG
done

# Call (main-)function
livecd

#
cleanup
exit $EXIT_SUCCESS

