"""linkedin-carousels Hermes plugin entrypoint.

Drop this folder into ~/.hermes/plugins/linkedin-carousels/, then run
`hermes plugins enable linkedin-carousels`. The agent gains five tools
under the `carousels` toolset plus the bundled SKILL.md orchestrator guide.
"""
from pathlib import Path

from . import schemas, tools

PLUGIN_DIR = Path(__file__).resolve().parent
SKILL_MD = PLUGIN_DIR / "data" / "SKILL.md"
TOOLSET = "carousels"


def register(ctx):
    """Wire schemas to handlers and bundle the orchestrator skill.

    Per Hermes' build-a-plugin guide:
      - Tools are registered via `ctx.register_tool(name=, toolset=,
        schema=, handler=)`.
      - Skills are bundled via `ctx.register_skill(name, path)`.
      - If this function crashes, the plugin is disabled but Hermes
        continues running normally.
    """
    for schema in schemas.ALL_SCHEMAS:
        ctx.register_tool(
            name=schema["name"],
            toolset=TOOLSET,
            schema=schema,
            handler=tools.HANDLERS[schema["name"]],
        )

    if SKILL_MD.exists():
        ctx.register_skill("linkedin-carousels", str(SKILL_MD))
