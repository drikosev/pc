
Sep 30, 2017 


                 FORTRAN PATCHES FOR GCC 4.8.5 in RHEL 7.3
                 -----------------------------------------

This document describes how you can manually extract some GNU Fortran patches from
the zip file "pc-rules-2017-08-19.tar.xz" and apply them to "gcc-4.8.5-16.el7.src.rpm"
in a RHEL 7.3 system. 

In specific, the above mentioned zip file (pc-rules-2017-08-19.tar.xz) contains 34 
unofficial GNU Fortran patches, mainly backports, which have been tested in both 
macOS and Linux. In addition, I've applied them to the source RPM and could build
and test it without any Fortran regressions.  

Please, note that if you rebuild the compiler, it might not be supported by Red Hat.

To run the instructions of this document, you must be familiar with both the RPM 
Building System and Bash scripts. If this isn't the case, contact an experienced
professional.

From time to time, more Fortran related patches are applied to the compiler. See
appendix D (this doesn't mean that I test each new patch in the source RPM).


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

One package required for the tests is "autogen", not mentioned as a prerequisite.
 a) autogen-5.18

Known Issues
------------

Some test failures during the RPM Build are listed in Appendix G. None of 
them is Fortran relevant though.


Instructions (step-by-step)
---------------------------

1) Install any official recommended updates and the Source RPM of gcc-4.8.5

If you don't have subscribed to the sources channel, type first:
sudo  subscription-manager repos --enable=rhel-7-server-source-rpms

Download the Source RPM for gcc, open a terminal in that directory and type:
rpm -i gcc-4.8.5-16.el7.src.rpm

In my system the installed compiler has the same version with the compiler I patch:
$ gcc --version
gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-16)

2) Once the "pc" tarball has been extracted to $HOME/pc, run all the commands of Appendix A
  You should download a tested tarball. Cross check with the date reported in Appendix G.
  curl -o https://github.com/drikosev/pc/blob/master/pc-rules-2017-08-19.tar.xz
  *SHA1 b3e5e4db6230b4b1404c2d52395977059fa59936  

3) Add all Patch Declarations of Appendix B below to the gcc.spec after the line:
Patch1200: cloog-%{cloog_version}-ppc64le-config.patch

4) Add all Patch Commands of Appendix C below to the gcc.spec after the line:
%patch1200 -p0 -b .cloog-ppc64le-config~ 

5) Run the following commands to build the "gcc-4.8.5-16.el7.src.rpm"
    cd ~/rpmbuild
    export RPM_BUILD_NCPUS=4
    export LD_LIBRARY_PATH=""
    export PATH=/usr/bin:/usr/sbin:/bin:/sbin:$PATH
    rpmbuild -ba SPECS/gcc.spec --target x86_64  

The first time I built this package on Aug 15, 2017, I started the building process
at 17:40 and finished at 22:20 (4 hours and 40 minutes).

Below are listed some issues I faced. You might face them also.

-Many dependencies (ie sharutils) are found in the "optionals" channel. If you have not
activated a subscription to it, type: 

 $ sudo subscription-manager repos --enable=rhel-7-server-optional-rpms

-Although my system is x86_64, the failed dependencies like "/lib/libc.so.6" were solved by:
 $ sudo yum install glibc.i686
 $ sudo yum install glibc-devel.i686

(try: sudo yum whatprovides /usr/lib/libc.so)

Also, some tests during the RPM building process require "autogen", which isn't
mentioned in the RPM dependencies.

 $ sudo yum install autogen-5.18

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
cp gcc48-pr56650.relax     ~/rpmbuild/SOURCES

cp gcc48-realloc.patch     ~/rpmbuild/SOURCES
cp gcc48-assumed.istat     ~/rpmbuild/SOURCES


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
Patch9073: gcc48-pr56650.relax

Patch9074: gcc48-realloc.patch   
Patch9075: gcc48-assumed.istat


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
%patch9073 -p0 -b .pr56650_relax~

%patch9074 -p0 -b .realloc.patch~   
%patch9075 -p0 -b .assumed.istat~


Appendix D
----------

  The officially backported patches to 4.8.5, from 2014-12-23 to 2015-04-14, are:
  PR's: 64244, 63733, 57023, 56867, 64528, 63744, 60898, 65024, 61138, 56674,
  58813,59016, 59024.

- Patch: "gcc48-pr56650.relax" (7.1 backport)
  [2017-08-16]      
  This patch restricts the conditions that an error message is issued. If you apply
  the "gcc48-pr56650.patch" but not the "gcc48-pr56650.relax", the RPM Build fails 
  (package "gcc-4.8.5-16.el7.src.rpm" in RHEL 7.3). 

