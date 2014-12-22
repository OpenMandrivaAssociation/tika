%{?_javapackages_macros:%_javapackages_macros}

# Conditionals to help breaking tika <-> vorbis-java-tika dependency cycle
%bcond_with vorbis_tika
# Disable only for now
%bcond_without tika_parsers
%bcond_without tika_app

Name:          tika
Version:       1.5
Release:       1.2
Summary:       A content analysis toolkit
Group:		Development/Java
License:       ASL 2.0
Url:           http://tika.apache.org/
Source0:       http://www.apache.org/dist/tika/%{name}-%{version}-src.zip
# Fix stax-api gId:aId
# Replace unavailable org.ow2.asm:asm-debug-all:4.1
# Replace ant-nodeps with ant
# Fix bouncycastle aId
Patch0:        %{name}-1.4-fix-build-deps.patch
Patch1:        %{name}-1.4-bouncycastle-1.50.patch
BuildRequires: java-devel

BuildRequires: mvn(biz.aQute:bndlib)
BuildRequires: mvn(org.apache.ant:ant)
BuildRequires: mvn(org.osgi:org.osgi.compendium)
BuildRequires: mvn(org.osgi:org.osgi.core)

%if %{with vorbis_tika}
BuildRequires: mvn(org.gagravarr:vorbis-java-tika)
%endif

%if %{with tika_parsers}
BuildRequires: mvn(com.adobe.xmp:xmpcore)
BuildRequires: mvn(com.drewnoakes:metadata-extractor:2)
BuildRequires: mvn(com.uwyn:jhighlight)
BuildRequires: mvn(org.gagravarr:vorbis-java-core)
BuildRequires: mvn(com.googlecode.juniversalchardet:juniversalchardet)
BuildRequires: mvn(commons-codec:commons-codec)
BuildRequires: mvn(de.l3s.boilerpipe:boilerpipe)
BuildRequires: mvn(edu.ucar:netcdf)
BuildRequires: mvn(javax.xml.stream:stax-api)
BuildRequires: mvn(org.apache.commons:commons-compress)
BuildRequires: mvn(org.apache.felix:org.apache.felix.scr.annotations)
BuildRequires: mvn(org.apache.james:apache-mime4j-core)
BuildRequires: mvn(org.apache.james:apache-mime4j-dom)
BuildRequires: mvn(org.apache.james:james-project:pom:)
BuildRequires: mvn(org.apache.pdfbox:pdfbox)
BuildRequires: mvn(org.apache.poi:poi)
BuildRequires: mvn(org.apache.poi:poi-scratchpad)
BuildRequires: mvn(org.apache.poi:poi-ooxml)
BuildRequires: mvn(org.bouncycastle:bcmail-jdk16)
BuildRequires: mvn(org.bouncycastle:bcprov-jdk16)
BuildRequires: mvn(org.ccil.cowan.tagsoup:tagsoup)
BuildRequires: mvn(org.ow2.asm:asm-all)
BuildRequires: mvn(rome:rome)
%if %{with tika_app}
BuildRequires: mvn(com.google.code.gson:gson)
BuildRequires: mvn(log4j:log4j:1.2.17)
BuildRequires: mvn(org.slf4j:slf4j-log4j12)
%endif
%endif

%if 0
# tika-server deps
BuildRequires: mvn(net.sf.opencsv:opencsv:2.0)
BuildRequires: mvn(org.apache.cxf:cxf-rt-frontend-jaxrs:2.6.1)
BuildRequires: mvn(org.apache.cxf:cxf-rt-transports-http-jetty:2.6.1)
# tika-parser deps
BuildRequires: mvn(com.googlecode.mp4parser:mp4parser-project:1.0-RC-1)
BuildRequires: mvn(com.googlecode.mp4parser:isoparser:1.0-RC-1)
# tika-xmp
BuildRequires: mvn(org.apache.felix:maven-scr-plugin:1.7.4)
%endif

# Test deps
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.mockito:mockito-core)
BuildRequires: mvn(xml-apis:xml-apis)

BuildRequires: maven-local
BuildRequires: maven-failsafe-plugin
BuildRequires: maven-plugin-bundle
BuildRequires: maven-remote-resources-plugin
BuildRequires: maven-site-plugin

BuildArch:     noarch

%description
The Apache Tika toolkit detects and extracts meta-data and
structured text content from various documents using existing
parser libraries.

%if %{with tika_parsers}
%package parsers
Summary:       Apache Tika parsers

