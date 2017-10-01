
Sep 30, 2017 


                 FORTRAN PATCHES FOR GCC 4.8.5 in RHEL 7.3
                 -----------------------------------------

   1) Introduction
      1.1) Environment
      1.2) Prerequisites & Dependencies
      1.3) Known Issues
   
   2) Step by Step Instructions to Apply the Fortran Patches  
      2.1) Download & Setup the PC Script
      2.2) Copy the Fortran Patches to the ~/rpmbuild/SOURCES Directory
      2.3) Install the Source RPM
      2.4) Update the gcc.spec File
      2.5) Install any missing Prerequisites
      2.6) Build the RPM
      2.7) Install the new Compiler

   3) Appendices
             A-D: text to copy/paste.
      Appendix F: sample code
      Appendix E: a short list with the most recent added patches
      Appendix G: the most recent RPM test results 


   --------------------------------------------------------------------------------


   1) Introduction
      ------------

   This document describes how you can manually extract some GNU Fortran patches
   from the zip file "pc-rules-2017-09-30.tar.xz" and apply them to the source 
   RPM "gcc-4.8.5-16.el7.src.rpm" in a RHEL/CentOS/Oracle-Linux 7.3 system. 

   In specific, the above mentioned zip file (pc-rules-2017-09-30.tar.xz) contains 
   42 unofficial GNU Fortran patches, mainly backports, which have been tested in
   both macOS and Linux. In addition, I've applied them to the source RPM and could
   build and test it without any Fortran regressions.  

   Please note that if you rebuild the default compiler on your system Red Hat 
   might no longer support it.

   To run the instructions of this document you must be familiar with both the RPM
   Building System and Bash scripts. If this isn't the case contact a professional.

   Occasionally, more Fortran related patches are applied to the compiler. See
   Appendix E (this doesn't mean that I test each new patch in the source RPM).


   1.1) Environment
        -----------

         Computer : Mac-Mini quad core i7 (late 2011)
              RAM : 4-GB
           Distro : RHEL 7.3 (Last Update on Aug 13, 2017)
          Machine : x86_64-redhat-linux
   Kernel Version : 3.10.0-514.el7.x86_64
   System Compiler: gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-16)

   So, in my system the installed compiler has the same version with the compiler
   I patch.

   The first time I built this package on Aug 15, 2017, I started the building
   process at 17:40 and finished at 22:20 (4 hours and 40 minutes).


   1.2) Prerequisites & Dependencies
        ----------------------------

   When you start the building process, you will be informed about any missing
   dependencies but some packages aren't downloaded from the default repository.

   In addition to the default repo channel, I needed another two: 
   a) rhel-7-server-source-rpms
   b) rhel-7-server-optional-rpms

   Although my system is x86_64, I had also to install the 686 version of glibc:
   c) glibc.i686
   d) glibc-devel.i686
   e) glibc.x86_64
   f) glibc-devel.x86_64

   One package required for the tests is "autogen", not mentioned as a prerequisite.
   g) autogen-5.18


   1.3) Known Issues
        ------------

   Some test failures during the RPM Build are listed in Appendix G. None of 
   them is Fortran relevant though. The ASAN test failures are likely caused
   by out of date test cases that don't match properly the sanitiser messages. 


   2) Step by Step Instructions to Apply the Fortran Patches
      ------------------------------------------------------

   2.1) Download & Setup the PC Script
        ------------------------------
   You should download a tested tarball. Cross check with the date reported in Appendix G.

   curl -L -k \
   https://github.com/drikosev/pc/raw/master/pc-rules-2017-09-30.tar.xz \
   -o ${HOME}/Downloads/pc-rules-2017-09-30.tar.xz

   Confirm that the tarball has the sha1 stamp "6550dfc6ce456cb08728ceb9181be66fed6cb90a": 
   openssl sha1 ${HOME}/Downloads/pc-rules-2017-09-30.tar.xz | awk '{print $2}'

   Setup a working area for the pc:
   install -d ~/pc 
   cd ~/pc 
   tar xf ~/Downloads/pc-rules-2017-09-30.tar.xz 
   ln -sf rules/port port
   ./port details gcc48 | grep patches


   2.2) Copy the Fortran Patches to the ~/rpmbuild/SOURCES Directory
        ------------------------------------------------------------

   Once the "pc-rules-2017-09-30.tar.xz" tarball has been extracted to $HOME/pc, 
   run all the commands listed in Appendix A.


   2.3) Install the Source RPM

   At first, install any official recommended updates and then the Source
   RPM of gcc-4.8.5

   If you don't have subscribed to the sources channel, type first:
   sudo  subscription-manager repos --enable=rhel-7-server-source-rpms

   Download the Source RPM for gcc, open a terminal in that directory and type:
   rpm -i gcc-4.8.5-16.el7.src.rpm


   2.4) Update the gcc.spec File

   Add all patch declarations listed in Appendix B below to the gcc.spec
   file after the line: Patch1200: cloog-%{cloog_version}-ppc64le-config.patch

   Add all patch instructions listed in Appendix C below to the gcc.spec
   file after the line: %patch1200 -p0 -b .cloog-ppc64le-config~ 


   2.5) Install any missing Prerequisites

   Here are listed some issues I faced. You might face them also.

   -Many dependencies (ie sharutils) are found in the "optionals" channel. If you have not
   activated a subscription to it, type: 
   sudo subscription-manager repos --enable=rhel-7-server-optional-rpms

   -Although my system is x86_64, the failed dependencies like "/lib/libc.so.6" were solved by:
   sudo yum install glibc.i686
   sudo yum install glibc-devel.i686
   (try: sudo yum whatprovides /usr/lib/libc.so)

   Also, some tests during the RPM building process require "autogen", which isn't
   mentioned in the RPM dependencies. Type:
   sudo yum install autogen-5.18


   2.6) Build the RPM

   Start a new terminal session!

   Run the following commands to build the "gcc-4.8.5-16.el7.src.rpm":
   cd ~/rpmbuild
   export RPM_BUILD_NCPUS=2
   export LD_LIBRARY_PATH=""
   export PATH=/usr/bin:/usr/sbin:/bin:/sbin:$PATH
   rpmbuild -ba SPECS/gcc.spec --target x86_64  


   2.7) Install the new Compiler

   To install all the sub-packages of the new compiler run all the commands
   listed in Appendix D.

   ------------------------------------------------------------------------

