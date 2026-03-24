from collections.abc import Callable
from typing import Any, TypeVar

from utils import get_provider

ProviderT = TypeVar("ProviderT")


def make_provider_api(
    provider_cls: type[ProviderT],
    *,
    env_var: str,
    default_provider: str,
    provider_label: str,
    action_name: str,
    auto_provider: str = "auto",
) -> tuple[Callable[[str], ProviderT], Callable[..., Any]]:
    providers = {provider_cls.provider_name: provider_cls}

    def get_selected_provider(provider_name: str = auto_provider) -> ProviderT:
        return get_provider(
            provider_name,
            providers,
            env_var=env_var,
            default_provider=default_provider,
            provider_label=provider_label,
            auto_provider=auto_provider,
        )

    def action(*args: Any, provider_name: str = auto_provider, **kwargs: Any) -> Any:
        provider = get_selected_provider(provider_name)
        return getattr(provider, action_name)(*args, **kwargs)

    get_selected_provider.__name__ = f"get_{provider_label.lower()}_provider"
    get_selected_provider.__qualname__ = get_selected_provider.__name__
    action.__name__ = action_name
    action.__qualname__ = action_name

    return get_selected_provider, action
