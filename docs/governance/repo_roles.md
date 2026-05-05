# TerraNova Restore Repository Role Map

Status: working inventory  
Scope: repositories visible through the GitHub connector on 2026-05-05

This map classifies repository purpose. It is not a security audit and does not imply that every file has been reviewed.

## Role labels

| Role | Meaning |
| --- | --- |
| `core` | Primary operating repository for TerraNova/FerrAI governance, sync, release and documentation. |
| `fork` | External upstream project fork or dependency mirror. |
| `research` | Research/data repository. |
| `private-app` | Private app or product prototype. |
| `archive` | Storage or historical/reference material. |
| `release` | Publication, Zenodo, artifact or distribution layer. |
| `raw-docs` | Raw documentation, IPFS or export-heavy document layer. |
| `sandbox` | Demo, test or experimental repository. |
| `identity` | Profile, author or identity-facing repository. |

## Visible repositories

| Repository | Visibility | Default branch | Working role | Notes |
| --- | --- | --- | --- | --- |
| `Terra-Nova-Restore/TerraNova-s-Framework` | public | `main` | `core`, `release`, `raw-docs` | Main governance, sync, atlas, dissertation and Zenodo layer. Highest public-boundary sensitivity. |
| `Terra-Nova-Restore/notion-mcp-server` | public | `main` | `fork` | Notion MCP Server fork / connector research layer. Keep upstream distinction clear. |
| `Terra-Nova-Restore/mermaid` | public | `develop` | `fork` | Mermaid fork / diagram dependency. Should not be confused with TerraNova original code. |
| `Terra-Nova-Restore/gumroad` | public | `main` | `archive`, `release` | Large public repository; purpose should be reviewed separately. |
| `Terra-Nova-Restore/miniapps` | public | `main` | `sandbox` | App sandbox / mini app layer; README and purpose should be clarified. |
| `Terra-Nova-Restore/TeNeVaRa` | private | `main` | `private-app` | Private application seed. Keep private unless public release is reviewed. |
| `Terra-Nova-Restore/ipfs-docs-FerrAI` | public | `main` | `raw-docs`, `archive` | IPFS/FerrAI documentation layer; review CIDs and sensitive references before promotion. |
| `Terra-Nova-Restore/FlyWireConnectome` | public | `main` | `research` | Research/data layer; verify source licence and attribution. |
| `Terra-Nova-Restore/demo-repository` | private | `main` | `sandbox` | Minimal private demo repository. |
| `Terra-Nova-Restore/Silvan-Lenhard` | public | `main` | `identity` | Minimal identity/profile placeholder. |

## Operating rules

- Core work should land in `TerraNova-s-Framework` through issues and pull requests.
- Forks should remain clearly marked as forks or dependency mirrors.
- Private app work should stay private until a public release boundary exists.
- Raw-docs repositories require the same public-boundary classification as the main repository.
- Large repositories should receive a short README stating purpose, origin, licence and public/private stance.

## Next review targets

1. Clarify `miniapps` purpose with a README.
2. Review `gumroad` purpose and public suitability.
3. Review `ipfs-docs-FerrAI` for CIDs, wallet/token references and patent-sensitive material.
4. Keep `notion-mcp-server` and `mermaid` labelled as forks/dependency layers.
5. Keep `TerraNova-s-Framework` as the canonical working hub, but not as a raw private archive.