Appendix A
----------

cd ~/pc/rules/patches/gcc48    
cp gcc48-pr57549.patch  ~/rpmbuild/SOURCES
cp gcc48-tc57549.patch  ~/rpmbuild/SOURCES
cp gcc48-pr56650.patch  ~/rpmbuild/SOURCES
cp gcc48-tc56650.patch  ~/rpmbuild/SOURCES
cp gcc48-pr65429.patch  ~/rpmbuild/SOURCES
cp gcc48-pr52153.patch  ~/rpmbuild/SOURCES
cp gcc48-pr59746.patch  ~/rpmbuild/SOURCES
cp gcc48-pr44265.patch  ~/rpmbuild/SOURCES
cp gcc48-pr59997.patch  ~/rpmbuild/SOURCES
cp gcc48-pr61960.patch  ~/rpmbuild/SOURCES
cp gcc48-pr64925.patch  ~/rpmbuild/SOURCES
cp gcc48-pr52832.patch  ~/rpmbuild/SOURCES
cp gcc48-pr58991.patch  ~/rpmbuild/SOURCES
cp gcc48-pr58618.patch  ~/rpmbuild/SOURCES
cp gcc48-pr57530.patch  ~/rpmbuild/SOURCES
cp gcc48-pr58586.patch  ~/rpmbuild/SOURCES
cp gcc48-pr60357.patch  ~/rpmbuild/SOURCES
cp gcc48-pr65792.patch  ~/rpmbuild/SOURCES
cp gcc48-pr66052.patch  ~/rpmbuild/SOURCES
cp gcc48-pr66044.patch  ~/rpmbuild/SOURCES
cp gcc48-pr66040.patch  ~/rpmbuild/SOURCES
cp gcc48-pr66043.patch  ~/rpmbuild/SOURCES
cp gcc48-pr58749.patch  ~/rpmbuild/SOURCES
cp gcc48-pr66245.patch  ~/rpmbuild/SOURCES
cp gcc48-pr66377.patch  ~/rpmbuild/SOURCES
cp gcc48-pr66113.patch  ~/rpmbuild/SOURCES
cp gcc48-pr51976.patch  ~/rpmbuild/SOURCES
cp gcc48-tc51976.patch  ~/rpmbuild/SOURCES
cp gcc48-pr60593.patch  ~/rpmbuild/SOURCES
cp gcc48-pr45689.patch  ~/rpmbuild/SOURCES
cp gcc48-tc45689.patch  ~/rpmbuild/SOURCES
cp gcc48-pr56650.relax  ~/rpmbuild/SOURCES
cp gcc48-realloc.patch  ~/rpmbuild/SOURCES
cp gcc48-assumed.istat  ~/rpmbuild/SOURCES
cp gcc48-pr58586.again  ~/rpmbuild/SOURCES
cp gcc48-pr63667.patch  ~/rpmbuild/SOURCES
cp gcc48-tc64230.patch  ~/rpmbuild/SOURCES
cp gcc48-tc64980.patch  ~/rpmbuild/SOURCES
cp gcc48-pr45516.patch  ~/rpmbuild/SOURCES
cp gcc48-tc45516.patch  ~/rpmbuild/SOURCES
cp gcc48-pr52162.patch  ~/rpmbuild/SOURCES
cp gcc48-pr64933.patch  ~/rpmbuild/SOURCES


