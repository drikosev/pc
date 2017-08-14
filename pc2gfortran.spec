
Aug 14, 2017 


                 FORTRAN PATCHES FOR GCC 4.8.5 in RHEL 7.3
                 -----------------------------------------

This document describes how to manually extract some GNU Fortran patches from the
file "pc-rules-2017-05-24.tar.xz" and transfer them to "gcc-4.8.5-16.el7.src.rpm"
in a RHEL 7.3 system. 

In specific, the above mentioned script (pc-rules-2017-05-24.tar.xz) contains 31 
unofficial GNU Fortran patches, mainly backports, which have been tested in macOS. 
That is, the pc (port center) script cannot install the *gcc48* package in Linux.

Please, note that if you rebuild the compiler, it won't be supported by Red Hat.

To run the instructions of this document, you must be experienced in both the RPM 
Building System and Bash scripts. If this isn't the case, contact an experienced
professional.

Many bugs are solved but there are case where a bug solved by a patch (ie 52832)
reappears after some other patches have been applied. In most cases this doesn't
happen however.

The program "slop.f90" below (in Appendix D) exhibits a bug in gfortran-4.8.5 on
RHEL 7.3, which doesn't appear in gfortran-4.8.5 built by the "pc" in a mac. This
was the reason I started this document but unfortunately the problem isn't solved
in Linux.


Environment
-----------

      Computer : Mac-Mini quad core i7 (late 2011)
           RAM : 4-GB
        Distro : RHEL 7.3 (Last Update on Aug 13, 2017)
       Machine : x86_64-redhat-linux
Kernel Version : 3.10.0-514.el7.x86_64
System Compiler: gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-16)


Prerequisites & Dependencies
----------------------------

When you start the building process, you will be informed of any missing
dependencies but some packages aren't downloaded from the default repository.

In addition to the default repo channel, I needed another two: 
 a) rhel-7-server-source-rpms
 b) rhel-7-server-optional-rpms

Although my system is x86_64, I had also to install the 686 version of glibc:
 a) glibc.i686
 b) glibc-devel.i686
 c) glibc.x86_64
 d) glibc-devel.x86_64


Known Issues
------------

The building process fails due to patch "gcc48-libgomp-20160715.patch", which
means that the default compiler gcc-4.8.5-16 cannot build itself.

Since the default compiler is the only one in my system, I've commented the
offensive patch:

#%patch35 -p0 -b .libgomp-20160715~ 

At the end of this document there is also an appendix with some test failures.




Instructions (step-by-step)
---------------------------

1) Install any official recommended updates and the Source RPM of gcc-4.8.5

If you don't have subscribed to the sources chanel, type first:
sudo  subscription-manager repos --enable=rhel-7-server-source-rpms

Download the Source RPM for gcc, open a terminal in that directory and type:
rpm -i gcc-4.8.5-16.el7.src.rpm

In my system the installed compiler has the same version with the compiler I'll patch:
$ gcc --version
gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-16)

2) Once the "pc" tarball has been extracted to $HOME/pc, run all the commands of Appendix A

3) Add all Patch Declarations of Appendix B below to the gcc.spec after the line:
Patch1200: cloog-%{cloog_version}-ppc64le-config.patch

4) Add all Patch Commands of Appendix C below to the gcc.spec after the line:
%patch1200 -p0 -b .cloog-ppc64le-config~ 

5) Run the following commands to build the "gcc-4.8.5-16.el7.src.rpm"
  $ cd ~/rpmbuild
  $ export RPM_BUILD_NCPUS=4
  $ rpmbuild -ba SPECS/gcc.spec --target x86_64  

I started the building process on Aug 14, 2017 at 13:30 pm and it took more than 4 hours.

Let's see in some detail some issues.

-Many dependencies (ie sharutils) are found in the "optionals" chanel. If you have not
activated a subscription to it, type: 

 $ sudo subscription-manager repos --enable=rhel-7-server-optional-rpms

