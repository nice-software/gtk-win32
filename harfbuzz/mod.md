 * Download [HarfBuzz 0.9.38](http://www.freedesktop.org/software/harfbuzz/release/harfbuzz-0.9.38.tar.bz2)
 * Download [blinkseb's HarfBuzz solution](https://github.com/blinkseb/harfbuzz)
 * Extract to `C:\mozilla-build\hexchat`
 * Open `win32\harfbuzz.sln` with VS
 * Generate .def file:
	* Open solution
	* Select `Release|Win32` configuration
	* Build solution
	* Start Developer Command Prompt for VS2013
	<pre>cd C:\mozilla-build\hexchat\build\Win32\harfbuzz\win32\libs\Release
powershell.exe -command "Out-File -Encoding utf8 -FilePath ..\\..\\harfbuzz.def -InputObject 'EXPORTS'; dumpbin /LINKERMEMBER harfbuzz.lib | Select-String ' .. \_(hb\_.*)$' | %{ $_.Matches[0].Groups[1].Value } | Out-File -Encoding utf8 -Append -FilePath ..\\..\\harfbuzz.def"</pre>
	* Go back to solution and change the project type to DLL.
	* Set _Linker_ `->` _Input_ `->` _Module DefinitionFile_ to `harfbuzz.def`
 * Add lib path and fix freetype name
 * Add `<Import Project="..\..\stack.props" />`
 * Add `<Import Project="harfbuzz.props" />`
 * Select `Release|Win32` configuration
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
