{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  packages = with pkgs; [
    (python310.withPackages (ps: with ps; [
      pyside6
      polib
    ]))
  ];
}
