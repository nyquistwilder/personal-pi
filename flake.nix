{
  description = "skills";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    treefmt-nix.url = "github:numtide/treefmt-nix";
  };

  outputs =
    {
      self,
      nixpkgs,
      treefmt-nix,
    }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
      ];

      forAllSystems = nixpkgs.lib.genAttrs systems;

      perSystem =
        system:
        let
          pkgs = import nixpkgs { inherit system; };

          treefmtEval = treefmt-nix.lib.evalModule pkgs {
            projectRootFile = "flake.nix";

            settings = {
              global.excludes = [
                ".git/**"
                ".direnv/**"
                ".rumdl_cache/**"
                "result"
                "result-*"
              ];

              formatter = {
                nix = {
                  command = "${pkgs.nixfmt}/bin/nixfmt";
                  includes = [ "*.nix" ];
                };

                markdown = {
                  command = "${pkgs.rumdl}/bin/rumdl";
                  options = [ "fmt" ];
                  includes = [ "*.md" ];
                };

                toml = {
                  command = "${pkgs.taplo}/bin/taplo";
                  options = [ "fmt" ];
                  includes = [ "*.toml" ];
                };

                yaml = {
                  command = "${pkgs.yamlfmt}/bin/yamlfmt";
                  includes = [
                    "*.yaml"
                    "*.yml"
                  ];
                };

                json = {
                  command = "${pkgs.prettier}/bin/prettier";
                  options = [ "--write" ];
                  includes = [
                    "*.json"
                    "*.jsonc"
                  ];
                };

                shell = {
                  command = "${pkgs.shfmt}/bin/shfmt";
                  options = [ "-w" ];
                  includes = [
                    "*.sh"
                    "*.bash"
                  ];
                };
              };
            };
          };
        in
        {
          inherit pkgs treefmtEval;
        };
    in
    {
      formatter = forAllSystems (system: (perSystem system).treefmtEval.config.build.wrapper);

      checks = forAllSystems (system: {
        formatting = (perSystem system).treefmtEval.config.build.check self;
      });

      devShells = forAllSystems (
        system:
        let
          inherit (perSystem system) pkgs;
        in
        {
          default = pkgs.mkShell {
            packages = [
              (perSystem system).treefmtEval.config.build.wrapper
              pkgs.actionlint
              pkgs.deadnix
              pkgs.editorconfig-checker
              pkgs.gitleaks
              pkgs.jq
              pkgs.just
              pkgs.ls-lint
              pkgs.nixfmt
              pkgs.prek
              pkgs.prettier
              pkgs.rumdl
              pkgs.shellcheck
              pkgs.shfmt
              pkgs.statix
              pkgs.taplo
              pkgs.trivy
              pkgs.typos
              pkgs.yamlfmt
            ];
          };
        }
      );
    };
}
