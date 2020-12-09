
Dec 08, 2020 


                 FORTRAN PATCHES FOR GCC 4.8.5 in CentOS 7.6
                 -------------------------------------------

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
      Appendix E: a short list with the first added patches
      Appendix G: the last RPM test results 


   --------------------------------------------------------------------------------


   1) Introduction
      ------------

   This document describes how you can manually extract some GNU Fortran patches
   from the zip file "pc-rules-2020-12-06.tar.bz2" and apply them to the source 
   RPM "gcc-4.8.5-44.0.3.el7.src.rpm" in a RHEL/CentOS/Oracle-Linux 7.6 system. 

   In specific, the above mentioned zip file (pc-rules-2020-12-06.tar.bz2) contains 
   146 unofficial GNU Fortran patches, mainly backports, which have been tested on
   both macOS and Linux. In addition, I've applied them to the source RPM and could
   build and test it without any Fortran regressions. 

   Note however that the Fortran library won't be fully compatible with older ones,
   which means that you may have to rebuild existing Fortran projects. 

   Please note that if you rebuild the default compiler on your system, Red Hat 
   may no longer support it. This document was originally written for a RHEL-7.3
   system but currently I use CentOS-7.6 and download sources manually from Oracle.
   Whereas, the distribution channels mentioned below could be used by RHEL users.

   To run the instructions of this document you must be familiar with both the RPM
   Building System and Bash scripts. If this isn't the case contact a professional.

   Occasionally, more Fortran patches are applied to the compiler. See Appendix E
   (this doesn't mean that I test each new patch in the source RPM).


   1.1) Environment
        -----------

         Computer : Mac-Mini quad core i7 (Mid 2011)
              RAM : 4-GB
           Distro : CentOS 7.6
          Machine : x86_64-redhat-linux
   Kernel Version : 3.10.0-957.el7.x86_64
   System Compiler: gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-39)

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

   As a CentOS user I now install the above packages from the CentOS-7.6 (DVD) disk.


   1.3) Known Issues
        ------------

   Some test failures during the RPM Build are listed in Appendix G. None of 
   them is Fortran relevant though. The ASAN test failures are perhaps caused
   by outdated test cases that don't match precisely the sanitiser messages. Yet,
   I faced them only while testing/running for target unix//-fstack-protector.


   2) Step by Step Instructions to Apply the Fortran Patches
      ------------------------------------------------------

   2.1) Download & Setup the PC Script
        ------------------------------
   You should download a tested tarball. Cross check with the date reported in Appendix G.

   curl -L -k \
   https://github.com/drikosev/pc/raw/master/pc-rules-2020-12-06.tar.bz2 \
   -o ${HOME}/Downloads/pc-rules-2020-12-06.tar.bz2

   Confirm that the tarball has the sha1 stamp "47f1a22e7727349dc821b2198cec9cfa2185d4c6": 
   openssl sha1 ${HOME}/Downloads/pc-rules-2020-12-06.tar.bz2 | awk '{print $2}'

   Setup a working area for the pc:
   install -d ~/pc 
   cd ~/pc 
   tar xf ~/Downloads/pc-rules-2020-12-06.tar.bz2 
   ln -sf rules/port port
   ./port details gcc48 | grep patches


   2.2) Copy the Fortran Patches to the ~/rpmbuild/SOURCES Directory
        ------------------------------------------------------------

   Once the "pc-rules-2020-12-06.tar.bz2" tarball has been extracted to $HOME/pc, 
   run all the commands listed in Appendix A.


   2.3) Install the Source RPM

   At first, install any official recommended updates and then the Source
   RPM of gcc-4.8.5

   If you don't have subscribed to the sources channel, type first:
   sudo  subscription-manager repos --enable=rhel-7-server-source-rpms

   Whereas, with CentOS-7.6, the file below can be downloaded from Oracle. So,
   download the Source RPM for gcc, open a terminal in that directory and type:
   rpm -i gcc-4.8.5-44.0.3.el7.src.rpm


   2.4) Update the gcc.spec File

   You may have to disable Ada, so set this: global build_ada 0
   You may have to disable also C++ docs: global build_libstdcxx_docs 0

   To apply our patches last, follow these two steps:

   Add all patch declarations listed in Appendix B below to the gcc.spec
   file before the line: # On ARM EABI systems

   Add all patch instructions listed in Appendix C below to the gcc.spec
   file before the line: sed -i -e 's/4\.8\.5/4.8.5/' gcc/BASE-VER 


   2.5) Install any missing Prerequisites

   Here are listed some issues I had faced with RHEL-7.3. You might face them also.

   -Many dependencies (ie sharutils) are found in the "optionals" channel. If you have
   not activated a subscription to it, type: 
   sudo subscription-manager repos --enable=rhel-7-server-optional-rpms

   -Although my system is x86_64, the failed dependencies like "/lib/libc.so.6" were
    solved by:
   sudo yum install glibc.i686
   sudo yum install glibc-devel.i686
   (try: sudo yum whatprovides /usr/lib/libc.so)

   Also, some tests during the RPM building process require "autogen", which isn't
   mentioned in the RPM dependencies. Type:
   sudo yum install autogen-5.18


   2.6) Build the RPM

   Start a new terminal session!

   Run the following commands to build the "gcc-4.8.5-44.0.3.el7.src.rpm":
   cd ~/rpmbuild
   export RPM_BUILD_NCPUS=2
   export LD_LIBRARY_PATH=""
   export PATH=/usr/bin:/usr/sbin:/bin:/sbin:$PATH
   rpmbuild --noclean -ba SPECS/gcc.spec --target x86_64  


   2.7) Install the new Compiler

   To install all the sub-packages of the new compiler run all the commands
   listed in Appendix D.

   ------------------------------------------------------------------------

