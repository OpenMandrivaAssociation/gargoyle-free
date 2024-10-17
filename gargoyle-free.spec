%define name    gargoyle-free
%define originalversion 2009-08-25
%define version 20090825
%define release %mkrel 4

Name:           %{name}
Summary:        Graphical player for Interactive Fiction games
Version:        %{version}
Release:        %{release}
URL:            https://ccxvii.net/gargoyle/ 
# This is not the original source zip because the original contains non-free code
# see README.mandriva for more explanations
# Original download URL : http://garglk.googlecode.com/files/gargoyle-%{original-version}-sources.zip
Source0:        gargoyle-free-%{originalversion}.tgz
Source1:	README.mandriva
Patch0:		dfsg_disable_alan.patch
Patch1:		dfsg_disable_hugo.patch
Patch2:		dfsg_replace_luximono_font.patch
Patch3:		mandrivaify-wrapper-script.patch
Patch4:		ignore_bundled_libraries.patch
Patch5:		sdl_sound_debian.patch
License:        GPLv2 and others
Group:          Games/Other
BuildRequires:  ftjam SDL-devel SDL_sound-devel SDL_mixer-devel gtk2-devel jpeg-devel freetype-devel png-devel fontconfig-devel
BuildRoot:      %{_tmppath}/%{name}-buildroot

%description
Gargoyle is an Interactive Fiction (text adventure) player that supports all 
the major interactive fiction formats.

Most interactive fiction is distributed as portable game files. These portable 
game files come in many formats. In the past, you used to have to download a 
separate player (interpreter) for each format of IF you wanted to play. 
Instead, Gargoyle provides an unified player.

Gargoyle is based on the standard interpreters for the formats it supports: 
Adrift, AdvSys, AGiliTy, Quest, JACL, Level 9, Magnetic, TADS2, TADS3, Z-code
and Glulxe.

Gargoyle also features graphics, sounds and Unicode support.

You can find hundreds of games at :
- the IF database : http://ifdb.tads.org
- the IF archive : http://ifarchive.org

Limitations:
* This free version of gargoyle does not include the non-free Alan and Hugo 
interpreter (and uses a different, free monospace font).
* The TADS interpreter doesn't support HTML TADS; you can play the games, but 
will miss the hyperlinks. 

%prep
%setup -q -n %{name}-%{originalversion}
%patch0 -p1 -b .orig
%patch1 -p1 -b .orig
%patch2 -p1 -b .orig
%patch3 -p0 -b .orig
%patch4 -p1 -b .orig
%patch5 -p1 -b .orig

%build
cp %SOURCE1 .
jam
sed -i garglk/launcher.sh -e 's#___LIBDIR___#'%{_libdir}'#' 
jam install #installs in BUILD/%{name}-%{originalversion}/build/dist

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
install -d %{buildroot}%{_gamesbindir}
install -m 755 build/dist/gargoyle %{buildroot}%{_gamesbindir}/%{name}
rm -f build/dist/gargoyle
install -d %{buildroot}%{_libdir}
install -m 755 build/dist/libgarglk.so %{buildroot}%{_libdir}/
rm -f build/dist/libgarglk.so
install -d %{buildroot}%{_libdir}/gargoyle
install -m 755 build/dist/* %{buildroot}%{_libdir}/gargoyle

%clean
jam clean
rm -rf build/
rm -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%doc README.mandriva License.txt
%{_gamesbindir}/%{name}
%dir %{_libdir}/gargoyle
%{_libdir}/lib*
%{_libdir}/gargoyle/*
