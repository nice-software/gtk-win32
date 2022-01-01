#!/usr/bash

prefix="$1"
gtk_dir="$2"
build_type="$3"
enable_gpl="$4"

extra_cflags=""
extra_flags=""

if [ "$build_type" = "debug" ]; then
    extra_flags="--enable-debug $extra_flags"
    # FIXME: the -Od and -Zi instructions are overriden in the compilation command
    extra_cflags="-Od -Zi -MDd $extra_cflags"
fi

if [ "$enable_gpl" = "enable_gpl" ]; then
    extra_flags="--enable-libx264 --enable-gpl --enable-encoder=\"libx264\" $extra_flags"
fi

export PKG_CONFIG_PATH=$gtk_dir/lib/pkgconfig:$PKG_CONFIG_PATH

./configure \
 --toolchain=msvc \
 --prefix="$prefix" \
 --enable-shared \
 --disable-everything \
 --enable-swscale \
 --enable-avcodec \
 --enable-hwaccel=h264_dxva2 \
 --enable-hwaccel=hevc_dxva2 \
 --enable-dxva2 \
 --enable-decoder=h264 \
 --enable-decoder=hevc \
 --enable-decoder=mpeg1video \
 --enable-encoder=mpeg1video \
 --enable-hwaccel=h264_d3d11va \
 --enable-hwaccel=h264_d3d11va2 \
 --enable-hwaccel=hevc_d3d11va \
 --enable-hwaccel=hevc_d3d11va2 \
 --enable-d3d11va \
 --enable-nvdec \
 --enable-hwaccel=h264_nvdec \
 --enable-hwaccel=hevc_nvdec \
 --disable-programs \
 --disable-avformat \
 --disable-avfilter \
 --disable-avdevice \
 --disable-swresample \
 --extra-cflags="$extra_cflags" \
 "$extra_flags"

make
make install