Appendix B
----------

Patch9042:  gcc48-pr57549.patch
Patch9043:  gcc48-tc57549.patch
Patch9044:  gcc48-pr56650.patch
Patch9045:  gcc48-tc56650.patch
Patch9046:  gcc48-pr65429.patch
Patch9047:  gcc48-pr52153.patch
Patch9048:  gcc48-pr59746.patch
Patch9049:  gcc48-pr44265.patch
Patch9050:  gcc48-pr59997.patch
Patch9051:  gcc48-pr61960.patch
Patch9052:  gcc48-pr64925.patch
Patch9053:  gcc48-pr52832.patch
Patch9054:  gcc48-pr58991.patch
Patch9055:  gcc48-pr58618.patch
Patch9056:  gcc48-pr57530.patch
Patch9057:  gcc48-pr58586.patch
Patch9058:  gcc48-pr60357.patch
Patch9059:  gcc48-pr65792.patch
Patch9060:  gcc48-pr66052.patch
Patch9061:  gcc48-pr66044.patch
Patch9062:  gcc48-pr66040.patch
Patch9063:  gcc48-pr66043.patch
Patch9064:  gcc48-pr58749.patch
Patch9065:  gcc48-pr66245.patch
Patch9066:  gcc48-pr66377.patch
Patch9067:  gcc48-pr66113.patch
Patch9068:  gcc48-pr51976.patch
Patch9069:  gcc48-tc51976.patch
Patch9070:  gcc48-pr60593.patch
Patch9071:  gcc48-pr45689.patch
Patch9072:  gcc48-tc45689.patch
Patch9073:  gcc48-pr56650.relax
Patch9074:  gcc48-realloc.patch
Patch9075:  gcc48-assumed.istat
Patch9076:  gcc48-pr58586.again
Patch9077:  gcc48-pr63667.patch
Patch9078:  gcc48-tc64230.patch
Patch9079:  gcc48-tc64980.patch
Patch9080:  gcc48-pr45516.patch
Patch9081:  gcc48-tc45516.patch
Patch9082:  gcc48-pr52162.patch
Patch9083:  gcc48-pr64933.patch  


Appendix C
-------