-Although my system is x86_64, the failed dependencies like "/lib/libc.so.6" were solved by:
 $ sudo yum install glibc.i686
 $ sudo yum install glibc-devel.i686

(try: sudo yum whatprovides /usr/lib/libc.so)


6) Install the new Compiler
 
cd ~/rpmbuild/RPMS/x86_64

sudo rpm --force -i libasan-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libasan-static-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libatomic-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libatomic-static-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libgcc-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libgfortran-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libgfortran-static-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libgnat-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libgnat-devel-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libgnat-static-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libgo-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libgo-devel-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libgomp-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libgo-static-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libitm-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libitm-devel-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libitm-static-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libmudflap-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libmudflap-devel-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libmudflap-static-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libobjc-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libquadmath-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libquadmath-devel-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libquadmath-static-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libstdc++-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libstdc++-devel-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libstdc++-docs-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libstdc++-static-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libtsan-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i libtsan-static-4.8.5-16.el7.x86_64.rpm

sudo rpm --force -i gcc-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i gcc-base-debuginfo-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i gcc-c++-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i gcc-debuginfo-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i gcc-gfortran-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i gcc-gnat-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i gcc-go-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i gcc-objc-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i gcc-objc++-4.8.5-16.el7.x86_64.rpm
sudo rpm --force -i gcc-plugin-devel-4.8.5-16.el7.x86_64.rpm


Appendix A
-------
cd ~/pc/rules/patches/gcc48


cp gcc48-pr57549.patch     ~/rpmbuild/SOURCES
cp gcc48-tc57549.patch     ~/rpmbuild/SOURCES
cp gcc48-pr56650.patch     ~/rpmbuild/SOURCES
cp gcc48-tc56650.patch     ~/rpmbuild/SOURCES
cp gcc48-pr65429.patch     ~/rpmbuild/SOURCES
cp gcc48-pr52153.patch     ~/rpmbuild/SOURCES
cp gcc48-pr59746.patch     ~/rpmbuild/SOURCES
cp gcc48-pr44265.patch     ~/rpmbuild/SOURCES
cp gcc48-pr59997.patch     ~/rpmbuild/SOURCES
cp gcc48-pr61960.patch     ~/rpmbuild/SOURCES
cp gcc48-pr64925.patch     ~/rpmbuild/SOURCES
cp gcc48-pr52832.patch     ~/rpmbuild/SOURCES
cp gcc48-pr58991.patch     ~/rpmbuild/SOURCES
cp gcc48-pr58618.patch     ~/rpmbuild/SOURCES
cp gcc48-pr57530.patch     ~/rpmbuild/SOURCES
cp gcc48-pr58586.patch     ~/rpmbuild/SOURCES
cp gcc48-pr60357.patch     ~/rpmbuild/SOURCES
cp gcc48-pr65792.patch     ~/rpmbuild/SOURCES
cp gcc48-pr66052.patch     ~/rpmbuild/SOURCES
cp gcc48-pr66044.patch     ~/rpmbuild/SOURCES
cp gcc48-pr66040.patch     ~/rpmbuild/SOURCES
cp gcc48-pr66043.patch     ~/rpmbuild/SOURCES
cp gcc48-pr58749.patch     ~/rpmbuild/SOURCES
cp gcc48-pr66245.patch     ~/rpmbuild/SOURCES
cp gcc48-pr66377.patch     ~/rpmbuild/SOURCES
cp gcc48-pr66113.patch     ~/rpmbuild/SOURCES
cp gcc48-pr51976.patch     ~/rpmbuild/SOURCES
cp gcc48-tc51976.patch     ~/rpmbuild/SOURCES
cp gcc48-pr60593.patch     ~/rpmbuild/SOURCES
cp gcc48-pr45689.patch     ~/rpmbuild/SOURCES
cp gcc48-tc45689.patch     ~/rpmbuild/SOURCES


