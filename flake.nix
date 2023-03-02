{
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }: flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs { inherit system; };
    in
    {
      packages.default = pkgs.stdenv.mkDerivation rec {
        name = "my-switches";
        src = ./.;
        propagatedBuildInputs = with pkgs; [
          (python3.withPackages (p: with p; [
            paho-mqtt
          ]))
        ];

        installPhase = ''
          mkdir -p $out/bin
          cp ./main.py $out/bin/my-switches
        '';
      };

      devShell = pkgs.mkShell {
        buildInputs = [
          (pkgs.python3.withPackages (ps: with ps; [
            paho-mqtt
          ]))
        ];
      };
    });
}