%patch9042 -p0 -b  .pr57549~
%patch9043 -p0 -b  .tc57549~
%patch9044 -p0 -b  .pr56650~
%patch9045 -p0 -b  .tc56650~
%patch9046 -p0 -b  .pr65429~
%patch9047 -p0 -b  .pr52153~
%patch9048 -p0 -b  .pr59746~
%patch9049 -p0 -b  .pr44265~
%patch9050 -p0 -b  .pr59997~
%patch9051 -p0 -b  .pr61960~
%patch9052 -p0 -b  .pr64925~
%patch9053 -p0 -b  .pr52832~
%patch9054 -p0 -b  .pr58991~
%patch9055 -p0 -b  .pr58618~
%patch9056 -p0 -b  .pr57530~
%patch9057 -p0 -b  .pr58586~
%patch9058 -p0 -b  .pr60357~
%patch9059 -p0 -b  .pr65792~
%patch9060 -p0 -b  .pr66052~
%patch9061 -p0 -b  .pr66044~
%patch9062 -p0 -b  .pr66040~
%patch9063 -p0 -b  .pr66043~
%patch9064 -p0 -b  .pr58749~
%patch9065 -p0 -b  .pr66245~
%patch9066 -p0 -b  .pr66377~
%patch9067 -p0 -b  .pr66113~
%patch9068 -p0 -b  .pr51976~
%patch9069 -p0 -b  .tc51976~
%patch9070 -p0 -b  .pr60593~
%patch9071 -p0 -b  .pr45689~
%patch9072 -p0 -b  .tc45689~
%patch9073 -p0 -b  .pr56650_relax~
%patch9074 -p0 -b  .realloc.patch~
%patch9075 -p0 -b  .assumed.istat~
%patch9076 -p0 -b  .pr58586~
%patch9077 -p0 -b  .pr63667~
%patch9078 -p0 -b  .tc64230~
%patch9079 -p0 -b  .tc64980~
%patch9080 -p0 -b  .pr45516~
%patch9081 -p0 -b  .tc45516.tc~
%patch9082 -p0 -b  .pr52162~
%patch9083 -p0 -b  .pr64933~  


Appendix D
----------

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


Appendix E
----------

  The officially backported Fortran patches to 4.8.5, between 2014-12-23 and
  2015-04-14, are: PR/64244, PR/63733, PR/57023, PR/56867, PR/64528, PR/63744,
  PR/60898, PR/65024, PR/61138, PR/56674, PR/58813, PR/59016, and PR/59024.

- Patch: "gcc48-pr56650.relax" (7.1 backport)
  [2017-08-16]      
  This patch restricts the conditions that an error message is issued. If you apply
  the "gcc48-pr56650.patch" but not the "gcc48-pr56650.relax", the RPM Building fails 
  (package "gcc-4.8.5-16.el7.src.rpm" in RHEL 7.3). 