Appendix A
----------

cd ~/pc/rules/patches/gcc48

cp gcc48-pr69960.patch  ~/rpmbuild/SOURCES
cp gcc48-pr69960.extra  ~/rpmbuild/SOURCES
cp gcc48-s922534.patch  ~/rpmbuild/SOURCES

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
cp gcc48-pr52846.patch  ~/rpmbuild/SOURCES
cp gcc48-tc52846.patch  ~/rpmbuild/SOURCES

cp gcc48-pr82814.patch  ~/rpmbuild/SOURCES
cp gcc48-pr60255.patch  ~/rpmbuild/SOURCES
cp gcc48-tc60255.patch  ~/rpmbuild/SOURCES
cp gcc48-pr69566.patch  ~/rpmbuild/SOURCES
cp gcc48-pr64578.patch  ~/rpmbuild/SOURCES
cp gcc48-pr70397.patch  ~/rpmbuild/SOURCES
cp gcc48-pr63230.patch  ~/rpmbuild/SOURCES
cp gcc48-bindptr.patch  ~/rpmbuild/SOURCES
cp gcc48-pr61261.patch  ~/rpmbuild/SOURCES
cp gcc48-tc64787.patch  ~/rpmbuild/SOURCES
cp gcc48-pr49954.patch  ~/rpmbuild/SOURCES
cp gcc48-pr80945.patch  ~/rpmbuild/SOURCES
cp gcc48-pr54070.patch  ~/rpmbuild/SOURCES
cp gcc48-pr66911.patch  ~/rpmbuild/SOURCES
cp gcc48-pr43366.patch  ~/rpmbuild/SOURCES
cp gcc48-pr87625.patch  ~/rpmbuild/SOURCES

cp gcc48-pr43366.part2  ~/rpmbuild/SOURCES
cp gcc48-pr70149.patch  ~/rpmbuild/SOURCES
cp gcc48-pr85954.patch  ~/rpmbuild/SOURCES
cp gcc48-pr34640.part1  ~/rpmbuild/SOURCES
cp gcc48-pr86863.patch  ~/rpmbuild/SOURCES
cp gcc48-pr69834.patch  ~/rpmbuild/SOURCES
cp gcc48-pr69742.patch  ~/rpmbuild/SOURCES
cp gcc48-tc34640.patch  ~/rpmbuild/SOURCES
cp gcc48-pr65548.patch  ~/rpmbuild/SOURCES
cp gcc48-pr67564.patch  ~/rpmbuild/SOURCES
cp gcc48-pr66927.patch  ~/rpmbuild/SOURCES
cp gcc48-pr34640.part2  ~/rpmbuild/SOURCES
cp gcc48-pr85603.patch  ~/rpmbuild/SOURCES
cp gcc48-pr85603.extra  ~/rpmbuild/SOURCES
cp gcc48-pr49074.patch  ~/rpmbuild/SOURCES