- Patch: "gcc48-realloc.patch" (5.1 backport)
  [2017-08-19] 
  It solves a bug for reallocation of arrays with zero length (that's my diagnosis).
  The bug solved was producing a runtime error only in Linux (see "realloc0last.f90").

- Patch: "gcc48-assume.istat"
  [2017-08-19] 
  It's a hack that mutes some deallocation errors with the option "-std=legacy"
  but without the option "-pedantic". See the program "2slop.f90" below.

  ----------------------------------------------------------------------------------
  The test results in Appendix G validate the above 34 Fortran patches (mentioned in
  Appendixes A, B, and C). Which means that I've tested the 9 patches below only in
  the PC script (on both Linux & Mac).
  ----------------------------------------------------------------------------------

- Patch: "gcc48-pr58586.again" (7.1 backport)
  [2017-08-21]
  Adds the second test case "alloc_comp_class_4.f03" which can be found also here:
  https://gcc.gnu.org/viewcvs/gcc?view=revision&revision=225447
  In macOS 10.12 this test case was crashing (Program received signal SIGABRT) but
  a manual test with "valgrind" proved a memory deallocation error in Linux also.

- Patches: "gcc48-pr63667.patch", "gcc48-tc64230.patch", "gcc48-tc64980.patch" 
  [2017-08-23]
  These test cases confirm that the compiler doesn't have certain bugs described at:
  https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63667 [ 64230 & 4980 ]
  [If the test case in 63667 is reduced to one class (t6) both 4.8 & 7.1 crash.]

-Patch: "gcc48-pr45516.patch", "gcc48-tc45516.patch" (7.1 backport)
  [2017-09-02]
  It solves a bug for recursive allocatable components of derived types as described
  at (a) below, not for classes as described at (b) below:

  (a) https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45516
  (b) https://gcc.gnu.org/bugzilla/show_bug.cgi?id=82036  

- Patch: "gcc48-pr52162.patch" (7.1 backport)
  [2017-09-05] 
  It solves a bug produced when the option " -fcheck=bounds" is passed, see:
  https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52162

- Patch: "gcc48-pr62174.patch"
  [2017-09-25] 
  It's a bug fix for Cray Pointers in Fortran, see:
  https://gcc.gnu.org/bugzilla/show_bug.cgi?id=62174

- Patch: "gcc48-pr64933.patch"
  [2017-09-25] 
  It's a bug fix for substring expressions in Fortran, see:
  https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64933


Appendix E
----------

The following program demonstrates that the patch "gcc48-realloc.patch" avoids the error:
  "Fortran runtime error: Attempt to DEALLOCATE unallocated 'arg'"

$ cat realloc0last.f90
! program  realloc0last.f90
! { dg-do run }
program main
 
  integer, allocatable,  dimension(:) :: arg
  integer :: i, n

  allocate (arg(2), source = [0,0])

  do n = 2, 0, -1
    call bar (arg, n)                 ! Automatic alloc/realloc
  end do

  deallocate(arg)         ! Allocation in main program is not automatically deallocated

contains

  subroutine bar (argarray, j)
    integer, allocatable,  intent(inout), dimension(:) :: argarray 
    integer, allocatable,                 dimension(:) ::  localarray
    integer :: i, j
    localarray = [(i, i = 1, j)]
    argarray = localarray             ! Automatic alloc/realloc
  end subroutine                      ! localarray is deallocated on going out of scope

end program main


The following program demonstrates what does the patch "gcc48-assume.istat".
   

$ gfortran -std=legacy 2slop.f90 -o 2slop; ./2slop
$ gfortran             2slop.f90 -o 2slop; ./2slop
At line 9 of file 2slop.f90
Fortran runtime error: Attempt to DEALLOCATE unallocated 'tmp'
$ cat 2slop.f90
! { dg-do run }
! { dg-options "-std=legacy" }
!
program slop2
 
  integer, allocatable,  dimension(:) :: arg
  integer, allocatable   ::  tmp 
  
  deallocate(tmp)
  deallocate(arg)

end program slop2

Appendix F - Tests Results from the PC Package gcc4
---------------------------------------------------
[2017-09-12]

All Fortran Tests passed successfully in both MacOS (10.12) & RHEL (7.3). Try:
make check-fortran

...
		=== gfortran Summary ===

# of expected passes		44119
# of expected failures		42
# of unsupported tests		70
...

To run only the test case which has the option "-fsanitize=address", type:
make check-fortran RUNTESTFLAGS="dg.exp=elemental_allocate_1.f90"


Appendix G - Test Failures During the RPM Build
-----------------------------------------------
[2017-08-19]

Some test failures (run on Aug 19, 2017) include, but not limited to:

autogen -T ../../fixincludes/check.tpl ../../fixincludes/inclhack.def
make[2]: autogen: Command not found

FAIL: gcc.dg/fstack-protector-strong.c scan-assembler-times stack_chk_fail 10

FAIL: c-c++-common/asan/use-after-free-1.c  -Os  output pattern test, is =================================================================
==9703== ERROR: AddressSanitizer: heap-use-after-free on address 0x60040000dff5 at pc 0x4007ea bp 0x7ffe5e3dbf30 sp 0x7ffe5e3dbf20


FAIL: c-c++-common/asan/heap-overflow-1.c  -O0  output pattern test, is =================================================================
==7924== ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60040000dffa at pc 0x400a95 bp 0x7ffda08a1410 sp 0x7ffda08a1400


FAIL: c-c++-common/asan/null-deref-1.c  -O0  output pattern test, is ASAN:SIGSEGV
=================================================================
==10114== ERROR: AddressSanitizer: SEGV on unknown address 0x000000000028 (pc 0x0000004008d8 sp 0x7ffc9ea17410 bp 0x7ffc9ea17420 T0)

FAIL: c-c++-common/asan/sanity-check-pure-c-1.c  -O0  output pattern test, is =================================================================
==11211== ERROR: AddressSanitizer: heap-use-after-free on address 0x60040000dff5 at pc 0x40097b bp 0x7fffcb1050a0 sp 0x7fffcb105090

FAIL: gcc.dg/stack-usage-1.c scan-file foo\t(256|264)\tstatic
FAIL: gcc.dg/superblock.c scan-rtl-dump-times sched2 "ADVANCING TO" 2

		=== gcc Summary for unix//-fstack-protector ===

# of expected passes		15081
# of unexpected failures	3
# of expected failures		65
# of unsupported tests		105

		=== gcc Summary ===

# of expected passes		42221
# of unexpected failures	3
# of expected failures		130


FAIL: g++.dg/asan/asan_test.C  -O2  AddressSanitizer_SimpleStackTest A[kSize + 31] = 0 execution test
FAIL: g++.dg/asan/asan_test.C  -O2  AddressSanitizer_SimpleStackTest A[kSize + 31] = 0 execution test
FAIL: g++.dg/asan/asan_test.C  -O2  AddressSanitizer_SimpleStackTest A[kSize + 31] = 0 execution test
FAIL: g++.dg/asan/asan_test.C  -O2  AddressSanitizer_SimpleStackTest A[kSize + 31] = 0 execution test
FAIL: g++.dg/fstack-protector-strong.C -std=gnu++11  scan-assembler-times stack_chk_fail 2
FAIL: gcc.dg/guality/pr54200.c  -Os  line 20 z == 3
FAIL: gcc.dg/guality/pr54519-5.c  -O2 -flto -fuse-linker-plugin -fno-fat-lto-objects  line 17 y == 25
FAIL: gcc.dg/guality/pr54693-2.c  -Os  line 21 x == 10 - i
FAIL: gcc.dg/guality/pr36728-3.c  -Os  line 16 arg3 == 3
FAIL: gcc.dg/guality/pr43051-1.c  -O3 -fomit-frame-pointer -funroll-loops  line 39 c == &a[0]

...
Running /home/suser/rpmbuild/BUILD/gcc-4.8.5-20150702/gcc/testsuite/gfortran.dg/dg.exp ...

		=== gfortran Summary for unix/ ===

# of expected passes		6116
# of expected failures		6
Running target unix//-fstack-protector
...
		=== gfortran Summary for unix//-fstack-protector ===

# of expected passes		6338
# of expected failures		2

		=== gfortran Summary ===

# of expected passes		12676
# of expected failures		4
...
Running /home/suser/rpmbuild/BUILD/gcc-4.8.5-20150702/libffi/testsuite/libffi.call/call.exp ...
--- FAIL: TestParseInSydney (0.32 seconds)
	time_test.go:553: ParseInLocation(Feb 01 2013 EST, Sydney) = 2013-02-01 00:00:00 +0000 EST, want 2013-02-01 00:00:00 +1100 AEDT
--- FAIL: TestLoadFixed (0.23 seconds)
	time_test.go:1326: Now().In(loc).Zone() = "-01", -3600, want "GMT+1", -3600
FAIL
FAIL: time
make[5]: *** [time/check] Error 1

...

PASS: text/template
make[4]: Leaving directory `/home/suser/rpmbuild/BUILD/gcc-4.8.5-20150702/obj-x86_64-redhat-linux/x86_64-redhat-linux/libgo'
make[3]: [check-am] Error 2 (ignored)
make[3]: Leaving directory `/home/suser/rpmbuild/BUILD/gcc-4.8.5-20150702/obj-x86_64-redhat-linux/x86_64-redhat-linux/libgo'
make[2]: *** [check-tail] Error 1
make[2]: Target `check' not remade because of errors.
make[2]: Leaving directory `/home/suser/rpmbuild/BUILD/gcc-4.8.5-20150702/obj-x86_64-redhat-linux/x86_64-redhat-linux/libgo'
make[1]: *** [check-target-libgo] Error 2

...

