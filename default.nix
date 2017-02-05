with import <nixpkgs> {};

let

      w3lib  = python35Packages.buildPythonPackage rec {
         name = "python3.5-w3lib-1.16.0";
         src = fetchurl {
           url = "https://pypi.python.org/packages/c8/4d/47d96235c171e456e711c0e5f14eb836e3215b838b064c1f2e5d336a7ca5/w3lib-1.16.0.tar.gz";
           md5 = "09be7841a9f5c651bc9e759bed7c7dc5";
           };
       propagatedBuildInputs = [ python35Packages.six ];
       dontStrip = true;
       };


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
     #libxml2
     #libxslt
     #libffi
     #stdenv
     #zlib
     #gcc
     #clang
     #openssl
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