Appendix B
-------

   
Patch9042: gcc48-pr57549.patch   
Patch9043: gcc48-tc57549.patch  
Patch9044: gcc48-pr56650.patch  
Patch9045: gcc48-tc56650.patch   
Patch9046: gcc48-pr65429.patch   
Patch9047: gcc48-pr52153.patch   
Patch9048: gcc48-pr59746.patch   
Patch9049: gcc48-pr44265.patch  
Patch9050: gcc48-pr59997.patch   
Patch9051: gcc48-pr61960.patch   
Patch9052: gcc48-pr64925.patch  
Patch9053: gcc48-pr52832.patch   
Patch9054: gcc48-pr58991.patch  
Patch9055: gcc48-pr58618.patch   
Patch9056: gcc48-pr57530.patch   
Patch9057: gcc48-pr58586.patch   
Patch9058: gcc48-pr60357.patch   
Patch9059: gcc48-pr65792.patch   
Patch9060: gcc48-pr66052.patch   
Patch9061: gcc48-pr66044.patch   
Patch9062: gcc48-pr66040.patch   
Patch9063: gcc48-pr66043.patch   
Patch9064: gcc48-pr58749.patch   
Patch9065: gcc48-pr66245.patch   
Patch9066: gcc48-pr66377.patch   
Patch9067: gcc48-pr66113.patch   
Patch9068: gcc48-pr51976.patch   
Patch9069: gcc48-tc51976.patch  
Patch9070: gcc48-pr60593.patch   
Patch9071: gcc48-pr45689.patch   
Patch9072: gcc48-tc45689.patch   



Appendix C
-------
 
%patch9042 -p0 -b .pr57549~   
%patch9043 -p0 -b .tc57549~  
%patch9044 -p0 -b .pr56650~  
%patch9045 -p0 -b .tc56650~   
%patch9046 -p0 -b .pr65429~   
%patch9047 -p0 -b .pr52153~   
%patch9048 -p0 -b .pr59746~   
%patch9049 -p0 -b .pr44265~  
%patch9050 -p0 -b .pr59997~   
%patch9051 -p0 -b .pr61960~   
%patch9052 -p0 -b .pr64925~  
%patch9053 -p0 -b .pr52832~   
%patch9054 -p0 -b .pr58991~  
%patch9055 -p0 -b .pr58618~   
%patch9056 -p0 -b .pr57530~   
%patch9057 -p0 -b .pr58586~   
%patch9058 -p0 -b .pr60357~   
%patch9059 -p0 -b .pr65792~   
%patch9060 -p0 -b .pr66052~   
%patch9061 -p0 -b .pr66044~   
%patch9062 -p0 -b .pr66040~   
%patch9063 -p0 -b .pr66043~   
%patch9064 -p0 -b .pr58749~   
%patch9065 -p0 -b .pr66245~   
%patch9066 -p0 -b .pr66377~   
%patch9067 -p0 -b .pr66113~   
%patch9068 -p0 -b .pr51976~   
%patch9069 -p0 -b .tc51976~  
%patch9070 -p0 -b .pr60593~   
%patch9071 -p0 -b .pr45689~   
%patch9072 -p0 -b .tc45689~   


Appendix D
----------

! program  slop.f90
! submited as a response to c.l.f to exhibit a bug
! which appears in gfortran-4.8.5 on RHEL 7.3:
! Fortran runtime error: Attempt to DEALLOCATE unallocated 'arg' 

      program main
 
  integer, allocatable,  dimension(:) :: arg
  integer :: i, n
  integer :: ierr

  allocate (arg(2), source = [0,0])

  do n = 2, 0, -1
    call foo (arg, n)                  ! Explicit array bounds in assignment
    print *, arg, ' size ', size(arg)
    arg = 0
  end do

  print *, ''

  do n = 2, 0, -1
    call bar (arg, n)                 ! Automatic alloc/realloc
    print *, arg, ' size ', size(arg)
  end do
  
  deallocate(arg)         ! Allocation in main program is not automatically deallocated