cp gcc48-pr62044.undo  ~/rpmbuild/SOURCES
cp gcc48-pr63570.patch  ~/rpmbuild/SOURCES
cp gcc48-pr84074.patch  ~/rpmbuild/SOURCES
cp gcc48-pr66929.patch  ~/rpmbuild/SOURCES
cp gcc48-pr59026.patch  ~/rpmbuild/SOURCES
cp gcc48-pr49630.patch  ~/rpmbuild/SOURCES
cp gcc48-pr57285.patch  ~/rpmbuild/SOURCES
cp gcc48-pr78300.patch  ~/rpmbuild/SOURCES
cp gcc48-pr78990.patch  ~/rpmbuild/SOURCES
cp gcc48-pr63205.patch  ~/rpmbuild/SOURCES
cp gcc48-pr60322.patch  ~/rpmbuild/SOURCES
cp gcc48-pr80477.patch  ~/rpmbuild/SOURCES
cp gcc48-pr49074.86116  ~/rpmbuild/SOURCES
cp gcc48-pr57117.patch  ~/rpmbuild/SOURCES
cp gcc48-pr78356.patch  ~/rpmbuild/SOURCES

cp gcc48-pr37336.patch  ~/rpmbuild/SOURCES
cp gcc48-tc80477.patch  ~/rpmbuild/SOURCES
cp gcc48-pr83149.patch  ~/rpmbuild/SOURCES
cp gcc48-pr33430.patch  ~/rpmbuild/SOURCES
cp gcc48-pr80392.patch  ~/rpmbuild/SOURCES
cp gcc48-pr36192.patch  ~/rpmbuild/SOURCES
cp gcc48-pr61454.patch  ~/rpmbuild/SOURCES
cp gcc48-pr67526.patch  ~/rpmbuild/SOURCES
cp gcc48-pr68153.patch  ~/rpmbuild/SOURCES
cp gcc48-pr71067.patch  ~/rpmbuild/SOURCES
cp gcc48-pr83864.patch  ~/rpmbuild/SOURCES
cp gcc48-pr54613.patch  ~/rpmbuild/SOURCES
cp gcc48-pr54613.linux  ~/rpmbuild/SOURCES
cp gcc48-pr92785.patch  ~/rpmbuild/SOURCES
cp gcc48-pr57093.patch  ~/rpmbuild/SOURCES
cp gcc48-pr82886.patch  ~/rpmbuild/SOURCES

cp gcc48-pr87352.patch  ~/rpmbuild/SOURCES
cp gcc48-pr44672.patch  ~/rpmbuild/SOURCES
cp gcc48-pr85780.patch  ~/rpmbuild/SOURCES
cp gcc48-pr88326.patch  ~/rpmbuild/SOURCES
cp gcc48-pr81701.patch  ~/rpmbuild/SOURCES
cp gcc48-pr64432.patch  ~/rpmbuild/SOURCES
cp gcc48-pr63921.patch  ~/rpmbuild/SOURCES
cp gcc48-pr67721.patch  ~/rpmbuild/SOURCES
cp gcc48-pr54949.patch  ~/rpmbuild/SOURCES
cp gcc48-pr77374.patch  ~/rpmbuild/SOURCES
cp gcc48-pr65894.patch  ~/rpmbuild/SOURCES
cp gcc48-pr91863.patch  ~/rpmbuild/SOURCES
cp gcc48-std2018.patch  ~/rpmbuild/SOURCES
cp gcc48-pr78534.patch  ~/rpmbuild/SOURCES
cp gcc48-pr44265.extra  ~/rpmbuild/SOURCES
cp gcc48-pr69834.extra  ~/rpmbuild/SOURCES

cp gcc48-pr92976.patch  ~/rpmbuild/SOURCES
cp gcc48-pr90329.patch  ~/rpmbuild/SOURCES
cp gcc48-pr80118.patch  ~/rpmbuild/SOURCES
cp gcc48-pr70260.patch  ~/rpmbuild/SOURCES
cp gcc48-2calloc.patch  ~/rpmbuild/SOURCES
cp gcc48-pr52846.extra  ~/rpmbuild/SOURCES
cp gcc48-pr67900.patch  ~/rpmbuild/SOURCES
cp gcc48-pr71203.patch  ~/rpmbuild/SOURCES
cp gcc48-pr52413.patch  ~/rpmbuild/SOURCES
cp gcc48-pr61632.patch  ~/rpmbuild/SOURCES
cp gcc48-pr35203.patch  ~/rpmbuild/SOURCES
cp gcc48-pr82995.patch  ~/rpmbuild/SOURCES

