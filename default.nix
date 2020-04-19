with import <nixpkgs> {};
crystal.buildCrystalPackage rec {
  version = "0.1.0";
  pname = "ChocoBot";
  src = ./.;

  shardsFile = ./shards.nix;
  crystalBinaries.ChocoBot.src = "src/ChocoBot.cr";
}