- Patch: "gcc48-realloc.patch" (5.1 backport)
  [2017-08-19] 
  It solves a bug for reallocation of arrays with zero length (that's my diagnosis).
  The bug solved was producing a runtime error only in Linux (see "realloc0last.f90").

- Patch: "gcc48-assume.istat"
  [2017-08-19] 
  It's a hack that mutes some deallocation errors with the option "-std=legacy"
  but without the option "-pedantic". See the program "2slop.f90" below.

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

- Patch: "gcc48-pr45516.patch", "gcc48-tc45516.patch" (7.1 backport)
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


Appendix F
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


Appendix G - Test Failures During the RPM Build
-----------------------------------------------
[2017-09-30]

Some test failures I faced during the RPM Build on 2017-09-30 include, but not limited to: 

...
Running target unix/
...
Running /home/suser/rpmbuild/BUILD/gcc-4.8.5-20150702/gcc/testsuite/g++.dg/asan/asan.exp ...
FAIL: g++.dg/asan/asan_test.C  -O2  AddressSanitizer_SimpleStackTest A[kSize + 31] = 0 execution test
FAIL: g++.dg/asan/asan_test.C  -O2  AddressSanitizer_SimpleStackTest A[kSize + 31] = 0 execution test
FAIL: g++.dg/asan/asan_test.C  -O2  AddressSanitizer_SimpleStackTest A[kSize + 31] = 0 execution test
FAIL: g++.dg/asan/asan_test.C  -O2  AddressSanitizer_SimpleStackTest A[kSize + 31] = 0 execution test
...
		=== g++ Summary for unix//-fstack-protector ===

# of expected passes		56

		=== g++ Summary ===

# of expected passes		19938
# of unexpected failures	4
...

FAIL: g++.dg/fstack-protector-strong.C -std=gnu++98  scan-assembler-times stack_chk_fail 2
FAIL: g++.dg/fstack-protector-strong.C -std=gnu++11  scan-assembler-times stack_chk_fail 2
...
		=== g++ Summary for unix//-fstack-protector ===

# of expected passes		27750
# of unexpected failures	2
...

Running /home/suser/rpmbuild/BUILD/gcc-4.8.5-20150702/gcc/testsuite/g++.dg/torture/dg-torture.exp ...
FAIL: gcc.dg/fstack-protector-strong.c scan-assembler-times stack_chk_fail 10
FAIL: gcc.dg/stack-usage-1.c scan-file foo\t(256|264)\tstatic
FAIL: gcc.dg/superblock.c scan-rtl-dump-times sched2 "ADVANCING TO" 2
...
		=== gcc Summary for unix//-fstack-protector ===

# of expected passes		15081
# of unexpected failures	3
# of expected failures		65
# of unsupported tests		105


...
Running target unix//-fstack-protector
Using /usr/share/dejagnu/baseboards/unix.exp as board description file for target.
Using /usr/share/dejagnu/config/unix.exp as generic interface file for target.
Using /home/suser/rpmbuild/BUILD/gcc-4.8.5-20150702/gcc/testsuite/config/default.exp as tool-and-target-specific interface file.
Running /home/suser/rpmbuild/BUILD/gcc-4.8.5-20150702/gcc/testsuite/gfortran.dg/dg.exp ...
XPASS: gcc.dg/guality/example.c  -O0  execution test
XPASS: gcc.dg/guality/example.c  -O1  execution test
XPASS: gcc.dg/guality/example.c  -O2  execution test
XPASS: gcc.dg/guality/example.c  -Os  execution test
XPASS: gcc.dg/guality/example.c  -O2 -flto -fno-use-linker-plugin -flto-partition=none  execution test
XPASS: gcc.dg/guality/guality.c  -O0  execution test
XPASS: gcc.dg/guality/guality.c  -O1  execution test
XPASS: gcc.dg/guality/guality.c  -O2  execution test
XPASS: gcc.dg/guality/guality.c  -O3 -fomit-frame-pointer  execution test
XPASS: gcc.dg/guality/guality.c  -O3 -g  execution test
XPASS: gcc.dg/guality/guality.c  -Os  execution test
XPASS: gcc.dg/guality/guality.c  -O2 -flto -fno-use-linker-plugin -flto-partition=none  execution test
XPASS: gcc.dg/guality/guality.c  -O2 -flto -fuse-linker-plugin -fno-fat-lto-objects  execution test
XPASS: gcc.dg/guality/inline-params.c  -O2  execution test
XPASS: gcc.dg/guality/inline-params.c  -O3 -fomit-frame-pointer  execution test
XPASS: gcc.dg/guality/inline-params.c  -O3 -g  execution test
XPASS: gcc.dg/guality/inline-params.c  -Os  execution test
XPASS: gcc.dg/guality/inline-params.c  -O2 -flto -fno-use-linker-plugin -flto-partition=none  execution test
XPASS: gcc.dg/guality/pr41353-1.c  -O0  line 28 j == 28 + 37
XPASS: gcc.dg/guality/pr41353-1.c  -O1  line 28 j == 28 + 37
XPASS: gcc.dg/guality/pr41353-1.c  -O2  line 28 j == 28 + 37
XPASS: gcc.dg/guality/pr41353-1.c  -O3 -fomit-frame-pointer  line 28 j == 28 + 37
XPASS: gcc.dg/guality/pr41353-1.c  -O3 -g  line 28 j == 28 + 37
XPASS: gcc.dg/guality/pr41353-1.c  -Os  line 28 j == 28 + 37
XPASS: gcc.dg/guality/pr41353-1.c  -O2 -flto -fno-use-linker-plugin -flto-partition=none  line 28 j == 28 + 37
XPASS: gcc.dg/guality/pr41353-1.c  -O2 -flto -fuse-linker-plugin -fno-fat-lto-objects  line 28 j == 28 + 37
XPASS: gcc.dg/guality/pr41447-1.c  -O0  execution test
XPASS: gcc.dg/guality/pr41447-1.c  -O1  execution test
XPASS: gcc.dg/guality/pr41447-1.c  -O2  execution test
XPASS: gcc.dg/guality/pr41447-1.c  -O3 -fomit-frame-pointer  execution test
XPASS: gcc.dg/guality/pr41447-1.c  -O3 -g  execution test
XPASS: gcc.dg/guality/pr41447-1.c  -Os  execution test
XPASS: gcc.dg/guality/pr41447-1.c  -O2 -flto -fno-use-linker-plugin -flto-partition=none  execution test
XPASS: gcc.dg/guality/pr41447-1.c  -O2 -flto -fuse-linker-plugin -fno-fat-lto-objects  execution test
XPASS: gcc.dg/guality/pr41616-1.c  -O0  execution test
XPASS: gcc.dg/guality/pr41616-1.c  -O1  execution test
XPASS: gcc.dg/guality/pr41616-1.c  -O2  execution test
XPASS: gcc.dg/guality/pr41616-1.c  -O3 -fomit-frame-pointer  execution test
XPASS: gcc.dg/guality/pr41616-1.c  -O3 -g  execution test
XPASS: gcc.dg/guality/pr41616-1.c  -Os  execution test
XPASS: gcc.dg/guality/pr41616-1.c  -O2 -flto -fno-use-linker-plugin -flto-partition=none  execution test
FAIL: gcc.dg/guality/pr43051-1.c  -O3 -fomit-frame-pointer -funroll-loops  line 39 c == &a[0]
FAIL: gcc.dg/guality/pr43051-1.c  -O3 -fomit-frame-pointer -funroll-all-loops -finline-functions  line 39 c == &a[0]
FAIL: gcc.dg/guality/pr54200.c  -Os  line 20 z == 3
FAIL: gcc.dg/guality/pr54519-1.c  -O2 -flto -fno-use-linker-plugin -flto-partition=none  line 20 y == 25
FAIL: gcc.dg/guality/pr54519-1.c  -O2 -flto -fno-use-linker-plugin -flto-partition=none  line 20 z == 6
FAIL: gcc.dg/guality/pr54519-1.c  -O2 -flto -fno-use-linker-plugin -flto-partition=none  line 23 y == 117
FAIL: gcc.dg/guality/pr54519-1.c  -O2 -flto -fno-use-linker-plugin -flto-partition=none  line 23 z == 8
FAIL: gcc.dg/guality/pr54519-1.c  -O2 -flto -fuse-linker-plugin -fno-fat-lto-objects  line 20 y == 25
FAIL: gcc.dg/guality/pr54519-1.c  -O2 -flto -fuse-linker-plugin -fno-fat-lto-objects  line 20 z == 6
FAIL: gcc.dg/guality/pr54519-2.c  -O2 -flto -fno-use-linker-plugin -flto-partition=none  line 17 y == 25
FAIL: gcc.dg/guality/pr54519-2.c  -O2 -flto -fuse-linker-plugin -fno-fat-lto-objects  line 17 y == 25
FAIL: gcc.dg/guality/pr54519-3.c  -O2 -flto -fuse-linker-plugin -fno-fat-lto-objects  line 20 z == 6
FAIL: gcc.dg/guality/pr54519-3.c  -O2 -flto -fuse-linker-plugin -fno-fat-lto-objects  line 23 z == 8
FAIL: gcc.dg/guality/pr54519-4.c  -O2 -flto -fuse-linker-plugin -fno-fat-lto-objects  line 17 y == 25
FAIL: gcc.dg/guality/pr54519-5.c  -O2 -flto -fno-use-linker-plugin -flto-partition=none  line 17 y == 25
FAIL: gcc.dg/guality/pr54519-5.c  -O2 -flto -fuse-linker-plugin -fno-fat-lto-objects  line 17 y == 25

...

		=== gfortran Summary for unix//-fstack-protector ===

# of expected passes		6105
# of expected failures		25
# of unsupported tests		1

		=== gfortran Summary ===

# of expected passes		12210
# of expected failures		50
# of unsupported tests		2

...

		=== gfortran Summary for unix/ ===

# of expected passes		6196
# of expected failures		6

...

+-docs-4.8.5/html/api': No space left on device
error: Bad exit status from /var/tmp/rpm-tmp.CbcTIJ (%doc)


RPM build errors:
    Bad exit status from /var/tmp/rpm-tmp.CbcTIJ (%doc)
[suser@miniserver rpmbuild]$
