#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define	apxs	/usr/sbin/apxs
%include	/usr/lib/rpm/macros.perl
%define	pdir	Apache2
%define	pnam	POST200
Summary:	Apache2::POST200 - Converting code 200 responses to POST requests to 302
#Summary(pl):	
Name:		perl-Apache2-POST200
Version:	0.05
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	fdf227479b223afc1cea90f7b217cf4d
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-Apache-Test
BuildRequires:	perl-Digest-CRC
BuildRequires:	perl-mod_perl >= 2.000002
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module inserts an request output filter that looks for replies for
POST requests with a HTTP code of 200. If it finds one it saves the reply
in a database and replaces the complete output with a temporary redirect
(HTTP code 302) to the same URL but with a special marked query string
appended.

When the browser follows the redirect the module recognizes the query
string and routes the request to its own response handler. The handler
then reads the saved page from the database and sends it to the browser.

# %description -l pl
# TODO

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

APACHE_TEST_APXS=%{apxs} \
%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes
%{perl_vendorlib}/Apache2/*.pm
%{_mandir}/man3/*
