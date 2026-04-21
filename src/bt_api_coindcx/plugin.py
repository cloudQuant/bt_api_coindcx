from __future__ import annotations

from typing import Any

from bt_api_base.plugins.protocol import PluginInfo

from bt_api_coindcx import __version__
from bt_api_coindcx.registry_registration import register_coindcx


def get_plugin_info() -> PluginInfo:
    return PluginInfo(
        name="bt_api_coindcx",
        version=__version__,
        core_requires=">=0.15,<1.0",
        supported_exchanges=("COINDCX___SPOT",),
        supported_asset_types=("SPOT",),
        plugin_module="bt_api_coindcx.plugin",
    )


def register_plugin(registry: Any, runtime_factory: Any) -> PluginInfo:
    del runtime_factory
    register_coindcx(registry)
    return get_plugin_info()
