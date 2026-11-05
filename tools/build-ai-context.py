"""Build an explicit allowlist of source context; never collect environment files."""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sources = [
    ('Platform', root, 'packages/design/smartcore.css'),
    ('Platform', root, 'apps/console/src/lib/platform.ts'),
    ('Platform', root, 'apps/console/src/components/shell.tsx'),
    ('Platform', root, 'apps/console/src/components/module-directory.tsx'),
    ('Platform', root, 'apps/console/src/components/preferences.tsx'),
    ('Platform', root, 'apps/console/src/app/[locale]/page.tsx'),
    ('Platform', root, 'apps/console/src/app/globals.css'),
    ('Identity', root.parent/'SmartCoreIdentity', 'web/identity/src/app/globals.css'),
    ('Business', root.parent/'SmartCoreServiceBusiness', 'frontend/components/app-shell.tsx'),
    ('Business', root.parent/'SmartCoreServiceBusiness', 'frontend/app/globals.css'),
]
text = [
    '# SmartCore design context\n',
    'Curated source snapshot. No runtime credentials, environments or customer data.\n',
    'This is an implemented modular-platform UI, not a KimiaBeauty website.\n',
    'Canonical tokens are in Platform/packages/design/smartcore.css; copies in apps are generated.\n',
    'The console is public navigation. Real authentication and organization-scoped permissions are separate.\n',
]
for label, repository, relative in sources:
    path = repository/relative
    if not path.is_file():
        raise SystemExit(f'Missing allowlisted source: {path}')
    language = 'css' if path.suffix == '.css' else 'tsx' if path.suffix == '.tsx' else 'ts'
    text.append(f'\n## {label}: {relative}\n\n```{language}\n{path.read_text(encoding="utf-8")}\n```\n')
destination = root/'handoff'/'AI_STUDIO_CONTEXT.md'
destination.parent.mkdir(parents=True, exist_ok=True)
destination.write_text('\n'.join(text), encoding='utf-8')
print(f'Created allowlisted context: {destination} ({destination.stat().st_size} bytes)')