%description parsers
Apache Tika parsers implementation that matches the
type of the document, once it is known, using
Mime Type detection.

%package java7
Summary:       Apache Tika Java-7 Components

%description java7
Java-7 reliant components, including FileTypeDetector
implementations.

%package xmp
Summary:       Apache Tika XMP

%description xmp
Converts Tika metadata to XMP.

%if %{with tika_app}
%package app
Summary:       Apache Tika Application
Requires:      mvn(log4j:log4j:1.2.17)

%description app
Apache Tika standalone application.
%endif
%endif

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
# Cleanup
find . -name '*.jar' -delete
find . -name '*.class' -delete
# Remove unwanted test resources
rm -r %{name}-parsers/src/test/resources/test-documents/testLinux-*-*
rm -r %{name}-parsers/src/test/resources/test-documents/testFreeBSD-*
rm -r %{name}-parsers/src/test/resources/test-documents/testSolaris-*
rm -r %{name}-parsers/src/test/resources/test-documents/*.ibooks
rm -r %{name}-parsers/src/test/resources/test-documents/*.numbers
rm -r %{name}-parsers/src/test/resources/test-documents/*.pages
rm -r %{name}-parsers/src/test/resources/test-documents/*.key
rm -r %{name}-parsers/src/test/resources/test-documents/*.war
rm -r %{name}-parsers/src/test/resources/test-documents/*.wma
rm -r %{name}-parsers/src/test/resources/test-documents/*.wmv
find . -name '*.7z' -delete
find . -name '*.ar' -delete
find . -name '*.cpio' -delete
find . -name '*.ear' -delete
find . -name '*.exe' -delete
find . -name '*.mp*' -delete
find . -name '*.tbz2' -delete
find . -name '*.tgz' -delete
find . -name '*.zip' -delete
%patch0 -p1
%patch1 -p1

%pom_disable_module %{name}-bundle
%pom_disable_module %{name}-server
# Unavailable plugins
%pom_remove_plugin org.codehaus.mojo:clirr-maven-plugin %{name}-core
%pom_remove_plugin org.apache.felix:maven-scr-plugin %{name}-xmp
%pom_remove_plugin org.apache.felix:maven-scr-plugin %{name}-java7

# Require com.drewnoakes:metadata-extractor:2.6.2 and fedora metadata-extractor pkg is too old
# see https://bugzilla.redhat.com/show_bug.cgi?id=947457
%pom_xpath_set "pom:project/pom:dependencies/pom:dependency[pom:artifactId='metadata-extractor']/pom:version" 2  %{name}-parsers
# Disable vorbis-java-tika support, cause circular dependency
%if %{without vorbis_tika}
%pom_remove_dep :vorbis-java-tika %{name}-parsers
%endif

%if %{without tika_parsers}
%pom_disable_module %{name}-parsers
%pom_disable_module %{name}-xmp
%else
%if %{without tika_app}
%pom_disable_module %{name}-app
%else
# No bundled libraries are shipped
%pom_remove_plugin :maven-shade-plugin %{name}-app
%pom_remove_plugin :maven-antrun-plugin %{name}-app
%endif
%endif

# Unavailable build dep com.googlecode.mp4parser:isoparser
# MP4 is non-free remove support for it
%pom_remove_dep com.googlecode.mp4parser:isoparser %{name}-parsers
rm -r %{name}-parsers/src/main/java/org/apache/tika/parser/mp4/MP4Parser.java \
 %{name}-parsers/src/test/java/org/apache/tika/parser/mp4/MP4ParserTest.java

# This test require network
rm %{name}-core/src/test/java/org/apache/tika/mime/MimeDetectionTest.java
# These test fails for unavailable deps: com.googlecode.mp4parser:isoparser and org.gagravarr:vorbis-java-tika
rm -r %{name}-parsers/src/test/java/org/apache/tika/parser/mail/RFC822ParserTest.java \
 %{name}-parsers/src/test/java/org/apache/tika/parser/mbox/MboxParserTest.java
rm -r %{name}-parsers/src/test/java/org/apache/tika/detect/TestContainerAwareDetector.java \
 %{name}-parsers/src/test/java/org/apache/tika/parser/AutoDetectParserTest.java \
 %{name}-parsers/src/test/java/org/apache/tika/parser/asm/ClassParserTest.java \
 %{name}-parsers/src/test/java/org/apache/tika/parser/pkg/Bzip2ParserTest.java \
 %{name}-parsers/src/test/java/org/apache/tika/parser/pkg/GzipParserTest.java \
 %{name}-parsers/src/test/java/org/apache/tika/parser/pkg/TarParserTest.java \
 %{name}-parsers/src/test/java/org/apache/tika/parser/pkg/ZipParserTest.java
rm -r %{name}-parsers/src/test/java/org/apache/tika/parser/image/ImageMetadataExtractorTest.java
# Fails for unavailable test resources
rm -r %{name}-parsers/src/test/java/org/apache/tika/parser/microsoft/ProjectParserTest.java \
 %{name}-parsers/src/test/java/org/apache/tika/parser/mp3/Mp3ParserTest.java \
 %{name}-parsers/src/test/java/org/apache/tika/mime/TestMimeTypes.java \
 %{name}-parsers/src/test/java/org/apache/tika/parser/iwork/IWorkParserTest.java \
 %{name}-parsers/src/test/java/org/apache/tika/parser/pkg/ArParserTest.java \
 %{name}-parsers/src/test/java/org/apache/tika/parser/executable/ExecutableParserTest.java \
 %{name}-parsers/src/test/java/org/apache/tika/parser/ibooks/iBooksParserTest.java \
 %{name}-app/src/test/java/org/apache/tika/cli/TikaCLITest.java

# NullPointerException: null
rm -r %{name}-parsers/src/test/java/org/apache/tika/parser/fork/ForkParserIntegrationTest.java
# NoClassDefFoundError: org/w3c/dom/ElementTraversal
%pom_add_dep xml-apis:xml-apis::test %{name}-parsers

%build
# skip tests for now because there are test failures:
# Tests which use cglib fail because of incompatibility with asm4
# Test fails for unavailable build deps: com.googlecode.mp4parser:isoparser
%mvn_package :%{name} %{name}
%mvn_package :%{name}-core %{name}
%mvn_package :%{name}-parent %{name}
%mvn_build -s -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%if %{with tika_app}
%jpackage_script org.apache.tika.cli.TikaCLI "" "" %{name}:google-gson:commons-io:commons-logging:log4j12-1.2.17:metadata-extractor2-2:juniversalchardet:apache-commons-codec:boilerpipe:thredds/netcdf:thredds/udunits:bea-stax-api:commons-compress:felix/org.apache.felix.scr.annotations:apache-mime4j/core:apache-mime4j/dom:pdfbox:poi/poi:poi/poi-scratchpad:poi/poi-ooxml:bcmail:bcprov:tagsoup:objectweb-asm4/asm-all:rome:fontbox:vorbis-java:dom4j:xmlbeans:poi/poi-ooxml-schemas:jempbox:xmpcore:slf4j/api:slf4j/log4j12:jdom:jdom2 %{name}-app true
%endif

%files -f .mfiles-%{name}
%dir %{_javadir}/%{name}
%doc CHANGES.txt HEADER.txt KEYS LICENSE.txt NOTICE.txt README.txt

%if %{with tika_parsers}
%files parsers -f .mfiles-%{name}-parsers
%doc LICENSE.txt NOTICE.txt

%files java7 -f .mfiles-%{name}-java7
%doc LICENSE.txt NOTICE.txt

%files xmp -f .mfiles-%{name}-xmp
%doc LICENSE.txt NOTICE.txt

%if %{with tika_app}
%files app -f .mfiles-%{name}-app
%doc LICENSE.txt NOTICE.txt
%{_bindir}/%{name}-app
%endif
%endif

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Tue Jul 01 2014 gil cattaneo <puntogil@libero.it> 1.5-1
- update to 1.5

* Wed Jun 11 2014 Fabrice Bellet <fabrice@bellet.info> 1.4-7
- enable app module, RHBZ#1109072

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 07 2014 Michal Srb <msrb@redhat.com> - 1.4-5
- Port to bouncycastle 1.50

* Tue Nov 19 2013 gil cattaneo <puntogil@libero.it> 1.4-4
- enable vorbis-java-tika support

* Wed Oct 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-3
- Rebuild to regenerate broken POMs
- Related: rhbz#1021484

* Mon Oct 21 2013 gil cattaneo <puntogil@libero.it> 1.4-2
- enable parsers and xpm modules

* Thu Aug 29 2013 gil cattaneo <puntogil@libero.it> 1.4-1
- update to 1.4

* Tue Oct 23 2012 gil cattaneo <puntogil@libero.it> 1.2-1
- initial rpm
