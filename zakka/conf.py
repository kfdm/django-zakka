from django.conf import settings as django_settings


try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version, PackageNotFoundError


def user_agent(name):
    try:
        v = version(distribution_name=name)
    except PackageNotFoundError:
        v = "unknown"

    try:
        from django.contrib.sites.shortcuts import get_current_site

        domain = get_current_site(None).domain
    except Exception:
        return f"{name}/{v}"
    else:
        return f"{name}/{v} (+{domain})"


DEFAULTS = {
    "USER_AGENT_DISTRIBUTION": "django-zakka",
    "USER_AGENT": user_agent,
}


class SettingsWrapper:
    def __getattr__(self, key):
        if key in DEFAULTS:
            if callable(DEFAULTS[key]):
                if key == "USER_AGENT":
                    DEFAULTS[key] = DEFAULTS[key](self.USER_AGENT_DISTRIBUTION)
            return getattr(django_settings, key, DEFAULTS[key])
        return getattr(django_settings, key)


settings = SettingsWrapper()
