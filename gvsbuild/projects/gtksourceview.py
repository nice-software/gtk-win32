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

from gvsbuild.utils.base_builders import Meson
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class GtkSourceView(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gtksourceview",
            archive_url="https://download.gnome.org/sources/gtksourceview/4.8/gtksourceview-4.8.2.tar.xz",
            hash="842de7e5cb52000fd810e4be39cd9fe29ffa87477f15da85c18f7b82d45637cc",
            dependencies=["python", "meson", "ninja", "gtk3", "pkg-config"],
        )
        if Project.opts.enable_gi:
            self.add_dependency("gobject-introspection")
        else:
            self.add_param("-Dgir=false")
        self.add_param("-Dvapi=false")

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gtksourceview")
