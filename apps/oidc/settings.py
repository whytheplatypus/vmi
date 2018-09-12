from oauth2_provider.settings import OAuth2ProviderSettings

DEFAULTS = {
    "OIDC_CLAIM_PROVIDER": 'apps.oidc.claims.DefaultProvider',
    "OIDC_JWT_BUILDER": 'apps.oidc.jwt.DefaultBuilder',
}

IMPORT_STRINGS = (
    "OIDC_CLAIM_PROVIDER",
    "OIDC_JWT_BUILDER",
)

oidc_settings = OAuth2ProviderSettings(import_strings=IMPORT_STRINGS, defaults=DEFAULTS)