cp gcc48-pr55117.patch  ~/rpmbuild/SOURCES
cp gcc48-pr36313.patch  ~/rpmbuild/SOURCES
cp gcc48-pr60355.patch  ~/rpmbuild/SOURCES
cp gcc48-pr82143.patch  ~/rpmbuild/SOURCES
cp gcc48-pr92959.patch  ~/rpmbuild/SOURCES
cp gcc48-pr93498.patch  ~/rpmbuild/SOURCES
cp gcc48-pr93686.patch  ~/rpmbuild/SOURCES
cp gcc48-pr65428.patch  ~/rpmbuild/SOURCES
cp gcc48-pr93835.patch  ~/rpmbuild/SOURCES
cp gcc48-pr93601.patch  ~/rpmbuild/SOURCES
cp gcc48-pr93580.patch  ~/rpmbuild/SOURCES
cp gcc48-pr93635.patch  ~/rpmbuild/SOURCES
cp gcc48-pr98016.patch  ~/rpmbuild/SOURCES


Note:
If you want to convert the characters length field from int to size_t, then run:

sed -i "s/define  LONG_CHARLEN 0/define  LONG_CHARLEN 1/g" \
        ~/rpmbuild/SOURCES/gcc48-pr78534.patch

Yet, this option will change only the API, not the actual limit!


Appendix B
----------

Patch9001: gcc48-pr69960.patch 
Patch9002: gcc48-pr69960.extra 
Patch9003: gcc48-s922534.patch

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
Patch9076: gcc48-pr58586.again
Patch9077: gcc48-pr63667.patch
Patch9078: gcc48-tc64230.patch
Patch9079: gcc48-tc64980.patch
Patch9080: gcc48-pr45516.patch
Patch9081: gcc48-tc45516.patch
Patch9082: gcc48-pr52162.patch
Patch9083: gcc48-pr64933.patch
Patch9084: gcc48-pr52846.patch
Patch9085: gcc48-tc52846.patch
Patch9086: gcc48-pr82814.patch
Patch9087: gcc48-pr60255.patch
Patch9088: gcc48-tc60255.patch
Patch9089: gcc48-pr69566.patch
Patch9090: gcc48-pr64578.patch
Patch9091: gcc48-pr70397.patch
Patch9092: gcc48-pr63230.patch
Patch9093: gcc48-bindptr.patch
Patch9094: gcc48-pr61261.patch
Patch9095: gcc48-tc64787.patch
Patch9096: gcc48-pr49954.patch
Patch9097: gcc48-pr80945.patch
Patch9098: gcc48-pr54070.patch
Patch9099: gcc48-pr66911.patch
Patch9100: gcc48-pr43366.patch
Patch9101: gcc48-pr87625.patch
Patch9102: gcc48-pr43366.part2
Patch9103: gcc48-pr70149.patch
Patch9104: gcc48-pr85954.patch
Patch9105: gcc48-pr34640.part1
Patch9106: gcc48-pr86863.patch
Patch9107: gcc48-pr69834.patch
Patch9108: gcc48-pr69742.patch
Patch9109: gcc48-tc34640.patch
Patch9110: gcc48-pr65548.patch
Patch9111: gcc48-pr67564.patch
Patch9112: gcc48-pr66927.patch
Patch9113: gcc48-pr34640.part2
Patch9114: gcc48-pr85603.patch
Patch9115: gcc48-pr85603.extra
Patch9116: gcc48-pr49074.patch
Patch9117: gcc48-pr62044.undo
Patch9118: gcc48-pr63570.patch
Patch9119: gcc48-pr84074.patch
Patch9120: gcc48-pr66929.patch
Patch9121: gcc48-pr59026.patch
Patch9122: gcc48-pr49630.patch
Patch9123: gcc48-pr57285.patch
Patch9124: gcc48-pr78300.patch
Patch9125: gcc48-pr78990.patch
Patch9126: gcc48-pr63205.patch
Patch9127: gcc48-pr60322.patch
Patch9128: gcc48-pr80477.patch
Patch9129: gcc48-pr49074.86116
Patch9130: gcc48-pr57117.patch
Patch9131: gcc48-pr78356.patch
Patch9132: gcc48-pr37336.patch
Patch9133: gcc48-tc80477.patch
Patch9134: gcc48-pr83149.patch
Patch9135: gcc48-pr33430.patch
Patch9136: gcc48-pr80392.patch
Patch9137: gcc48-pr36192.patch
Patch9138: gcc48-pr61454.patch
Patch9139: gcc48-pr67526.patch
Patch9140: gcc48-pr68153.patch
Patch9141: gcc48-pr71067.patch
Patch9142: gcc48-pr83864.patch
Patch9143: gcc48-pr54613.patch
Patch9144: gcc48-pr54613.linux
Patch9145: gcc48-pr92785.patch
Patch9146: gcc48-pr57093.patch
Patch9147: gcc48-pr82886.patch
Patch9148: gcc48-pr87352.patch
Patch9149: gcc48-pr44672.patch
Patch9150: gcc48-pr85780.patch
Patch9151: gcc48-pr88326.patch
Patch9152: gcc48-pr81701.patch
Patch9153: gcc48-pr64432.patch
Patch9154: gcc48-pr63921.patch
Patch9155: gcc48-pr67721.patch
Patch9156: gcc48-pr54949.patch
Patch9157: gcc48-pr77374.patch
Patch9158: gcc48-pr65894.patch
Patch9159: gcc48-pr91863.patch
Patch9160: gcc48-std2018.patch
Patch9161: gcc48-pr78534.patch
Patch9162: gcc48-pr44265.extra
Patch9163: gcc48-pr69834.extra
Patch9164: gcc48-pr92976.patch
Patch9165: gcc48-pr90329.patch
Patch9166: gcc48-pr80118.patch
Patch9167: gcc48-pr70260.patch
Patch9168: gcc48-2calloc.patch
Patch9169: gcc48-pr52846.extra
Patch9170: gcc48-pr67900.patch
Patch9171: gcc48-pr71203.patch
Patch9172: gcc48-pr52413.patch
Patch9173: gcc48-pr61632.patch
Patch9174: gcc48-pr35203.patch
Patch9175: gcc48-pr82995.patch

