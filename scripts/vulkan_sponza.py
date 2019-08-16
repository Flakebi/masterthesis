import os
from os import path
import shutil
import subprocess

from utils import *

name = "sponza"

def run(env, remove_cache, debug, sig):
	subprocess.run("/home/sebi/Dokumente/Dateien/Programme/Libraries/VulkanSponza/bin//vulkanSponza",
		cwd="/home/sebi/Dokumente/Dateien/Programme/Libraries/VulkanSponza/bin", check=True, env={**env, **dict(os.environ)})
	return RunResult(0)
