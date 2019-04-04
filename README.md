libtalloc-2.2.x-srpm
====================

SRPM building tools for libtalloc-2.2.x, needed for Samba 4 on RHEL 8 and Fedora.

These are built from Fedora rawhide releases, and need to be built and
installed in the following order.

	libtalloc-2.2.x-srpm
	libtdb-1.3.x-srpm
	libldb-1.6.x-srpm
	libtevent-0.10.x-srpm

	samba-4.10.x-srpm

The "make" command will do these steps.

	make build	# Build the package on the local OS
	make all	# Use "mock" to build the packages with the local
			# samba4repo-f29-x96_64 configuration
	make install	# Actually install the RPM's in the designated
			# location for samba4repo-6-x86_64


		Nico Kadel-Garcia <nkadel@gmail.com>