Patch9176: gcc48-pr55117.patch
Patch9177: gcc48-pr36313.patch
Patch9178: gcc48-pr60355.patch
Patch9179: gcc48-pr82143.patch
Patch9180: gcc48-pr92959.patch
Patch9181: gcc48-pr93498.patch
Patch9182: gcc48-pr93686.patch
Patch9183: gcc48-pr65428.patch
Patch9184: gcc48-pr93835.patch
Patch9185: gcc48-pr93601.patch
Patch9186: gcc48-pr93580.patch
Patch9187: gcc48-pr93635.patch
Patch9188: gcc48-pr98016.patch

Appendix C
-------

%patch9001 -p0 -b .pr69960~ 
%patch9002 -p0 -b .pr69960.extra~
%patch9003 -p0 -b .s922534~

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
%patch9073 -p0 -b .pr56650.relax
%patch9074 -p0 -b .realloc~
%patch9075 -p0 -b .assumed.istat
%patch9076 -p0 -b .pr58586.again
%patch9077 -p0 -b .pr63667~
%patch9078 -p0 -b .tc64230~
%patch9079 -p0 -b .tc64980~
%patch9080 -p0 -b .pr45516~
%patch9081 -p0 -b .tc45516~
%patch9082 -p0 -b .pr52162~
%patch9083 -p0 -b .pr64933~
%patch9084 -p0 -b .pr52846~
%patch9085 -p0 -b .tc52846~
%patch9086 -p0 -b .pr82814~
%patch9087 -p0 -b .pr60255~
%patch9088 -p0 -b .tc60255~
%patch9089 -p0 -b .pr69566~
%patch9090 -p0 -b .pr64578~
%patch9091 -p0 -b .pr70397~
%patch9092 -p0 -b .pr63230~
%patch9093 -p0 -b .bindptr~
%patch9094 -p0 -b .pr61261~
%patch9095 -p0 -b .tc64787~
%patch9096 -p0 -b .pr49954~
%patch9097 -p0 -b .pr80945~
%patch9098 -p0 -b .pr54070~
%patch9099 -p0 -b .pr66911~
%patch9100 -p0 -b .pr43366~
%patch9101 -p0 -b .pr87625~
%patch9102 -p0 -b .pr43366.part2
%patch9103 -p0 -b .pr70149~
%patch9104 -p0 -b .pr85954~
%patch9105 -p0 -b .pr34640.part1
%patch9106 -p0 -b .pr86863~
%patch9107 -p0 -b .pr69834~
%patch9108 -p0 -b .pr69742~
%patch9109 -p0 -b .tc34640~
%patch9110 -p0 -b .pr65548~
%patch9111 -p0 -b .pr67564~
%patch9112 -p0 -b .pr66927~
%patch9113 -p0 -b .pr34640.part2
%patch9114 -p0 -b .pr85603~
%patch9115 -p0 -b .pr85603.extra
%patch9116 -p0 -b .pr49074~
%patch9117 -p0 -b .pr62044.undo
%patch9118 -p0 -b .pr63570~
%patch9119 -p0 -b .pr84074~
%patch9120 -p0 -b .pr66929~
%patch9121 -p0 -b .pr59026~
%patch9122 -p0 -b .pr49630~
%patch9123 -p0 -b .pr57285~
%patch9124 -p0 -b .pr78300~
%patch9125 -p0 -b .pr78990~
%patch9126 -p0 -b .pr63205~
%patch9127 -p0 -b .pr60322~
%patch9128 -p0 -b .pr80477~
%patch9129 -p0 -b .pr49074.86116
%patch9130 -p0 -b .pr57117~
%patch9131 -p0 -b .pr78356~
%patch9132 -p0 -b .pr37336~
%patch9133 -p0 -b .tc80477~
%patch9134 -p0 -b .pr83149~
%patch9135 -p0 -b .pr33430~
%patch9136 -p0 -b .pr80392~
%patch9137 -p0 -b .pr36192~
%patch9138 -p0 -b .pr61454~
%patch9139 -p0 -b .pr67526~
%patch9140 -p0 -b .pr68153~
%patch9141 -p0 -b .pr71067~
%patch9142 -p0 -b .pr83864~
%patch9143 -p0 -b .pr54613~
%patch9144 -p0 -b .pr54613.linux
%patch9145 -p0 -b .pr92785~
%patch9146 -p0 -b .pr57093~
%patch9147 -p0 -b .pr82886~
%patch9148 -p0 -b .pr87352~
%patch9149 -p0 -b .pr44672~
%patch9150 -p0 -b .pr85780~
%patch9151 -p0 -b .pr88326~
%patch9152 -p0 -b .pr81701~
%patch9153 -p0 -b .pr64432~
%patch9154 -p0 -b .pr63921~
%patch9155 -p0 -b .pr67721~
%patch9156 -p0 -b .pr54949~
%patch9157 -p0 -b .pr77374~
%patch9158 -p0 -b .pr65894~
%patch9159 -p0 -b .pr91863~
%patch9160 -p0 -b .std2018~
%patch9161 -p0 -b .pr78534~
%patch9162 -p0 -b .pr44265.extra
%patch9163 -p0 -b .pr69834.extra
%patch9164 -p0 -b .pr92976~
%patch9165 -p0 
%patch9166 -p0 -b .pr80118~
%patch9167 -p0 -b .pr70260~
%patch9168 -p0 -b .2calloc~
%patch9169 -p0 -b .pr52846.extra
%patch9170 -p0 -b .pr67900~
%patch9171 -p0 -b .pr71203~
%patch9172 -p0 -b .pr52413~
%patch9173 -p0 -b .pr61632~
%patch9174 -p0 -b .pr35203~
%patch9175 -p0 -b .pr82995~
%patch9176 -p0 -b .pr55117~
%patch9177 -p0 -b .pr36313~
%patch9178 -p0 -b .pr60355~
%patch9179 -p0 -b .pr82143~
%patch9180 -p0 -b .pr92959~
%patch9181 -p0 -b .pr93498~
%patch9182 -p0 -b .pr93686~
%patch9183 -p0 -b .pr65428~
%patch9184 -p0 -b .pr93835~
%patch9185 -p0 -b .pr93601~
%patch9186 -p0 -b .pr93580~
%patch9187 -p0 -b .pr93635~
%patch9188 -p0 -b .pr98016~