contains

  subroutine foo (argarray, j)
    integer, allocatable,  dimension(:) :: argarray, localarray
    integer :: i, j
    localarray = [(i, i = 1, j)]
    argarray(1:j) = localarray(1:j)   ! As in the report
  end subroutine                      ! localarray is deallocated on going out of scope

  subroutine bar (argarray, j)
    integer, allocatable,  dimension(:) :: argarray, localarray
    integer :: i, j
    localarray = [(i, i = 1, j)]
    argarray = localarray             ! Automatic alloc/realloc
  end subroutine                      ! localarray is deallocated on going out of scope

end program main
   
Appendix E - Test Failures
----------------------

Some test failures include, but not limited to:

FAIL: gcc.c-torture/execute/pr51581-1.c compilation,  -O0 
FAIL: tmpdir-g++.dg-struct-layout-1/t024 cp_compat_y_tst.o compile
FAIL: 22_locale/time_get/get_monthname/wchar_t/3.cc (test for excess errors)
FAIL: 23_containers/multimap/23781_neg.cc  (test for errors, line 27)
FAIL: 23_containers/multimap/23781_neg.cc  (test for errors, line 28)
FAIL: 23_containers/multimap/23781_neg.cc (test for excess errors)
FAIL: gcc.dg/fstack-protector-strong.c scan-assembler-times stack_chk_fail 10
FAIL: gcc.dg/stack-usage-1.c scan-file foo\t(256|264)\tstatic
FAIL: gcc.dg/superblock.c scan-rtl-dump-times sched2 "ADVANCING TO" 2
FAIL: g++.dg/template/ref7.C -std=c++98 (test for excess errors)
FAIL: g++.dg/template/ref7.C -std=c++11 (test for excess errors)
FAIL: g++.dg/fstack-protector-strong.C -std=gnu++98  scan-assembler-times stack_chk_fail 2
FAIL: g++.dg/fstack-protector-strong.C -std=gnu++11  scan-assembler-times stack_chk_fail 2
FAIL: gfortran.dg/elemental_allocate_1.f90  -O0  (test for excess errors)
FAIL: gfortran.dg/elemental_allocate_1.f90  -O1  (test for excess errors)
FAIL: gfortran.dg/elemental_allocate_1.f90  -O2  (test for excess errors)
FAIL: gfortran.dg/elemental_allocate_1.f90  -O3 -fomit-frame-pointer  (test for excess errors)
FAIL: gfortran.dg/elemental_allocate_1.f90  -O3 -fomit-frame-pointer -funroll-loops  (test for excess errors)
FAIL: gfortran.dg/elemental_allocate_1.f90  -O3 -fomit-frame-pointer -funroll-all-loops -finline-functions  (test for excess errors)
FAIL: gfortran.dg/elemental_allocate_1.f90  -O3 -g  (test for excess errors)
FAIL: gfortran.dg/elemental_allocate_1.f90  -Os  (test for excess errors)
FAIL: gcc.dg/guality/pr36728-1.c  -O2 -flto -fuse-linker-plugin -fno-fat-lto-objects  line 18 arg3 == 3
FAIL: gcc.dg/guality/pr36728-3.c  -O1  line 14 arg3 == 3
--- FAIL: TestParseInSydney (0.00 seconds)
	time_test.go:553: ParseInLocation(Feb 01 2013 EST, Sydney) = 2013-02-01 00:00:00 +0000 EST, want 2013-02-01 00:00:00 +1100 AEDT
--- FAIL: TestLoadFixed (0.00 seconds)
	time_test.go:1326: Now().In(loc).Zone() = "-01", -3600, want "GMT+1", -3600
FAIL
FAIL: time
make[4]: *** [time/check] Error 1



		=== libstdc++ Summary ===

# of expected passes		1277
# of unexpected failures	3
# of expected failures		24
# of unsupported tests		154



		=== gcc Summary ===

# of expected passes		42219
# of unexpected failures	4
# of expected failures		130
# of unresolved testcases	1
# of unsupported tests		210







