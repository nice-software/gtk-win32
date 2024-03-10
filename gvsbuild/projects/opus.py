#  Copyright (C) 2016 The Gvsbuild Authors
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
from gvsbuild.utils.base_project import project_add


@project_add
class Opus(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "opus",
            version="1.5.1",
            repository="https://github.com/xiph/opus",
            archive_url="https://github.com/xiph/opus/archive/refs/tags/v{version}.tar.gz",
            archive_filename="opus-{version}.tar.gz",
            hash="7ce44ef3d335a3268f26be7d53bb3bed7205b34eaf80bf92a99e69d490afe9d9",
            dependencies=[
                "ninja",
                "meson",
                "pkgconf",
            ],
        )

        self.add_param("-Dtests=disabled")
        self.add_param("-Ddocs=disabled")

    def build(self):
        Meson.build(self)
        self.install(r"COPYING share\doc\opus")