Appendix D
----------

cd ~/rpmbuild/RPMS/x86_64

sudo rpm --force --nodeps -i  cpp-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  gcc-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  gcc-base-debuginfo-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  gcc-c++-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  gcc-debuginfo-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  gcc-gfortran-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  gcc-go-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  gcc-objc-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  gcc-objc++-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  gcc-plugin-devel-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libasan-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libasan-static-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libatomic-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libatomic-static-4.8.5-44.0.3.el7.x86_64.rpm

sudo rpm --force --nodeps -i  libgcc-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libgfortran-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libgfortran-static-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libgo-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libgo-devel-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libgomp-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libgo-static-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libitm-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libitm-devel-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libitm-static-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libmudflap-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libmudflap-devel-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libmudflap-static-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libobjc-4.8.5-44.0.3.el7.x86_64.rpm

sudo rpm --force --nodeps -i  libquadmath-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libquadmath-devel-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libquadmath-static-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libstdc++-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libstdc++-devel-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libstdc++-static-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libtsan-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force --nodeps -i  libtsan-static-4.8.5-44.0.3.el7.x86_64.rpm



#if you have built libgnat along with the C++ documentation also:
sudo rpm --force -i libgnat-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force -i libgnat-devel-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force -i libgnat-static-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force -i gcc-gnat-4.8.5-44.0.3.el7.x86_64.rpm
sudo rpm --force -i libstdc++-docs-4.8.5-44.0.3.el7.x86_64.rpm


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

