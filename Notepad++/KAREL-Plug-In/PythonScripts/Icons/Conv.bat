@echo off
for %%f in (*.ico) do (
convert "%%f" -define bmp3:alpha=on "bmp3:%%~nf.bmp"
)
PAUSE