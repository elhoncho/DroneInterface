# DroneInterface

Building a Cross Compiler on Mac OSX

-------First Step--------
Reinstalled osx with case sensitive partition

------Install Toolchain-------
install jdk
xcode-select --install

/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew update
brew install bash
brew install autoconf
brew install gnu-sed
brew install binutils
brew install automake
brew install coreutils
brew install gawk
brew install libelf
brew install libtool
brew install wget
brew install xz
brew install help2man
brew install bison
export PATH=/usr/local/Cellar/bison/3.0.4_1/bin:$PATH

git clone https://github.com/crosstool-ng/crosstool-ng
./bootstrap
./configure --prefix=/Users/owner/Documents/crosstool-ng-build/
make
make install
export PATH="${PATH}:/Users/owner/Documents/crosstool-ng-build/bin/
sudo ln -s /usr/local/bin/gsha512sum sha512sum

ct-ng armv6-rpi-linux-gnueabi
Ulimit -n 1024
ct-ng build


-------Get sysroot of target-----------
brew install rsync
mkdir sysroot
rsync -rzLR --safe-links \
      pi@192.168.1.101:/usr/lib/arm-linux-gnueabihf \
      pi@192.168.1.101:/usr/lib/gcc/arm-linux-gnueabihf \
      pi@192.168.1.101:/usr/include \
      pi@192.168.1.101:/lib/arm-linux-gnueabihf \
      sysroot/

rsync -rzLR --safe-links pi@192.168.1.101:/usr/local/lib/ pi@192.168.1.101:/usr/local/include/ sysroo

-----Setup Eclipse--------
Right click project->properties
	Cross Settings
		Prefix: armv6-rpi-linux-gnueabi-
		Path: /Users/owner/x-tools/armv6-rpi-linux-gnueabi/bin
	Cross GCC Compiler->Includes
		Includes Path (-I)
			"${workspace_loc:/${ProjName}/AT86RF212B/Inc}"
			/Users/owner/RaspberryPiEnv/sysroot/usr/local/include
	Cross GCC Linker->Libraries
		Libraries(-I)
			wiringPi
		Library search path (-L)
			/Users/owner/RaspberryPiEnv/sysroot/usr/local/lib


------Update Binaries------
Install sshpass
sshpass -p 'raspberry' scp Debug/RaspberryPi pi@192.168.1.101:/home/pi/test/