- Patch: "gcc48-pr52846.patch", "gcc48-tc52846.patch" (7.1 backport)
  [2017-11-18]
  This is a collective patch for Fortran SubModules.

- Patch: "gcc48-pr82814.patch"
  [2017-11-18] 
  It's a bug fix for submodule character functions that hasn't been finalised yet
  and was submitted on 2017-11-17, see:
  https://gcc.gnu.org/bugzilla/show_bug.cgi?id=82814

- Patch: "gcc48-pr60255.patch", "gcc48-tc60255.patch" (4.9 & 7.1 backport)
  [2017-11-24]
  This patch allows deferred character length variables to be associated with 
  unlimited polymorphic entities, see:
  https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60255

- Patch "gcc48-pr69566.patch", (6 backport)
  [2017-11-25]
  It contains a bug fix for the test case "unlimited_polymorphic_25.f03", see:
  https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69566

- Patch "gcc48-pr64578.patch", (5 backport)
  [2017-11-26]
  It contains a bug fix for the test case "unlimited_polymorphic_21.f90", see:
  https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64578

- Patch "gcc48-pr70397.patch", (5 backport)
  [2017-12-01]
  It's a bug fix for the test case "unlimited_polymorphic_26.f90", which presents
  random failures (during the tests in Linux) and "unlimited_polymorphic_24.f90":
  https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70397

- Patch "gcc48-pr63230.patch", (5 backport) 
  [2017-12-04]
  It contains a bug fix for the test case "unlimited_polymorphic_22.f90", see:
  https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63230

- Since 2017 many other patches have been backported.


Appendix F
----------

  The program below demonstrates that the patch "gcc48-realloc.patch" avoids the error:
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
    integer, allocatable,                 dimension(:) :: localarray
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
Running target unix//-fstack-protector
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

[2020-04-29]

I've seen/noticed at least two failures for the first time:

FAIL: gcc.dg/guality/pr36728-1.c  -O1  line 16 arg3 == 3
FAIL: gcc.dg/guality/pr36728-3.c  -O1  line 16 arg3 == 3


[2020-05-11]

The above two failures were reproduced again [Running target unix//-fstack-protector]

FAIL: gcc.dg/guality/pr36728-1.c  -O1  line 16 arg3 == 3
FAIL: gcc.dg/guality/pr36728-3.c  -O1  line 16 arg3 == 3

[2020-05-17]

Same results as above.

[2020-06-10]

Same results as above.

[suser@miniserver rpmbuild]$


---------------------------------------------------------------------------
[2020-10-16]

I've seen/noticed this failure for the first time:

FAIL: gcc.dg/guality/pr54693-2.c  -Os  line 21 x == 10 - i


[suser@miniserver rpmbuild]$

