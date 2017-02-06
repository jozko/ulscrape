# Needs a w3lib override to >= 1.15.1 since upstream w3lib is at version 1.14.2
# scrapy starproject showing a weird problem not setting the
# top level project dir to +x, exiting with 'PermissionError: [Errno 13] Permission denied'
# on MacOS and Ubuntu 12.04. Need to test in NixOS maybe nix-shell is to blame?
with import <nixpkgs> {};

let
       Scrapy = python35Packages.buildPythonPackage rec {
         name = "Scrapy-1.3.0";
         src = fetchurl {
           url = "https://pypi.python.org/packages/e1/2d/f54cb2bed5d1d4bbc6ae093842282c8a0daad8c0cd9bf7504fbdf01b657f/Scrapy-1.3.0.tar.gz";
           md5 = "605e38a6ed446c9bdef8c0d0f09b8f61";
           };
       propagatedBuildInputs = [ 
            python35Packages.twisted 
            python35Packages.service-identity 
            python35Packages.virtualenv
            python35Packages.cffi
            python35Packages.twisted
            python35Packages.lxml
            python35Packages.parsel
            python35Packages.six
            python35Packages.pydispatcher
            python35Packages.service-identity
            python35Packages.pyopenssl
            python35Packages.queuelib
            python35Packages.w3lib
       ];
       checkPhase = ''
       '';
       doCheck = false;
       dontStrip = true;
       };

in
python35Packages.buildPythonPackage {
  name = "impurePythonEnv";
  buildInputs = [
     git
     Scrapy
     ];
      src = null;
      # When used as `nix-shell --pure`
      shellHook = ''
      export SOURCE_DATE_EPOCH=315532800
      unset http_proxy
      export GIT_SSL_CAINFO=/etc/ssl/certs/ca-bundle.crt
      '';
      # used when building environments
      extraCmds = ''
      unset http_proxy # otherwise downloads will fail ("nodtd.invalid")
      export SOURCE_DATE_EPOCH=315532800
      export GIT_SSL_CAINFO=/etc/ssl/certs/ca-bundle.crt
      '';
    }
