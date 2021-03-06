with import (builtins.fetchTarball {
  # nixos-unstable on 2020-10-13
  url =
    "https://github.com/NixOS/nixpkgs/tarball/420f89ceb267b461eed5d025b6c3c0e57703cc5c";
  sha256 = "0c9kr76p6nmf4z2j2afgcddckbaxq6kxlmp1895h6qamm1c0ypb9";
}) { };

poetry2nix.mkPoetryApplication {
  projectDir = ./.;
  nativeBuildInputs = [ tesseract ];
}
