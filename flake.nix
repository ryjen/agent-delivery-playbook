{
  description = "Reproducible validation environment for the Agent Delivery Playbook";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs = { self, nixpkgs }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      forAllSystems = nixpkgs.lib.genAttrs systems;

      packagesFor = system:
        let
          pkgs = import nixpkgs { inherit system; };
          python = pkgs.python3.withPackages (ps: with ps; [
            pyyaml
            jsonschema
          ]);

          checkedSource = ''
            cp -R ${self} source
            chmod -R u+w source
            cd source
          '';
        in
        {
          inherit pkgs python checkedSource;
        };
    in
    {
      checks = forAllSystems (system:
        let
          env = packagesFor system;
        in
        {
          repository-integrity = env.pkgs.runCommand "agent-delivery-playbook-repository-integrity"
            {
              nativeBuildInputs = [ env.python ];
            }
            ''
              ${env.checkedSource}
              python3 scripts/validate-repository.py
              touch "$out"
            '';

          task-envelopes = env.pkgs.runCommand "agent-delivery-playbook-task-envelopes"
            {
              nativeBuildInputs = [ env.python ];
            }
            ''
              ${env.checkedSource}
              python3 -m unittest discover -s tests -p 'test_*.py' -v
              python3 scripts/validate-task-envelopes.py
              python3 scripts/validate-task-envelopes-standard.py
              python3 scripts/validate-adversarial-fixtures.py
              touch "$out"
            '';
        });

      devShells = forAllSystems (system:
        let
          env = packagesFor system;
        in
        {
          default = env.pkgs.mkShell {
            packages = [
              env.python
              env.pkgs.mise
            ];
          };
        });
    };
}
