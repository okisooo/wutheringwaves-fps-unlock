from cx_Freeze import setup, Executable

setup(
    name="Wuthering Waves FPS Unlock",
    version="1.1",
    description="A tool to change FPS",
    executables=[Executable("WW_Unlocker.py", icon="icon.ico", base="Win32GUI")]
)