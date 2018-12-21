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
Various downloader / unpacker (tar, git, hg, ...)
"""

import os
import shutil
import zipfile
import tarfile

from .simple_ui import print_log
from .simple_ui import print_debug
from .utils import rmtree_full

def extract_exec(src, dest_dir, dir_part=None, strip_one=False, check_file=None, force_dest=None, check_mark=False):
    """
    Extract (or copy, in case of an exe file) from src to dest_dir,
    handling the strip of the first part of the path in case of the tarbombs.

    dir_part is a piece, present in the tar/zip file, added to the desst_dir for
    the checks

    if check_file is passed and is present in the filesystem the extract is
    skipped (tool alreay installed)

    force_dest can be used only on the exe file and set the destination name

    with check_mark the name of the original file extracted is written in the
    destination dir and checked, forcing a new, clean, extraction
    
    Returns True if the extraction has been done, False if it's skipped (so we can skip 
    marking the dependents of the project/tool)
    """

    # Support function
    def __get_stripped_tar_members(tar):
        for tarinfo in tar.getmembers():
            path = tarinfo.name.split('/')
            if len(path) == 1:
                if tarinfo.isdir():
                    continue
                else:
                    raise Exception('Cannot strip directory prefix from tar with top level files')
            tarinfo.name = '/'.join(path[1:])
            if tarinfo.issym() or tarinfo.islnk():
                tarinfo.linkname = '/'.join(tarinfo.linkname.split('/')[1:])
            yield tarinfo

    if dir_part:
        full_dest = os.path.join(dest_dir, dir_part)
    else:
        full_dest = dest_dir

    if check_mark:
        rd_file = ''
        try:
            with open(os.path.join(full_dest, '.wingtk-extracted-file'), 'rt') as fi:
                rd_file = fi.readline().strip()
        except IOError:
            pass

        wr_file = os.path.basename(src)
        if rd_file != wr_file:
            print_log('Forcing extraction of %s' % (src, ))
            rmtree_full(full_dest, retry=True)
            check_file = None
        else:
            # ok, finish, we've done
            return False

    if check_file is not None:
        if check_file:
            # look for the specific file
            if os.path.isfile(check_file):
                print_debug('Skipping %s handling, %s present' % (src, check_file, ))
                return False
        else:
            # If the directory exist we are ok
            if os.path.exists(full_dest):
                print_debug('Skipping %s handling, directory exists' % (src, ))
                return False

    print_log('Extracting %s to %s' % (src, full_dest, ))
    os.makedirs(full_dest, exist_ok=True)

    _n, ext = os.path.splitext(src.lower())
    if ext == '.exe':
        # Exe file, copy directly
        if force_dest:
            shutil.copy2(src, force_dest)
        else:
            shutil.copy2(src, dest_dir)
    elif ext == '.zip':
        # Zip file
        with zipfile.ZipFile(src) as zf:
            zf.extractall(path=dest_dir)
    else:
        # Ok, hoping it's a tarfile we can handle :)
        with tarfile.open(src) as tar:
            tar.extractall(dest_dir, __get_stripped_tar_members(tar) if strip_one else tar.getmembers())

    if check_mark:
        # write the data
        with open(os.path.join(full_dest, '.wingtk-extracted-file'), 'wt') as fo:
            fo.write('%s\n' % (os.path.basename(src), ))
    # Say that we have done the extraction
    return True

def dirlist2set(st_dir, add_dirs=False, skipped_dir=None):
    """
    Loads & return a set with all the files and, eventually,
    directory from a single dir.

    Used to make a file list to create a .zip file
    """
    def _load_single_dir(dir_name, returned_set, skipped_dir):
        for cf in os.scandir(dir_name):
            full = os.path.join(dir_name, cf.name.lower())
            if cf.is_file():
                returned_set.add(full)
            elif cf.is_dir():
                if cf.name.lower() in skipped_dir:
                    print_debug("  Skipped dir '%s' (from '%s')" % (cf.name, dir_name, ))
                else:
                    if (add_dirs):
                        returned_set.add(full)
                    _load_single_dir(full, returned_set, skipped_dir)
    rt = set()
    if skipped_dir is None:
        skipped_dir = []
    skipped_dir.append('__pycache__')
    try:
        print_debug("Getting file list from '%s'" % (st_dir, ))
        _load_single_dir(st_dir, rt, set(skipped_dir))
    except FileNotFoundError:
        print("Warning: (--zip-continue) No file found on '%s'" % (st_dir, ))
    return rt

def make_zip(name, files, skip_spc=0):
    """
    Create the name .zip using all files. skip_spc spaces are dropped
    from the beginning of all file/dir names to avoid to have the full
    path (e.g. from c:\data\temp\build\my_arch we want to save only
    mt_arch
    """
    print_log('Creating zip file %s with %u files' % (name, len(files), ))
    with zipfile.ZipFile(name + '.zip', 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(list(files)):
            zf.write(f, arcname=f[skip_spc:])

class Tarball(object):
    def update_build_dir(self):
        rt = extract_exec(self.archive_file, self.build_dir, strip_one=not self.tarbomb, check_mark=True)
        if rt:
            print_log('Extracted %s (forced)' % (self.archive_file,))
        return rt

    def unpack(self):
        extract_exec(self.archive_file, self.build_dir, strip_one=not self.tarbomb, check_mark=True)
        print_log('Extracted %s' % (self.archive_file,))

class MercurialRepo(object):
    def unpack(self):
        print_log('Cloning %s to %s' % (self.repo_url, self.build_dir))
        self.exec_cmd('hg clone %s %s-tmp' % (self.repo_url, self.build_dir))
        shutil.move(self.build_dir + '-tmp', self.build_dir)
        print_log('Cloned %s to %s' % (self.repo_url, self.build_dir))

    def update_build_dir(self):
        print_log('Updating directory %s' % (self.build_dir,))
        self.exec_cmd('hg pull -u', working_dir=self.build_dir)

class GitRepo(object):
    def create_zip(self):
        """
        Create a .zip file with the git checkout to be able to 
        work offline and as a reference of the last correct build
        """
        if self.tag:
            # name the .zip from the tag, validating it
            t_name = [ c if c.isalnum() else '_' for c in self.tag ]
            zip_post = ''.join(t_name)
        else:
            of = os.path.join(self.build_dir, '.git-temp.rsp')
            self.builder.exec_msys('git rev-parse --short HEAD >%s' % (of, ), working_dir=self.build_dir)
            with open(of, 'rt') as fi:
                zip_post = fi.readline().rstrip('\n')
            os.remove(of)
            
        # Be sure to have the git .zip dir
        git_tmp_dir = os.path.join(self.builder.opts.archives_download_dir, 'git')
        if not os.path.exists(git_tmp_dir):
            print_log("Creating git archives save directory %s" % (git_tmp_dir, ))
            os.makedirs(git_tmp_dir)
        
        # create a .zip file with the downloaded project
        all_files = dirlist2set(self.build_dir, add_dirs=True, skipped_dir=[ '.git', ])
        make_zip(os.path.join(git_tmp_dir, self.prj_dir + '-' + zip_post), all_files, len(self.build_dir))
        
    def unpack(self):
        print_log('Cloning %s to %s' % (self.repo_url, self.build_dir))

        self.builder.exec_msys('git clone %s %s-tmp' % (self.repo_url, self.build_dir))
        shutil.move(self.build_dir + '-tmp', self.build_dir)

        if self.tag:
            self.builder.exec_msys('git checkout -f %s' % self.tag, working_dir=self.build_dir)

        self.create_zip()
        if self.fetch_submodules:
            self.builder.exec_msys('git submodule update --init',  working_dir=self.build_dir)

        print_log('Cloned %s to %s' % (self.repo_url, self.build_dir))

    def update_build_dir(self):
        print_log('Updating directory %s' % (self.build_dir,))

        # I don't like too much this, but at least we ensured it is properly cleaned up
        self.builder.exec_msys('git clean -xdf', working_dir=self.build_dir)

        if self.tag:
            self.builder.exec_msys('git fetch origin', working_dir=self.build_dir)
            self.builder.exec_msys('git checkout -f %s' % self.tag, working_dir=self.build_dir)
        else:
            self.builder.exec_msys('git checkout -f', working_dir=self.build_dir)
            self.builder.exec_msys('git pull --rebase', working_dir=self.build_dir)

        self.create_zip()
        if self.fetch_submodules:
            self.builder.exec_msys('git submodule update --init', working_dir=self.build_dir)

        if os.path.exists(self.patch_dir):
            print_log("Copying files from %s to %s" % (self.patch_dir, self.build_dir))
            self.builder.copy_all(self.patch_dir, self.build_dir)

class NullExpander(object):
    """
    Null expander to use when all the source are present in the script and
    nothing must be downloaded

    """
    def update_build_dir(self):
        # Force the copy of the files in the script
        return True

    def unpack(self):
        # Everything is in our script, nothing to download
        pass

