#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>.

"""
Default projects to build
"""

import os
import glob
import shutil

from .utils.simple_ui import print_debug
from .utils.simple_ui import print_message
from .utils.utils import convert_to_msys
from .utils.utils import file_replace
from .utils.utils import python_find_libs_dir
from .utils.base_expanders import Tarball, GitRepo
from .utils.base_expanders import NullExpander
from .utils.base_project import Project, project_add
from .utils.base_project import GVSBUILD_IGNORE
from .utils.base_builders import Meson, MercurialCmakeProject, CmakeProject

@project_add
class Project_adwaita_icon_theme(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'adwaita-icon-theme',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/adwaita-icon-theme/3.24/adwaita-icon-theme-3.24.0.tar.xz',
            hash = 'ccf79ff3bd340254737ce4d28b87f0ccee4b3358cd3cd5cd11dc7b42f41b272a',
            dependencies = ['librsvg'],
            )

    def build(self):
        self.push_location(r'.\win32')
        self.exec_vs(r'nmake /nologo /f adwaita-msvc.mak CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PREFIX="%(gtk_dir)s"', add_path=os.path.join(self.builder.opts.msys_dir, 'usr', 'bin'))
        self.exec_vs(r'nmake /nologo /f adwaita-msvc.mak install CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PREFIX="%(gtk_dir)s"', add_path=os.path.join(self.builder.opts.msys_dir, 'usr', 'bin'))
        self.pop_location()

        self.install(r'.\COPYING_CCBYSA3 share\doc\adwaita-icon-theme')

@project_add
class Project_atk(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'atk',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/atk/2.26/atk-2.26.1.tar.xz',
            hash = 'ef00ff6b83851dddc8db38b4d9faeffb99572ba150b0664ee02e46f015ea97cb',
            dependencies = ['ninja', 'meson', 'pkg-config', 'perl', 'glib'],
            )

    def build(self):
        Meson.build(self, meson_params='-Ddisable_introspection=true -Denable_docs=false', make_tests=True)
        self.install(r'.\COPYING share\doc\atk')

@project_add
class Project_cairo(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'cairo',
            archive_url = 'http://cairographics.org/snapshots/cairo-1.15.2.tar.xz',
            hash = '268cc265a7f807403582f440643064bf52896556766890c8df7bad02d230f6c9',
            dependencies = ['fontconfig', 'glib', 'pixman', 'libpng'],
            patches = ['cairo.patch']
            )

    def build(self):
        self.exec_vs(r'make -f Makefile.win32 CFG=%(configuration)s ARCH=%(platform)s', add_path=os.path.join(self.builder.opts.msys_dir, 'usr', 'bin'))
        self.push_location(r'.\util\cairo-gobject')
        self.exec_vs(r'make -f Makefile.win32 CFG=%(configuration)s ARCH=%(platform)s', add_path=os.path.join(self.builder.opts.msys_dir, 'usr', 'bin'))
        self.pop_location()

        self.install(r'.\src\%(configuration)s\cairo.dll bin')
        self.install(r'.\util\cairo-gobject\%(configuration)s\cairo-gobject.dll bin')

        self.install(r'.\src\%(configuration)s\cairo.lib lib')
        self.install(r'.\util\cairo-gobject\%(configuration)s\cairo-gobject.lib lib')

        self.install(r'.\src\cairo.h include\cairo')
        self.install(r'.\src\cairo-deprecated.h include\cairo')
        self.install(r'.\src\cairo-pdf.h include\cairo')
        self.install(r'.\src\cairo-ps.h include\cairo')
        self.install(r'.\src\cairo-script.h include\cairo')
        self.install(r'.\src\cairo-svg.h include\cairo')
        self.install(r'.\src\cairo-tee.h include\cairo')
        self.install(r'.\src\cairo-win32.h include\cairo')
        self.install(r'.\src\cairo-xml.h include\cairo')
        self.install(r'.\src\cairo-ft.h include\cairo')
        self.install(r'.\src\cairo-features.h include\cairo')
        self.install(r'.\util\cairo-gobject\cairo-gobject.h include\cairo')
        self.install(r'.\cairo-version.h include\cairo')

        self.install(r'.\pc-files\* lib\pkgconfig')

        self.install(r'.\COPYING share\doc\cairo')

@project_add
class Project_clutter(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'clutter',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/clutter/1.26/clutter-1.26.2.tar.xz',
            hash = 'e7233314983055e9018f94f56882e29e7fc34d8d35de030789fdcd9b2d0e2e56',
            dependencies = ['atk','cogl','json-glib'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\clutter.sln')

        self.install(r'.\COPYING share\doc\clutter')

@project_add
class Project_cogl(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'cogl',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/cogl/1.22/cogl-1.22.2.tar.xz',
            hash = '39a718cdb64ea45225a7e94f88dddec1869ab37a21b339ad058a9d898782c00d',
            dependencies = ['python', 'glib','cairo','pango','gdk-pixbuf'],
            patches = ['001-cogl-missing-symbols.patch',
                       '002-cogl-pango-missing-symbols.patch'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\cogl.sln')

        self.install(r'.\COPYING share\doc\cogl')

@project_add
class Project_cyrus_sasl(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'cyrus-sasl',
            hash = '9e8035c12d419209ea60584d5efa51d042c3ed44b450b9d173d5504b222df9f1',
            archive_url = 'https://github.com/wingtk/cyrus-sasl/releases/download/cyrus-sasl-lmdb-2.1.28/cyrus-sasl-2.1.28.tar.xz',
            dependencies = ['lmdb', 'openssl'],
            )

    def build(self):
        configuration = 'Debug' if self.builder.opts.configuration == 'debug' else 'Release'
        self.exec_vs(r'nmake /nologo /f NTMakefile SASLDB="LMDB" LMDB_INCLUDE="%(gtk_dir)s\include" LMDB_LIBPATH="%(gtk_dir)s\lib" ' +
                     r'OPENSSL_INCLUDE="%(gtk_dir)s\include" OPENSSL_LIBPATH="%(gtk_dir)s\lib" prefix="%(pkg_dir)s" CFG=' + configuration)
        self.exec_vs(r'nmake /nologo /f NTMakefile install SASLDB="LMDB" LMDB_INCLUDE="%(gtk_dir)s\include" ' +
                     r'LMDB_LIBPATH="%(gtk_dir)s\lib" OPENSSL_INCLUDE="%(gtk_dir)s\include" OPENSSL_LIBPATH="%(gtk_dir)s\lib" prefix="%(pkg_dir)s" CFG=' + configuration)

        self.install(r'.\COPYING share\doc\cyrus-sasl')

@project_add
class Project_emeus(GitRepo, Meson):
    def __init__(self):
        Meson.__init__(self,
            'emeus',
            repo_url = 'https://github.com/ebassi/emeus.git',
            fetch_submodules = False,
            tag = None,
            dependencies = ['ninja', 'meson', 'pkg-config', 'gtk3'],
            patches = [
                '00_win_no_script.patch'
                ],
            )

    def build(self):
        Meson.build(self, meson_params='-Ddocs=false -Dintrospection=false', make_tests=True)
        self.install(r'.\COPYING.txt share\doc\emeus')

@project_add
class Project_enchant(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'enchant',
            archive_url = 'https://dl.hexchat.net/gtk-win32/src/enchant-1.6.1.tar.xz',
            hash = 'd6cddd2621589ca8becaba1bfe8d3668f7d6592743664ef0e1a35543971fbe6e',
            dependencies = ['glib'],
            )

    def build(self):
        x64_param = ''
        if self.builder.x64:
            x64_param = 'X64=1'

        self.push_location(r'.\src')

        #Exec nmake /nologo -f makefile.mak clean
        self.exec_vs(r'nmake /nologo -f makefile.mak DLL=1 ' + x64_param + ' MFLAGS=-MD GLIBDIR=%(gtk_dir)s\include\glib-2.0')

        self.pop_location()

        self.install(r'.\bin\release\enchant.exe ' \
                     r'.\bin\release\pdb\enchant.pdb ' \
                     r'.\bin\release\enchant-lsmod.exe ' \
                     r'.\bin\release\pdb\enchant-lsmod.pdb ' \
                     r'.\bin\release\test-enchant.exe ' \
                     r'.\bin\release\pdb\test-enchant.pdb ' \
                     r'.\bin\release\libenchant.dll ' \
                     r'.\bin\release\pdb\libenchant.pdb '\
                     r'bin')

        self.install(r'.\fonts.conf ' \
                     r'.\fonts.dtd ' \
                     r'etc\fonts')

        self.install(r'.\src\enchant.h ' \
                     r'.\src\enchant++.h ' \
                     r'.\src\enchant-provider.h ' \
                     r'include\enchant')

        self.install(r'.\bin\release\libenchant.lib lib')

        self.install(r'.\bin\release\libenchant_ispell.dll ' \
                     r'.\bin\release\libenchant_ispell.lib ' \
                     r'.\bin\release\pdb\libenchant_ispell.pdb ' \
                     r'.\bin\release\libenchant_myspell.dll ' \
                     r'.\bin\release\libenchant_myspell.lib ' \
                     r'.\bin\release\pdb\libenchant_myspell.pdb ' \
                     r'lib\enchant')

        self.install(r'.\COPYING.LIB share\doc\enchant')

@project_add
class Project_ffmpeg(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'ffmpeg',
            archive_url = 'http://ffmpeg.org/releases/ffmpeg-3.3.tar.xz',
            hash = '599e7f7c017221c22011c4037b88bdcd1c47cd40c1e466838bc3c465f3e9569d',
            dependencies = [ 'yasm', 'x264' ],
            patches = [ '0001-lavc-mpegvideo_enc-allow-low_delay-for-non-MPEG2-cod.patch' ]
        )

    def build(self):
        self.exec_vs(r'bash build\build.sh %s %s %s' % (self.pkg_dir, self.builder.gtk_dir, self.builder.opts.configuration),
                     add_path=os.path.join(self.builder.opts.msys_dir, 'usr', 'bin'))

        self.install(r'.\COPYING.LGPLv2.1 ' \
                     r'.\COPYING.LGPLv3 ' \
                     r'.\COPYING.GPLv2 ' \
                     r'share\doc\ffmpeg')

    def post_install(self):
        self.builder.exec_msys(['mv', 'avcodec.lib', '../lib/'], working_dir=os.path.join(self.builder.gtk_dir, 'bin'))
        self.builder.exec_msys(['mv', 'avutil.lib', '../lib/'], working_dir=os.path.join(self.builder.gtk_dir, 'bin'))
        self.builder.exec_msys(['mv', 'postproc.lib', '../lib/'], working_dir=os.path.join(self.builder.gtk_dir, 'bin'))
        self.builder.exec_msys(['mv', 'swscale.lib', '../lib/'], working_dir=os.path.join(self.builder.gtk_dir, 'bin'))

@project_add
class Project_fontconfig(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'fontconfig',
            archive_url = 'https://www.freedesktop.org/software/fontconfig/release/fontconfig-2.12.6.tar.gz',
            hash = '064b9ebf060c9e77011733ac9dc0e2ce92870b574cca2405e11f5353a683c334',
            dependencies = ['freetype', 'libxml2'],
            patches = ['fontconfig.patch'],
            )

    def build(self):
        #make the fontconfig files work on other compatible vs versions
        for proj in glob.glob(r'%s\*.vcxproj' % (self.build_dir,)):
            with open(proj, 'r') as f:
                content = f.read()
            if content.find('<PlatformToolset>FIXME</PlatformToolset>') >= 0:
                print_debug('patching project file %s' % (proj,))
                content = content.replace('<PlatformToolset>FIXME</PlatformToolset>', '<PlatformToolset>v%s0</PlatformToolset>' % (self.builder.opts.vs_ver))
                with open(proj, 'w') as f:
                    f.write(content)

        self.exec_msbuild('fontconfig.sln /t:build')

        if self.builder.x86:
            rel_dir = r'.\%(configuration)s'
        else:
            rel_dir = r'.\x64\%(configuration)s'

        self.push_location(rel_dir)
        self.install('fontconfig.dll', 'fontconfig.pdb', 'fc-cache.exe', 'fc-cache.pdb', 'fc-cat.exe', 'fc-cat.pdb', 'fc-list.exe', 'fc-list.pdb',
                     'fc-match.exe', 'fc-match.pdb', 'fc-query.exe', 'fc-query.pdb', 'fc-scan.exe', 'fc-scan.pdb', 'bin')
        self.pop_location()

        self.install(r'fonts.conf fonts.dtd etc\fonts')
        self.install(r'.\fontconfig\fcfreetype.h .\fontconfig\fcprivate.h .\fontconfig\fontconfig.h include\fontconfig')

        self.push_location(rel_dir)
        self.install('fontconfig.lib', 'lib')
        self.pop_location()

        self.install(r'.\COPYING share\doc\fontconfig')

@project_add
class Project_freetype(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'freetype',
            archive_url = 'http://download.savannah.gnu.org/releases/freetype/freetype-2.8.1.tar.gz',
            hash = '876711d064a6a1bd74beb18dd37f219af26100f72daaebd2d86cb493d7cd7ec6',
            )

    def build(self):
        self.exec_msbuild(r'builds\windows\vc%(vs_ver)s\freetype.vcxproj')
        self.install_dir(r'.\include')
        self.install(r'.\objs\%(platform)s\freetype.lib lib')
        self.install(r'.\pc-files\* lib\pkgconfig')
        self.install(r'.\docs\LICENSE.TXT share\doc\freetype')

@project_add
class Project_gdk_pixbuf(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'gdk-pixbuf',
            archive_url = 'https://git.gnome.org/browse/gdk-pixbuf/snapshot/gdk-pixbuf-f38e3e2cededb3ed9d8887072a4e685d3057847e.tar.xz',
            hash = '548d650085806379fae62e181696d4e9c29507d131ea62b75612e628c26e54ad',
            dependencies = ['ninja', 'pkg-config', 'meson', 'perl', 'libtiff-4', 'jasper', 'glib', 'libpng'],
            )

    def build(self):
        # We can experiment with a couple of options to give to meson:
        #    -Dbuiltin_loaders=all|windows
        #        Buld the loader inside the library
        Meson.build(self, meson_params='-Djasper=true -Dnative_windows_loaders=true -Dgir=false -Dman=false')
        self.install(r'.\COPYING share\doc\gdk-pixbuf')

@project_add
class Project_gettext(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'gettext',
            archive_url = 'http://ftp.gnu.org/pub/gnu/gettext/gettext-0.19.7.tar.gz',
            hash = '5386d2a40500295783c6a52121adcf42a25519e2d23675950619c9e69558c23f',
            dependencies = ['win-iconv'],
            patches = ['0001-gettext-runtime-Add-pre-configured-headers-for-MSVC-.patch',
                       '0001-gettext-tools-Add-pre-configured-headers-and-sources.patch',
                       '0001-gettext-tools-gnulib-lib-libxml-Check-for-_WIN32-as-.patch',
                       '0001-gettext-tools-Make-private-headers-C-friendly.patch',
                       '0001-gettext-tools-src-x-lua.c-Fix-C99ism.patch',
                       '0002-gettext-tools-gnulib-lib-Declare-items-at-top-of-blo.patch',
                       '0004-gettext-runtime-intl-plural-exp.h-Match-up-declarati.patch',
                       '0005-gettext-runtime-intl-printf-parse.c-Fix-build-on-Vis.patch'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\gettext.sln')

        self.install(r'.\gettext-tools\its\*.its share\gettext\its')
        self.install(r'.\gettext-tools\its\*.loc share\gettext\its')
        self.install(r'.\COPYING share\doc\gettext')

@project_add
class Project_glib(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'glib',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/glib/2.54/glib-2.54.2.tar.xz',
            hash = 'bb89e5c5aad33169a8c7f28b45671c7899c12f74caf707737f784d7102758e6c',
            dependencies = ['gettext', 'libffi', 'zlib'],
            patches = ['glib-if_nametoindex.patch',
                       'glib-package-installation-directory.patch'],
            )

    def build(self):
        configuration = 'Release_BundledPCRE'
        if self.builder.opts.configuration == 'debug':
            configuration = 'Debug_BundledPCRE'

        self.exec_msbuild(r'win32\vs%(vs_ver)s\glib.sln', configuration=configuration)
        self.install(r'.\COPYING share\doc\glib')

@project_add
class Project_glib_networking(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'glib-networking',
            archive_url = 'https://github.com/wingtk/glib-networking/releases/download/2.50.0-openssl/glib-networking-2.50.0.tar.xz',
            hash = 'ca116a5b9435001d0dd8cfab3743f9a5d0003dbdc99a407c66858b183f07192b',
            dependencies = ['gsettings-desktop-schemas', 'openssl'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\glib-networking.sln')
        self.install(r'.\COPYING share\doc\glib-networking')

@project_add
class Project_glib_py_wrapper(NullExpander, Meson):
    def __init__(self):
        Project.__init__(self,
            'glib-py-wrapper',
            dependencies = ['glib'],
            )

    def build(self):
        Meson.build(self)

@project_add
class Project_glib_openssl(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'glib-openssl',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/glib-openssl/2.50/glib-openssl-2.50.6.tar.xz',
            hash = '1703a1da93911cf7f386e5fd9f82b803a150448e257db749166c0c3a1b5d3880',
            dependencies = ['pkg-config', 'ninja', 'meson', 'glib', 'openssl'],
            )

    def build(self):
        Meson.build(self)
        self.install(r'.\COPYING share\doc\glib-openssl')
        self.install(r'.\LICENSE_EXCEPTION share\doc\glib-openssl')

@project_add
class Project_gobject_introspection(GitRepo, Meson):
    def __init__(self):
        Project.__init__(self,
            'gobject-introspection',
            repo_url = 'https://git.gnome.org/browse/gobject-introspection',
            fetch_submodules = False,
            tag = 'wip/meson',
            dependencies = [
                'ninja',
                'meson',
                'msys2',
                'pkg-config',
                'glib',
                # This ones are for add their's gir
                'atk',
                'gdk-pixbuf',
                'pango',
                'gtk',
                'gtk3',
                ],
            patches = [
                '00_glib_win_ver.patch',
                ],
            )

    def make_single_gir(self, prj_name, prj_dir=None, add_meson=False):
        if not prj_dir:
            prj_dir = prj_name

        b_dir = r'%s\%s\build\win32' % (self.builder.working_dir, prj_dir, )
        if not os.path.isfile(os.path.join(b_dir, 'detectenv-msvc.mak')):
            b_dir = r'%s\%s\win32' % (self.builder.working_dir, prj_dir, )
            if not os.path.isfile(os.path.join(b_dir, 'detectenv-msvc.mak')):
                print_message('Unable to find detectenv-msvc.mak for %s' % (prj_name, ))
                return

        old_inc = None
        if add_meson:
            # include 
            add_inc = r'%s\%s-meson' % (self.builder.working_dir, prj_dir, )
            old_inc = self.builder.mod_env('INCLUDE', add_inc, prepend=False)
            print("Include add: %s" % (add_inc, ))

        cmd = 'nmake -f %s-introspection-msvc.mak CFG=%s PREFIX=%s PYTHON=%s\python.exe install-introspection' % (
                prj_name,
                self.builder.opts.configuration,
                self.builder.gtk_dir,
                self.builder.opts.python_dir,
                )

        self.push_location(b_dir)
        self.exec_vs(cmd)
        self.pop_location()
        self.builder.restore_env(old_inc)

    def build(self):
        # For finding gobject-introspection.pc
        self.builder.mod_env('PKG_CONFIG_PATH', '.')
        # For finding & using girepository.lib/.dll
        self.builder.mod_env('LIB', r'.\girepository')
        self.builder.mod_env('PATH', r'.\girepository')
        # For linking the _giscanner.pyd extension module when using a virtualenv
        py_libs = python_find_libs_dir(Project.get_tool_path('python'))
        if py_libs:
            print_debug("Python library path is [%s]" % (py_libs, ))
            self.builder.mod_env('LIB', py_libs, prepend=False)

        Meson.build(self)

        # Build extra gir/typelib
        self.make_single_gir('atk')
        self.make_single_gir('gdk-pixbuf', add_meson=True)
        self.make_single_gir('pango')
        self.make_single_gir('gtk', prj_dir='gtk')
        self.make_single_gir('gtk', prj_dir='gtk3')

@project_add
class Project_graphene(GitRepo, Meson):
    def __init__(self):
        Meson.__init__(self,
            'graphene',
            repo_url = 'https://github.com/ebassi/graphene',
            fetch_submodules = False,
            tag = None,
            dependencies = ['ninja', 'meson', 'pkg-config', 'glib'],
            )

    def build(self):
        Meson.build(self)
        self.install(r'.\LICENSE share\doc\graphene')

@project_add
class Project_grpc(GitRepo, Project):
    def __init__(self):
        Project.__init__(self,
            'grpc',
            repo_url = 'https://github.com/grpc/grpc.git',
            fetch_submodules = True,
            tag = 'v1.0.0',
            dependencies = ['nuget', 'protobuf'],
            patches = ['0001-Remove-RuntimeLibrary-setting-from-the-projects.patch'],
            )

    def build(self):
        self.exec_cmd(self.builder.nuget + ' restore ' + os.path.join(self.build_dir, 'vsprojects', 'grpc.sln'))
        self.exec_msbuild(r'vsprojects\grpc.sln /t:grpc++')
        self.exec_msbuild(r'vsprojects\grpc_protoc_plugins.sln')

        self.install(r'.\include\grpc include\google')
        self.install(r'.\include\grpc++ include\google')

        platform = ''
        if self.builder.x64:
            platform = 'x64\\'

        bin_dir = r'.\vsprojects\%s%s' % (platform, self.builder.opts.configuration, )

        self.install(bin_dir + r'\gpr.lib lib')
        self.install(bin_dir + r'\grpc.lib lib')
        self.install(bin_dir + r'\grpc++.lib lib')

        self.install(bin_dir + r'\grpc_cpp_plugin.exe bin')
        self.install(bin_dir + r'\grpc_cpp_plugin.pdb bin')

        self.install(bin_dir + r'\grpc_csharp_plugin.exe bin')
        self.install(bin_dir + r'\grpc_csharp_plugin.pdb bin')

        self.install(bin_dir + r'\grpc_node_plugin.exe bin')
        self.install(bin_dir + r'\grpc_node_plugin.pdb bin')

        self.install(bin_dir + r'\grpc_objective_c_plugin.exe bin')
        self.install(bin_dir + r'\grpc_objective_c_plugin.pdb bin')

        self.install(bin_dir + r'\grpc_python_plugin.exe bin')
        self.install(bin_dir + r'\grpc_python_plugin.pdb bin')

        self.install(bin_dir + r'\grpc_ruby_plugin.exe bin')
        self.install(bin_dir + r'\grpc_ruby_plugin.pdb bin')

        self.install(r'.\LICENSE share\doc\grpc')

@project_add
class Project_gsettings_desktop_schemas(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'gsettings-desktop-schemas',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gsettings-desktop-schemas/3.24/gsettings-desktop-schemas-3.24.0.tar.xz',
            hash = 'f6573a3f661d22ff8a001cc2421d8647717f1c0e697e342d03c6102f29bbbb90',
            dependencies = ['perl', 'glib'],
            patches = ['0001-build-win32-replace.py-Fix-replacing-items-in-files-.patch'],
            )

    def build(self):
        self.push_location(r'.\build\win32')
        self.exec_vs(r'nmake /nologo /f gsettings-desktop-schemas-msvc.mak CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PERL="%(perl_dir)s\bin\perl.exe" PREFIX="%(gtk_dir)s"')
        self.exec_vs(r'nmake /nologo /f gsettings-desktop-schemas-msvc.mak install CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PREFIX="%(gtk_dir)s"')
        self.pop_location()

        self.install(r'.\COPYING share\doc\gsettings-desktop-schemas')

class Project_gtk_base(Tarball, Project):
    def __init__(self, name, **kwargs):
        Project.__init__(self, name, **kwargs)

    def build(self):
        mo = 'gtk20.mo' if self.name == 'gtk' else 'gtk30.mo'

        localedir = os.path.join(self.pkg_dir, 'share', 'locale')
        self.push_location(r'.\po')
        for fp in glob.glob(os.path.join(self.build_dir, 'po', '*.po')):
            f = os.path.basename(fp)
            lcmsgdir = os.path.join(localedir, f[:-3], 'LC_MESSAGES')
            self.builder.make_dir(lcmsgdir)
            cmd = ' '.join(['msgfmt', '-co', os.path.join(lcmsgdir, mo), f])
            self.builder.exec_cmd(cmd, working_dir=self._get_working_dir())
        self.pop_location()

        self.install(r'.\COPYING share\doc\%s' % self.name)

@project_add
class Project_gtk(Project_gtk_base):
    def __init__(self):
        Project_gtk_base.__init__(self,
            'gtk',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gtk+/2.24/gtk+-2.24.31.tar.xz',
            hash = '68c1922732c7efc08df4656a5366dcc3afdc8791513400dac276009b40954658',
            dependencies = ['atk', 'gdk-pixbuf', 'pango'],
            patches = ['gtk-revert-scrolldc-commit.patch', 'gtk-bgimg.patch', 'gtk-accel.patch', 'gtk-multimonitor.patch'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\gtk+.sln')

        super(Project_gtk, self).build()

@project_add
class Project_gtk3(Project_gtk_base):
    def __init__(self):
        Project_gtk_base.__init__(self,
            'gtk3',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gtk+/3.22/gtk+-3.22.26.tar.xz',
            hash = '61eef0d320e541976e2dfe445729f12b5ade53050ee9de6184235cb60cd4b967',
            dependencies = ['atk', 'gdk-pixbuf', 'pango', 'libepoxy'],
            patches = ['gtk3-clip-retry-if-opened-by-others.patch'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\gtk+.sln /p:GtkPostInstall=rem')

        super(Project_gtk3, self).build()

    def post_install(self):
        self.exec_cmd(r'%(gtk_dir)s\bin\glib-compile-schemas.exe %(gtk_dir)s\share\glib-2.0\schemas')
        self.exec_cmd(r'%(gtk_dir)s\bin\gtk-update-icon-cache.exe --ignore-theme-index --force "%(gtk_dir)s\share\icons\hicolor"')

@project_add
class Project_gtksourceview3(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'gtksourceview3',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gtksourceview/3.22/gtksourceview-3.22.2.tar.xz',
            hash = '6ce84231dd0931cc747708434ca2f344c65a092dd6e1a800283fe0748773af5e',
            dependencies = ['perl', 'gtk3'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\gtksourceview.sln')

        self.install(r'.\COPYING share\doc\gtksourceview3')

@project_add
class Project_harfbuzz(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'harfbuzz',
            archive_url = 'https://www.freedesktop.org/software/harfbuzz/release/harfbuzz-1.7.2.tar.bz2',
            hash = 'a790585e35c1a87f0dcc23580c84b7cc2324e6f67a2946178d278c2a36c790cb',
            dependencies = ['perl', 'freetype', 'pkg-config', 'glib'],
            )

    def build(self):
        CmakeProject.build(self, cmake_params='-DHB_HAVE_FREETYPE=ON -DHB_HAVE_GLIB=ON -DHB_HAVE_GOBJECT=ON', use_ninja=True)

        self.install(r'.\COPYING share\doc\harfbuzz')

@project_add
class Project_hicolor_icon_theme(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'hicolor-icon-theme',
            archive_url = 'http://icon-theme.freedesktop.org/releases/hicolor-icon-theme-0.15.tar.xz',
            hash = '9cc45ac3318c31212ea2d8cb99e64020732393ee7630fa6c1810af5f987033cc',
            )

    def build(self):
        self.install(r'.\index.theme share\icons\hicolor')

@project_add
class Project_jasper(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'jasper',
            archive_url = 'http://www.ece.uvic.ca/~frodo/jasper/software/jasper-2.0.14.tar.gz',
            hash = '2a1f61e55afe8b4ce8115e1508c5d7cb314d56dfcc2dd323f90c072f88ccf57b',
            dependencies = ['cmake', 'ninja', 'libjpeg-turbo', ],
            patches = [
                    '001-dont-use-pkg-full-path.patch',
                    '002-dont-install-msvc-runtime.patch',
                ]
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True)

        self.install(r'.\COPYRIGHT share\doc\jasper')
        self.install(r'.\LICENSE share\doc\jasper')

@project_add
class Project_jsonc(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'json-c',
            archive_url = 'https://github.com/json-c/json-c/archive/json-c-0.12.1-20160607.tar.gz',
            hash = '989e09b99ded277a0a651cd18b81fcb76885fea08769d7a21b6da39fb8a34816',
            patches = ['json-c-0.12.1-20160607.patch'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\json-c.sln')

        self.install(r'.\COPYING share\doc\json-c')

@project_add
class Project_json_glib(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'json-glib',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/json-glib/1.4/json-glib-1.4.2.tar.xz',
            hash = '2d7709a44749c7318599a6829322e081915bdc73f5be5045882ed120bb686dc8',
            dependencies = ['meson', 'ninja', 'pkg-config', 'perl', 'glib'],
            )

    def build(self):
        Meson.build(self, meson_params='-Ddocs=false -Dintrospection=false', make_tests=True)

        self.install(r'.\COPYING share\doc\json-glib')

@project_add
class Project_leveldb(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'leveldb',
            archive_url = 'https://github.com/google/leveldb/archive/v1.20.tar.gz',
            hash = 'f5abe8b5b209c2f36560b75f32ce61412f39a2922f7045ae764a2c23335b6664',
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\leveldb.sln')

        self.install(r'.\LICENSE share\doc\leveldb')

@project_add
class Project_libarchive(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'libarchive',
            archive_url = 'https://libarchive.org/downloads/libarchive-3.3.1.tar.gz',
            hash = '29ca5bd1624ca5a007aa57e16080262ab4379dbf8797f5c52f7ea74a3b0424e7',
            dependencies = ['cmake', 'ninja', 'win-iconv', 'zlib', 'lz4', 'openssl', 'libxml2'],
            patches = ['0001-Do-not-try-to-compile-with-warnings-as-errors-on-deb.patch'],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True)
        # Fix the pkg-config .pc file, correcting the library's names
        file_replace(os.path.join(self.pkg_dir, 'lib', 'pkgconfig', 'libarchive.pc'),
                     [ (' -llz4',   ' -lliblz4'),
                       (' -leay32', ' -llibeay32'),
                       (' -lxml2',  ' -llibxml2'),
                       ]
                     )
        self.install(r'.\COPYING share\doc\libarchive')

@project_add
class Project_libcroco(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libcroco',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/libcroco/0.6/libcroco-0.6.11.tar.xz',
            hash = '132b528a948586b0dfa05d7e9e059901bca5a3be675b6071a90a90b81ae5a056',
            dependencies = ['glib', 'libxml2'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\libcroco.sln')
        self.install(r'.\COPYING share\doc\libcroco')

@project_add
class Project_libepoxy(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'libepoxy',
            archive_url = 'https://github.com/anholt/libepoxy/releases/download/1.4.3/libepoxy-1.4.3.tar.xz',
            hash = '0b808a06c9685a62fca34b680abb8bc7fb2fda074478e329b063c1f872b826f6',
            dependencies = ['python', 'ninja', 'meson'],
            )

    def build(self):
        Meson.build(self)

        self.install(r'COPYING share\doc\libepoxy')

@project_add
class Project_libffi(GitRepo, Meson):
    def __init__(self):
        Project.__init__(self,
            'libffi',
            repo_url = 'https://github.com/centricular/libffi.git',
            fetch_submodules = False,
            tag = None,
            dependencies = ['python', 'ninja', 'meson'],
            )

    def build(self):
        Meson.build(self)
        self.install(r'LICENSE share\doc\libffi')

@project_add
class Project_libgxps(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libgxps',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/libgxps/0.3/libgxps-0.3.0.tar.xz',
            hash = '412b1343bd31fee41f7204c47514d34c563ae34dafa4cc710897366bd6cd0fae',
            dependencies = ['meson', 'ninja', 'pkg-config', 'glib', 'libarchive', 'cairo', 'libpng', 'libjpeg-turbo', 'libtiff-4', 'gtk3', ],
            patches = [
                '001-ignore-m-lib.patch',
                ],
            )

    def build(self):
        Meson.build(self, meson_params='-Dwith-liblcms2=false -Denable-test=false')

        self.install(r'.\COPYING share\doc\libgxps')

@project_add
class Project_libjpeg_turbo(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'libjpeg-turbo',
            archive_url = 'https://sourceforge.net/projects/libjpeg-turbo/files/1.5.2/libjpeg-turbo-1.5.2.tar.gz',
            hash = '9098943b270388727ae61de82adec73cf9f0dbb240b3bc8b172595ebf405b528',
            dependencies = ['cmake', 'ninja', 'nasm', ],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True)

        self.install(r'.\pc-files\* lib\pkgconfig')
        self.install(r'.\LICENSE.md share\doc\libjpeg-turbo')

@project_add
class Project_libmicrohttpd(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libmicrohttpd',
             archive_url = 'http://ftp.gnu.org/gnu/libmicrohttpd/libmicrohttpd-0.9.54.tar.gz',
             hash = 'bcc721895d4a114b0548a39d2241c35caacb9e2e072d40e11b55c60e3d5ddcbe',
             patches = ['001-remove-postsample.patch'],
            )

    def build(self):
        configuration = 'release-dll'
        if self.builder.opts.configuration == 'debug':
            configuration = 'debug-dll'

        version = '13'
        if self.builder.opts.vs_ver == '14':
            version = '15'

        self.exec_msbuild(r'w32\VS20' + version + '\libmicrohttpd.sln', configuration=configuration)

        debug_option = ''
        if self.builder.opts.configuration == 'debug':
            debug_option = r'_d'

        if self.builder.x86:
            rel_dir = r'.\w32\VS20' + version + r'\Output'
        else:
            rel_dir = r'.\w32\VS20' + version + r'\Output\x64'

        self.push_location(rel_dir)
        self.install(r'microhttpd.h include')
        self.install(r'libmicrohttpd-dll' + debug_option + '.lib' + ' lib')
        self.install(r'libmicrohttpd-dll' + debug_option + '.dll' + ' bin')
        self.install(r'libmicrohttpd-dll' + debug_option + '.pdb' + ' bin')
        self.install(r'hellobrowser-dll' + debug_option + '.exe' + ' bin')
        self.pop_location()



        self.install(r'.\COPYING share\doc\libmicrohttpd')

@project_add
class Project_libpng(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'libpng',
            archive_url = 'http://prdownloads.sourceforge.net/libpng/libpng-1.6.34.tar.xz',
            hash = '2f1e960d92ce3b3abd03d06dfec9637dfbd22febf107a536b44f7a47c60659f6',
            dependencies = ['cmake', 'ninja', 'zlib'],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True)

        self.install(r'.\pc-files\* lib\pkgconfig')
        self.install('LICENSE share\doc\libpng')

@project_add
class Project_librsvg(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'librsvg',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/librsvg/2.40/librsvg-2.40.16.tar.xz',
            hash = 'd48bcf6b03fa98f07df10332fb49d8c010786ddca6ab34cbba217684f533ff2e',
            dependencies = ['libcroco', 'cairo', 'pango', 'gdk-pixbuf', 'gtk3'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\librsvg.sln')
        self.install(r'.\COPYING share\doc\librsvg')

    def post_install(self):
        self.exec_cmd(r'%(gtk_dir)s\bin\gdk-pixbuf-query-loaders.exe --update-cache')

@project_add
class Project_sqlite(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'sqlite',
            archive_url = 'https://www.sqlite.org/2016/sqlite-autoconf-3120200.tar.gz',
            hash = 'fd00770c9afd39db555c78400e52f55e8bd6568c78be23561abb472a22d09abb',
            )

    def build(self):
        nmake_debug = 'DEBUG=2' if self.builder.opts.configuration == 'debug' else 'DEBUG=0'
        self.exec_vs(r'nmake /f Makefile.msc sqlite3.dll DYNAMIC_SHELL=1 ' + nmake_debug)

        self.install('sqlite3.h include')
        self.install('sqlite3.dll sqlite3.pdb bin')
        self.install('sqlite3.lib lib')

@project_add
class Project_libcurl(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'libcurl',
            archive_url = 'https://github.com/curl/curl/releases/download/curl-7_54_0/curl-7.54.0.tar.gz',
            hash = 'a84b635941c74e26cce69dd817489bec687eb1f230e7d1897fc5b5f108b59adf',
            dependencies = ['perl', 'cmake', 'ninja', ],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True)
        # Fix the pkg-config .pc file, correcting the library's names
        file_replace(os.path.join(self.pkg_dir, 'lib', 'pkgconfig', 'libcurl.pc'),
                     [ (' -lcurl', ' -llibcurl_imp'),
                       ]
                     )

        self.install(r'.\COPYING share\doc\libcurl')

@project_add
class Project_libsoup(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libsoup',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/libsoup/2.60/libsoup-2.60.2.tar.xz',
            hash = '7263cfe18872e2e652c196f5667e514616d9c97c861dfca82a65a55f45f0da01',
            dependencies = ['libxml2', 'glib-openssl', 'sqlite'],
            patches = [
                '0001-websocket-connection-do-not-send-new-frames-until-th.patch',
                ],
            )

    def build(self):
        self.exec_msbuild(r'win32\vs%(vs_ver)s\libsoup.sln')

        self.install(r'.\COPYING share\doc\libsoup')

@project_add
class Project_libssh(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libssh',
            archive_url = 'https://red.libssh.org/attachments/download/218/libssh-0.7.5.tar.xz',
            hash = '54e86dd5dc20e5367e58f3caab337ce37675f863f80df85b6b1614966a337095',
            dependencies = ['zlib','openssl'],
            )

    def build(self):
        self.exec_msbuild(r'build\vs%(vs_ver)s\libssh-library.sln')

        self.install(r'.\COPYING share\doc\libssh')

@project_add
class Project_libssh2(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'libssh2',
            archive_url = 'https://www.libssh2.org/download/libssh2-1.8.0.tar.gz',
            hash = '39f34e2f6835f4b992cafe8625073a88e5a28ba78f83e8099610a7b3af4676d4',
            dependencies = ['cmake', 'ninja', ],
            )

    def build(self):
        CmakeProject.build(self, cmake_params='-DWITH_ZLIB=ON', use_ninja=True)
        self.install(r'.\COPYING share\doc\libssh2')

@project_add
class Project_libtiff4(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'libtiff-4',
            archive_url = 'ftp://download.osgeo.org/libtiff/tiff-4.0.8.tar.gz',
            hash = '59d7a5a8ccd92059913f246877db95a2918e6c04fb9d43fd74e5c3390dac2910',
            dependencies = ['cmake', 'ninja', 'libjpeg-turbo', ],
            patches = [
                '001-no-absolute-pc-paths.patch',
                ],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True)

        self.install(r'.\COPYRIGHT share\doc\tiff')

@project_add
class Project_libuv(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libuv',
            archive_url = 'https://github.com/libuv/libuv/archive/v1.11.0.tar.gz',
            hash = '6ec7eec6ecc24b1a8ffedebedb2fe9313fffb5410de89aaf784dd01080411c7a',
            )

    def build(self):
        rel_dir = r'Release'
        if self.builder.opts.configuration == 'debug':
            rel_dir = r'Debug'

        platform = r'x86'
        if self.builder.x64:
            platform = r'x64'

        tmp_python = os.getenv('PYTHON')
        os.environ["PYTHON"] = 'c:\python27\python'
        os.system(r'%s\vcbuild.bat build static %s %s' % (self._get_working_dir(), self.builder.opts.configuration, platform))
        if tmp_python != None:
            os.environ["PYTHON"] = tmp_python

        self.install(r'include\pthread-barrier.h include\libuv')
        self.install(r'include\stdint-msvc2008.h include\libuv')
        self.install(r'include\tree.h include\libuv')
        self.install(r'include\uv.h include\libuv')
        self.install(r'include\uv-aix.h include\libuv')
        self.install(r'include\uv-bsd.h include\libuv')
        self.install(r'include\uv-darwin.h include\libuv')
        self.install(r'include\uv-errno.h include\libuv')
        self.install(r'include\uv-linux.h include\libuv')
        self.install(r'include\uv-sunos.h include\libuv')
        self.install(r'include\uv-threadpool.h include\libuv')
        self.install(r'include\uv-unix.h include\libuv')
        self.install(r'include\uv-version.h include\libuv')
        self.install(r'include\uv-win.h include\libuv')

        self.push_location(rel_dir)
        self.install(r'run-benchmarks' + '.exe' + ' bin')
        self.install(r'run-tests' + '.exe' + ' bin')
        self.install(r'lib\libuv' + '.lib' + ' lib')
        self.pop_location()

        self.install(r'.\LICENSE share\doc\libuv')

@project_add
class Project_libxml2(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libxml2',
            archive_url = 'ftp://xmlsoft.org/libxml2/libxml2-2.9.7.tar.gz',
            hash = 'f63c5e7d30362ed28b38bfa1ac6313f9a80230720b7fb6c80575eeab3ff5900c',
            dependencies = ['win-iconv'],
            )

    def build(self):
        shutil.copy(os.path.join(self._get_working_dir(), 'include', 'win32config.h'),
                    os.path.join(self._get_working_dir(), 'config.h'))

        lib = ';'.join([self.builder.vs_env['LIB'],
                        os.path.join(self.builder.gtk_dir, 'lib')])

        nmake_config = 'DEBUG=1' if self.builder.opts.configuration == 'debug' else 'DEBUG=0'
        self.push_location(r'.\win32')
        self.exec_vs(r'nmake /nologo /f Makefile.msvc WITH_ICONV=1 LIB="%s" PREFIX="%s" %s' % (lib, self.builder.gtk_dir, nmake_config))
        self.exec_vs(r'nmake /nologo /f Makefile.msvc install LIB="%s" PREFIX="%s" %s' % (lib, self.builder.gtk_dir, nmake_config))
        self.pop_location()

        self.install(r'.\COPYING share\doc\libxml2')

@project_add
class Project_libyuv(GitRepo, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'libyuv',
            repo_url = 'https://chromium.googlesource.com/libyuv/libyuv',
            fetch_submodules = False,
            tag = None,
            dependencies = ['cmake', 'ninja', ],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True)

        self.install(r'.\LICENSE share\doc\libyuv')

@project_add
class Project_libzip(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'libzip',
            archive_url = 'https://nih.at/libzip/libzip-1.2.0.tar.gz',
            hash = '6cf9840e427db96ebf3936665430bab204c9ebbd0120c326459077ed9c907d9f',
            dependencies = ['cmake', 'ninja', 'zlib'],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True)
        self.install(r'.\LICENSE share\doc\libzip')

@project_add
class Project_lmdb(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'lmdb',
            archive_url = 'https://github.com/LMDB/lmdb/archive/LMDB_0.9.19.tar.gz',
            hash = '108532fb94c6f227558d45be3f3347b52539f0f58290a7bb31ec06c462d05326',
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\lmdb.sln')

        self.install(r'.\libraries\liblmdb\lmdb.h include')
        self.install(r'.\build\win32\vs%(vs_ver)s\%(platform)s\%(configuration)s\lmdb.lib lib')
        self.install(r'.\libraries\liblmdb\LICENSE share\doc\lmdb')

@project_add
class Project_lz4(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'lz4',
            archive_url = 'https://github.com/lz4/lz4/archive/v1.8.0.tar.gz',
            hash = '2ca482ea7a9bb103603108b5a7510b7592b90158c151ff50a28f1ca8389fccf6',
            )

    def build(self):
        self.exec_msbuild(r'visual\VS20%(vs_ver)s\lz4.sln')

        self.install(r'visual\VS20%(vs_ver)s\bin\%(platform)s_%(configuration)s\liblz4.dll visual\VS20%(vs_ver)s\bin\%(platform)s_%(configuration)s\liblz4.pdb bin')
        self.install(r'.\lib\lz4.h .\lib\lz4hc.h .\lib\lz4frame.h include')
        self.install(r'visual\VS20%(vs_ver)s\bin\%(platform)s_%(configuration)s\liblz4.lib lib')

        self.install(r'.\lib\LICENSE share\doc\lz4')

@project_add
class Project_openssl(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'openssl',
            archive_url = 'ftp://ftp.openssl.org/source/openssl-1.0.2n.tar.gz',
            hash = '370babb75f278c39e0c50e8c4e7493bc0f18db6867478341a832a982fd15a8fe',
            dependencies = ['perl', 'nasm', ],
            )

    def build(self):
        common_options = r'no-ssl2 no-ssl3 no-comp --prefix="%(pkg_dir)s"'
        add_path = None

        debug_option = ''
        if self.builder.opts.configuration == 'debug':
            debug_option = 'debug-'

        # Note that we want to give priority to the system perl version.
        # Using the msys2 one might endup giving us a broken build
        add_path = ';'.join([os.path.join(self.builder.perl_dir, 'bin'),
                             os.path.join(self.builder.opts.msys_dir, 'usr', 'bin')])

        if self.builder.x86:
            self.exec_vs(r'%(perl_dir)s\bin\perl.exe Configure ' + debug_option + 'VC-WIN32 ' + common_options)
            self.exec_vs(r'ms\do_nasm', add_path=add_path)
        else:
            self.exec_vs(r'%(perl_dir)s\bin\perl.exe Configure ' + debug_option + 'VC-WIN64A ' + common_options)
            self.exec_vs(r'ms\do_win64a', add_path=add_path)

        try:
            self.exec_vs(r'nmake /nologo -f ms\ntdll.mak vclean', add_path=add_path)
        except:
            pass

        self.exec_vs(r'nmake /nologo -f ms\ntdll.mak', add_path=add_path)
        self.exec_vs(r'nmake /nologo -f ms\ntdll.mak test', add_path=add_path)
        self.exec_vs(r'%(perl_dir)s\bin\perl.exe mk-ca-bundle.pl -n cert.pem')
        self.exec_vs(r'nmake /nologo -f ms\ntdll.mak install', add_path=add_path)

        self.install(r'.\cert.pem bin')
        self.install(r'.\openssl.cnf share')
        self.install(r'.\LICENSE share\doc\openssl\COPYING')
        self.install(r'.\pc-files\* lib\pkgconfig')

@project_add
class Project_opus(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'opus',
            archive_url = 'https://archive.mozilla.org/pub/opus/opus-1.2.1.tar.gz',
            hash = 'cfafd339ccd9c5ef8d6ab15d7e1a412c054bf4cb4ecbbbcc78c12ef2def70732',
            )

    def build(self):
        version = '13'
        if self.builder.opts.vs_ver == '14':
            version = '15'
        elif self.builder.opts.vs_ver == '15':
            version = '17'

        configuration = 'ReleaseDLL'
        if self.builder.opts.configuration == 'debug':
            configuration = 'DebugDLL'

        self.exec_msbuild(r'.\win32\VS20' + version + '\opus.sln', configuration=configuration)

        bin_dir = r'.\win32\VS20' + version + '\%s\%s' % (self.builder.opts.platform, configuration, )

        self.install(bin_dir + r'\opus.dll bin')
        self.install(bin_dir + r'\opus.pdb bin')

        self.install(bin_dir + r'\opus.lib lib')

        self.install(r'include\* include')

        self.install(r'COPYING share\doc\opus')

@project_add
class Project_pango(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'pango',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/pango/1.40/pango-1.40.14.tar.xz',
            hash = '90af1beaa7bf9e4c52db29ec251ec4fd0a8f2cc185d521ad1f88d01b3a6a17e3',
            dependencies = ['cairo', 'harfbuzz'],
            patches = ['0001-Drop-unused-_pango_ft2_ft_strerror.patch'],
            )

    def build(self):
        configuration = 'Release_FC'
        if self.builder.opts.configuration == 'debug':
            configuration = 'Debug_FC'

        self.exec_msbuild(r'win32\vs%(vs_ver)s\pango.sln', configuration=configuration)
        self.install(r'COPYING share\doc\pango')

@project_add
class Project_pixman(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'pixman',
            archive_url = 'http://cairographics.org/releases/pixman-0.34.0.tar.gz',
            hash = '21b6b249b51c6800dc9553b65106e1e37d0e25df942c90531d4c3997aa20a88e',
            )

    def build(self):
        optimizations = 'SSE2=on SSSE3=on'
        if self.builder.x64:
            # FIXME: cairo fails to build due to missing symbols if I enable MMX on 64bit
            optimizations += ' MMX=off'
        else:
            optimizations += ' MMX=on'

        add_path = os.path.join(self.builder.opts.msys_dir, 'usr', 'bin')

        self.exec_vs(r'make -f Makefile.win32 pixman CFG=%(configuration)s ' + optimizations, add_path=add_path)

        self.install(r'.\pixman\%(configuration)s\pixman-1.lib lib')

        self.install(r'.\pixman\pixman.h include\pixman-1')
        self.install(r'.\pixman\pixman-version.h include\pixman-1')

        self.install(r'.\COPYING share\doc\pixman')

@project_add
class Project_pkg_config(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'pkg-config',
            archive_url = 'https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz',
            hash = '6fc69c01688c9458a57eb9a1664c9aba372ccda420a02bf4429fe610e7e7d591',
            dependencies = [ 'glib', ],
            )

    def build(self):
        self.exec_vs(r'nmake /nologo /f Makefile.vc CFG=%(configuration)s GLIB_PREFIX="%(gtk_dir)s"')

        bin_dir = r'.\%s\%s' % (self.builder.opts.configuration, self.builder.opts.platform, )
        self.install(bin_dir + r'\pkg-config.exe bin')
        self.install(bin_dir + r'\pkg-config.pdb bin')

        self.install(r'.\COPYING share\doc\pkg-config')

@project_add
class Project_portaudio(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'portaudio',
            archive_url = 'http://www.portaudio.com/archives/pa_stable_v190600_20161030.tgz',
            dependencies = ['cmake', 'ninja', ],
            patches = [ '0001-Do-not-add-suffice-to-the-library-name.patch',
                        '0001-Fix-MSVC-check.patch' ]
            )

    def build(self):
        CmakeProject.build(self,
                           cmake_params='-DPA_DLL_LINK_WITH_STATIC_RUNTIME=off',
                           use_ninja=True,
                           do_install=False,
                           out_of_source=False)

        self.install(r'portaudio.dll bin')
        self.install(r'portaudio.pdb bin')
        self.install(r'portaudio.lib lib')

        self.install(r'.\include\* include')

        self.install(r'.\LICENSE.txt share\doc\portaudio')

@project_add
class Project_protobuf(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'protobuf',
            archive_url = 'https://github.com/google/protobuf/releases/download/v3.3.0/protobuf-cpp-3.3.0.tar.gz',
            hash = '5e2587dea2f9287885e3b04d3a94ed4e8b9b2d2c5dd1f0032ceef3ea1d153bd7',
            dependencies = ['cmake', 'zlib', 'ninja', ],
            )

    def build(self):
        # We need to compile with STATIC_RUNTIME off since protobuf-c also compiles with it OFF
        CmakeProject.build(self,
                           cmake_params=r'-Dprotobuf_DEBUG_POSTFIX="" -Dprotobuf_BUILD_TESTS=OFF -Dprotobuf_WITH_ZLIB=ON -Dprotobuf_MSVC_STATIC_RUNTIME=OFF',
                           use_ninja=True,
                           source_part='cmake')

        self.install(r'.\LICENSE share\doc\protobuf')

@project_add
class Project_protobuf_c(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'protobuf-c',
            archive_url = 'https://github.com/protobuf-c/protobuf-c/releases/download/v1.3.0/protobuf-c-1.3.0.tar.gz',
            hash = '5dc9ad7a9b889cf7c8ff6bf72215f1874a90260f60ad4f88acf21bb15d2752a1',
            dependencies = ['cmake', 'protobuf', 'ninja', ],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True, source_part='build-cmake')

        self.install(r'.\LICENSE share\doc\protobuf-c')

@project_add
class Project_win_iconv(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'win-iconv',
            archive_url = 'http://dl.hexchat.net/gtk-win32/src/win-iconv-0.0.8.tar.gz',
            hash = '23adea990a8303c6e69e32a64a30171efcb1b73824a1c2da1bbf576b0ae7c520',
            dependencies = ['cmake', 'ninja', ],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True, cmake_params='-DBUILD_TEST=1', make_tests=True)

        self.install(r'.\COPYING share\doc\win-iconv')

@project_add
class Project_wing(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'wing',
            archive_url = 'https://gitlab.gnome.org/GNOME/wing/repository/v0.0.14/archive.tar.gz',
            hash = 'ebae9f7a51c585541cfb320c32ad1ea5f5d13414800205001c8065b0f2b27f37',
            dependencies = ['ninja', 'meson', 'pkg-config', 'glib'],
            )

    def build(self):
        Meson.build(self)
        self.install(r'.\COPYING share\doc\wing')

@project_add
class Project_x264(GitRepo, Project):
    def __init__(self):
        Project.__init__(self,
            'x264',
            repo_url = 'http://git.videolan.org/git/x264.git',
            fetch_submodules = False,
            dependencies = ['yasm', ],
            tag = '97eaef2ab82a46d13ea5e00270712d6475fbe42b',
            patches = [ '0001-use-more-recent-version-of-config.guess.patch',
                        '0002-configure-recognize-the-msys-shell.patch' ]
            )
    def build(self):
        self.exec_vs(r'bash build\build.sh %s %s' % (convert_to_msys(self.builder.gtk_dir), self.builder.opts.configuration),
                     add_path=os.path.join(self.builder.opts.msys_dir, 'usr', 'bin'))

        # use the path expected when building with a dependent project
        self.builder.exec_msys(['mv', 'libx264.dll.lib', 'libx264.lib'], working_dir=os.path.join(self.builder.gtk_dir, 'lib'))

        self.install(r'.\COPYING share\doc\x264')

@project_add
class Project_zlib(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'zlib',
            archive_url = 'http://www.zlib.net/zlib-1.2.11.tar.xz',
            hash = '4ff941449631ace0d4d203e3483be9dbc9da454084111f97ea0a2114e19bf066',
            )

    def build(self):
        options = ''
        if self.builder.opts.configuration == 'debug':
            options = 'CFLAGS="-nologo -MDd -W3 -Od -Zi -Fd\\"zlib\\""'

        self.exec_vs(r'nmake /nologo /f win32\Makefile.msc STATICLIB=zlib-static.lib IMPLIB=zlib1.lib ' + options)

        self.install(r'.\zlib.h .\zconf.h include')
        self.install(r'.\zlib1.dll .\zlib1.pdb bin')
        self.install(r'.\zlib1.lib lib')

        self.install(r'.\pc-files\* lib\pkgconfig')
        self.install(r'.\README share\doc\zlib')

@project_add
class Project_pycairo(GitRepo, CmakeProject):
    def __init__(self):
        GitRepo.__init__(self)
        Project.__init__(self,
                         'pycairo',
                         repo_url='git://github.com/muntyan/pycairo-gtk-win32.git',
                         fetch_submodules = False,
                         tag = None,
                         dependencies = ['cmake', 'cairo'],
                         )

@project_add
class Project_pygobject(GitRepo, CmakeProject):
    def __init__(self):
        GitRepo.__init__(self)
        Project.__init__(self,
                         'pygobject',
                         repo_url='git://github.com/muntyan/pygobject-gtk-win32.git',
                         fetch_submodules = False,
                         tag = None,
                         dependencies = ['cmake', 'glib'],
                         )

@project_add
class Project_pygtk(GitRepo, CmakeProject):
    def __init__(self):
        GitRepo.__init__(self)
        Project.__init__(self,
                         'pygtk',
                         repo_url='git://github.com/muntyan/pygtk-gtk-win32.git',
                         fetch_submodules = False,
                         tag = None,
                         dependencies = ['cmake', 'gtk', 'pycairo', 'pygobject'],
                         )

@project_add
class Project_check_libs(NullExpander, Meson):
    def __init__(self):
        Project.__init__(self,
            'check-libs',
            dependencies = [
                    # Used to build the various tests
                    'meson',
                    'ninja',
                    'pkg-config',
                    # libraries to test, hopefully all the one we build!
                    'atk',
                    'cairo',
                    'freetype',
                    'gdk-pixbuf',
                    'glib',
                    'jasper',
                    'json-glib',
                    'libarchive',
                    'libcurl',
                    'libffi',
                    'libjpeg-turbo',
                    'libpng',
                    'libtiff-4',
                    'pango',
                    'zlib',

                ],
            )

    def build(self):
        Meson.build(self, make_tests=True)
        self.install(r'.\COPYING share\doc\check-libs')

@project_add
class Project_dev_shell(Project):
    def __init__(self):
        Project.__init__(self,
            'dev-shell',
            # We may need all tools
            dependencies = [ 'tools' ],
            )
        # We don't want this project to be built with the group 'all'
        self.type = GVSBUILD_IGNORE

    def unpack(self):
        # Nothing to do, it's not really a project
        pass

    def build(self):
        # Do the shell
        print("")
        print("gvsbuild dev shell. Type exit to exit :)")
        print("")
        # If you need to use it as a --prefix in some build test ...
        self.builder.mod_env('GTK_BASE_DIR', self.builder.gtk_dir)
        self.builder.mod_env('PROMPT', '[ gvsbuild shell ] $P $G', subst=True)
        self.builder.exec_vs("cmd", working_dir=self.builder.working_dir)

